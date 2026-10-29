import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from uuid import uuid4

import numpy as np
import streamlit as st

from src.database.db import get_all_students

logger = logging.getLogger(__name__)
FACE_EMBEDDING_DIM = 128
FACE_MATCH_THRESHOLD = 0.6


@st.cache_resource
def load_dlib_models():
    try:
        import dlib
        import face_recognition_models

        try:
            models_version = version("face-recognition-models")
        except PackageNotFoundError:
            models_version = "unknown"
        logger.info(
            "Initializing face models (dlib=%s, face_recognition_models=%s)",
            getattr(dlib, "__version__", "unknown"),
            models_version,
        )

        shape_predictor_path = Path(
            face_recognition_models.pose_predictor_model_location()
        )
        face_recognition_path = Path(
            face_recognition_models.face_recognition_model_location()
        )
        for model_path in (shape_predictor_path, face_recognition_path):
            if not model_path.is_file() or model_path.stat().st_size == 0:
                raise FileNotFoundError("A required dlib model file is missing or empty.")

        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor(str(shape_predictor_path))
        facerec = dlib.face_recognition_model_v1(str(face_recognition_path))
    except Exception:
        logger.exception(
            "Face model initialization failed in "
            "src.pipelines.face_pipeline.load_dlib_models"
        )
        raise

    return detector, sp, facerec


def prepare_dlib_image(image_np, color_order="RGB"):
    """Return contiguous uint8 RGB pixels without changing image orientation."""
    image = np.asarray(image_np)
    channels = image.shape[2] if image.ndim == 3 else (1 if image.ndim == 2 else None)
    logger.debug(
        "Preparing face image: shape=%s dtype=%s channels=%s",
        image.shape,
        image.dtype,
        channels,
    )

    if image.ndim not in (2, 3):
        raise ValueError(
            f"Unsupported image dimensions {image.shape}; expected a 2D "
            "grayscale image or a 3D RGB/RGBA image."
        )
    if image.shape[0] == 0 or image.shape[1] == 0:
        raise ValueError("Cannot process an empty image.")

    if image.ndim == 3:
        if image.shape[2] == 4:
            image = image[:, :, :3]
        elif image.shape[2] != 3:
            raise ValueError(
                f"Unsupported image shape {image.shape}; expected RGB (3) or "
                "RGBA (4) channels."
            )

    if image.ndim == 2:
        image = np.repeat(image[:, :, np.newaxis], 3, axis=2)

    if not isinstance(color_order, str) or color_order.upper() not in {"RGB", "BGR"}:
        raise ValueError("color_order must be 'RGB' or 'BGR'.")

    if image.dtype != np.uint8:
        if np.issubdtype(image.dtype, np.floating):
            if not np.isfinite(image).all():
                raise ValueError("Image contains NaN or infinite values.")

            minimum = float(image.min())
            maximum = float(image.max())

            if minimum >= 0 and maximum <= 1:
                image = np.rint(image * 255).astype(np.uint8)
            elif minimum >= 0 and maximum <= 255:
                image = np.rint(image).astype(np.uint8)
            else:
                raise ValueError(
                    "Floating-point image pixels must be in [0, 1] normalized "
                    f"or [0, 255] intensity range; received [{minimum}, {maximum}]."
                )
        elif np.issubdtype(image.dtype, np.integer):
            minimum = int(image.min())
            maximum = int(image.max())
            if minimum < 0 or maximum > 255:
                raise ValueError(
                    "Integer image pixels must be in [0, 255]; "
                    f"received [{minimum}, {maximum}]."
                )
            image = image.astype(np.uint8)
        else:
            raise ValueError(
                f"Unsupported image dtype {image.dtype}; expected uint8 or "
                "numeric pixels in a supported 8-bit range."
            )

    if color_order.upper() == "BGR":
        image = image[:, :, ::-1]

    return np.ascontiguousarray(image, dtype=np.uint8)


def get_face_embeddings(image_np, color_order="RGB"):
    image_np = prepare_dlib_image(image_np, color_order=color_order)
    detector, sp, facerec = load_dlib_models()

    try:
        faces = _deduplicate_face_rectangles(
            list(detector(image_np, 1)) + list(detector(image_np, 2))
        )
        encodings = []

        for face in faces:
            shape = sp(image_np, face)
            face_descriptor = np.asarray(
                facerec.compute_face_descriptor(image_np, shape, 1),
                dtype=np.float64,
            )
            if face_descriptor.shape != (FACE_EMBEDDING_DIM,) or not np.isfinite(
                face_descriptor
            ).all():
                raise RuntimeError(
                    "Face recognition returned an invalid descriptor; "
                    f"expected {FACE_EMBEDDING_DIM} finite values."
                )
            encodings.append(face_descriptor)
    except Exception:
        logger.exception(
            "dlib face detection, landmark, or descriptor extraction failed in "
            "src.pipelines.face_pipeline.get_face_embeddings: "
            "shape=%s dtype=%s channels=%s",
            image_np.shape,
            image_np.dtype,
            image_np.shape[2],
        )
        raise

    return encodings


def _rectangle_iou(first, second):
    left = max(first.left(), second.left())
    top = max(first.top(), second.top())
    right = min(first.right(), second.right())
    bottom = min(first.bottom(), second.bottom())
    intersection = max(0, right - left + 1) * max(0, bottom - top + 1)
    first_area = max(0, first.right() - first.left() + 1) * max(
        0, first.bottom() - first.top() + 1
    )
    second_area = max(0, second.right() - second.left() + 1) * max(
        0, second.bottom() - second.top() + 1
    )
    union = first_area + second_area - intersection
    return intersection / union if union else 0.0


def _deduplicate_face_rectangles(rectangles, overlap_threshold=0.5):
    ordered = sorted(
        enumerate(rectangles),
        key=lambda item: (
            -(
                (item[1].right() - item[1].left() + 1)
                * (item[1].bottom() - item[1].top() + 1)
            )
            if all(
                callable(getattr(item[1], coordinate, None))
                for coordinate in ("left", "top", "right", "bottom")
            )
            else 0,
            item[0],
        ),
    )
    kept = []
    for _, rectangle in ordered:
        duplicate = False
        for existing in kept:
            has_coordinates = all(
                callable(getattr(rectangle, coordinate, None))
                and callable(getattr(existing, coordinate, None))
                for coordinate in ("left", "top", "right", "bottom")
            )
            if rectangle is existing or (
                has_coordinates
                and _rectangle_iou(rectangle, existing) >= overlap_threshold
            ):
                duplicate = True
                break
        if not duplicate:
            kept.append(rectangle)
    return kept


def _build_model_data(student_db):
    X = []
    y = []
    student_records = {}

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        student_id = student.get("student_id")

        if embedding and student_id is not None:
            stored_embedding = np.asarray(embedding, dtype=np.float64)
            if stored_embedding.shape != (FACE_EMBEDDING_DIM,) or not np.isfinite(
                stored_embedding
            ).all():
                logger.warning(
                    "Skipping a stored face embedding with an invalid shape "
                    "or non-finite values."
                )
                continue
            X.append(stored_embedding)
            y.append(student_id)
            student_records.setdefault(
                str(student_id),
                {"student_id": student_id, "name": student.get("name")},
            )

    if len(X) == 0:
        return None

    return {
        "X": X,
        "y": y,
        "students_by_id": student_records,
    }


@st.cache_resource
def get_trained_model():
    return _build_model_data(get_all_students())


def match_face_embedding(encoding, model_data):
    """Match against every stored template, rejecting multiple student candidates."""
    distances_by_student = {}

    for stored_embedding, student_id in zip(model_data["X"], model_data["y"]):
        distance = float(np.linalg.norm(stored_embedding - encoding))
        key = str(student_id)
        distances_by_student[key] = min(
            distance, distances_by_student.get(key, float("inf"))
        )

    ranked_candidates = sorted(
        distances_by_student.items(),
        key=lambda candidate: candidate[1],
    )
    matching_candidates = [
        candidate
        for candidate in ranked_candidates
        if candidate[1] <= FACE_MATCH_THRESHOLD
    ]
    result = {
        "status": "unknown",
        "student": None,
        "distance": ranked_candidates[0][1] if ranked_candidates else None,
        "best_distance": ranked_candidates[0][1] if ranked_candidates else None,
        "second_best_distance": (
            ranked_candidates[1][1] if len(ranked_candidates) > 1 else None
        ),
        "candidate_count": len(ranked_candidates),
        "candidate_record_count": len(model_data["X"]),
        "candidates_within_threshold": len(matching_candidates),
        "threshold": FACE_MATCH_THRESHOLD,
    }

    if len(matching_candidates) > 1:
        result["status"] = "ambiguous"
    elif len(matching_candidates) == 1:
        student_key, distance = matching_candidates[0]
        result["status"] = "matched"
        result["student"] = model_data["students_by_id"][student_key]
        result["distance"] = distance

    return result


def match_registered_face(encoding, student_records):
    """Check a new enrollment against a fresh set of database records."""
    model_data = _build_model_data(student_records)
    if model_data is None:
        result = {
            "status": "unknown",
            "student": None,
            "distance": None,
            "candidate_count": 0,
            "threshold": FACE_MATCH_THRESHOLD,
        }
    else:
        result = match_face_embedding(encoding, model_data)
    result["face_processing_id"] = uuid4().hex[:12]
    _log_face_match("registration_duplicate_check", result)
    return result


def refresh_face_model():
    get_trained_model.clear()
    model_data = get_trained_model()
    return model_data is not None


def _log_face_match(operation, result):
    log_method = logger.warning if result["status"] == "ambiguous" else logger.info
    student = result["student"]
    log_method(
        "Face recognition operation=%s face_processing_id=%s outcome=%s "
        "matched_student_id=%s distance=%s best_distance=%s "
        "second_best_distance=%s threshold=%s candidate_students=%s "
        "candidate_records=%s candidates_within_threshold=%s identity_source=%s",
        operation,
        result.get("face_processing_id"),
        result["status"],
        student["student_id"] if student else None,
        result["distance"],
        result.get("best_distance", result["distance"]),
        result.get("second_best_distance"),
        result["threshold"],
        result["candidate_count"],
        result.get("candidate_record_count", result["candidate_count"]),
        result.get("candidates_within_threshold", 0),
        "database_match" if student else "none",
    )


def identify_student(image_np, color_order="RGB"):
    """Identify one face and return the matched student identity from its DB row."""
    encodings = get_face_embeddings(image_np, color_order=color_order)
    if not encodings:
        result = {
            "status": "no_face",
            "student": None,
            "distance": None,
            "candidate_count": 0,
            "threshold": FACE_MATCH_THRESHOLD,
        }
        _log_face_match("student_sign_in", result)
        return result
    if len(encodings) != 1:
        result = {
            "status": "multiple_faces",
            "student": None,
            "distance": None,
            "candidate_count": 0,
            "threshold": FACE_MATCH_THRESHOLD,
        }
        _log_face_match("student_sign_in", result)
        return result

    get_trained_model.clear()
    model_data = get_trained_model()
    if model_data is None:
        result = {
            "status": "unknown",
            "student": None,
            "distance": None,
            "candidate_count": 0,
            "threshold": FACE_MATCH_THRESHOLD,
        }
    else:
        result = match_face_embedding(encodings[0], model_data)

    result["face_processing_id"] = uuid4().hex[:12]
    _log_face_match("student_sign_in", result)
    return result


def analyze_attendance_images(images):
    """Analyze each classroom photo independently and aggregate confident matches."""
    photos = []
    detected_students = {}
    unknown_faces = 0
    ambiguous_faces = 0
    total_faces = 0

    get_trained_model.clear()
    model_data = get_trained_model()
    if model_data is None:
        model_data = {"X": [], "y": [], "students_by_id": {}}

    for photo_number, image in enumerate(images, start=1):
        photo = {
            "photo_number": photo_number,
            "status": "processed",
            "face_count": 0,
            "unknown_faces": 0,
            "ambiguous_faces": 0,
            "error": None,
        }
        try:
            if hasattr(image, "convert"):
                image = np.asarray(image.convert("RGB"), dtype=np.uint8)
            encodings = get_face_embeddings(image)
        except Exception as exc:
            logger.exception(
                "Face attendance photo processing failed for photo_number=%s",
                photo_number,
            )
            photo["status"] = "failed"
            photo["error"] = type(exc).__name__
            photos.append(photo)
            continue

        photo["face_count"] = len(encodings)
        total_faces += len(encodings)
        for encoding in encodings:
            result = match_face_embedding(encoding, model_data)
            result["face_processing_id"] = uuid4().hex[:12]
            _log_face_match("attendance", result)
            if result["status"] == "matched":
                student = result["student"]
                student_key = str(student["student_id"])
                match = detected_students.setdefault(
                    student_key,
                    {
                        "student": student,
                        "photos": [],
                    },
                )
                photo_label = f"Photo {photo_number}"
                if photo_label not in match["photos"]:
                    match["photos"].append(photo_label)
            elif result["status"] == "ambiguous":
                photo["ambiguous_faces"] += 1
                ambiguous_faces += 1
            else:
                photo["unknown_faces"] += 1
                unknown_faces += 1
        photos.append(photo)

    processed_photos = sum(photo["status"] == "processed" for photo in photos)
    failed_photos = len(photos) - processed_photos
    return {
        "photos_uploaded": len(photos),
        "photos_processed": processed_photos,
        "photos_failed": failed_photos,
        "photos": photos,
        "faces_detected": total_faces,
        "unique_students_matched": len(detected_students),
        "unknown_faces": unknown_faces,
        "ambiguous_faces": ambiguous_faces,
        "detected_students": detected_students,
    }


def build_attendance_review_records(
    enrolled_students,
    analysis,
    subject_id,
    timestamp,
):
    results = []
    attendance_to_log = []

    for node in enrolled_students:
        student = node["students"]
        match = analysis["detected_students"].get(str(student["student_id"]), {})
        sources = match.get("photos", [])
        is_present = bool(sources)

        results.append(
            {
                "Name": student["name"],
                "ID": student["student_id"],
                "Source": ", ".join(sources) if is_present else "-",
                "Status": "✅ Present" if is_present else "❌ Absent",
            }
        )
        attendance_to_log.append(
            {
                "student_id": student["student_id"],
                "subject_id": subject_id,
                "timestamp": timestamp,
                "is_present": is_present,
            }
        )

    return results, attendance_to_log


def predict_attendance(class_image_np, color_order="RGB"):
    encodings = get_face_embeddings(
        class_image_np,
        color_order=color_order
    )

    model_data = get_trained_model()

    if not model_data:
        logger.info(
            "Face recognition operation=attendance outcome=no_candidates "
            "matched_student_id=None distance=None threshold=%s "
            "candidate_records=0 identity_source=none",
            FACE_MATCH_THRESHOLD,
        )
        return {}, [], len(encodings)

    detected_student = {}
    all_students = sorted(set(model_data["y"]), key=str)

    for encoding in encodings:
        result = match_face_embedding(encoding, model_data)
        result["face_processing_id"] = uuid4().hex[:12]
        _log_face_match("attendance", result)
        if result["status"] == "matched":
            student_id = result["student"]["student_id"]
            detected_student[student_id] = True

    return detected_student, all_students, len(encodings)
import logging

import numpy as np
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

logger = logging.getLogger(__name__)
FACE_EMBEDDING_DIM = 128


@st.cache_resource
def load_dlib_models():
    try:
        import dlib
    except ImportError as exc:
        raise RuntimeError(
            "Face recognition requires a compatible dlib installation. "
            "Check your Python environment and Windows security logs."
        ) from exc

    import face_recognition_models

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def prepare_dlib_image(image_np, color_order="RGB"):
    """Validate RGB/BGR pixel data without changing its left-to-right orientation."""
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

    if image.ndim == 3 and color_order.upper() == "BGR":
        image = image[:, :, ::-1]

    return np.ascontiguousarray(image, dtype=np.uint8)


def get_face_embeddings(image_np, color_order="RGB"):
    image_np = prepare_dlib_image(image_np, color_order=color_order)
    detector, sp, facerec = load_dlib_models()

    try:
        faces = detector(image_np, 1)
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
    except RuntimeError:
        logger.exception(
            "dlib face processing failed: shape=%s dtype=%s channels=%s",
            image_np.shape,
            image_np.dtype,
            image_np.shape[2] if image_np.ndim == 3 else 1,
        )
        raise

    return encodings


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

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

    if len(X) == 0:
        return None

    clf = None
    if len(set(y)) > 1:
        clf = SVC(
            kernel="linear",
            probability=True,
            class_weight="balanced"
        )

        try:
            clf.fit(X, y)
        except ValueError:
            return None

    return {"clf": clf, "X": X, "y": y}


def train_classifier():
    get_trained_model.clear()
    model_data = get_trained_model()
    return model_data is not None


def predict_attendance(class_image_np, color_order="RGB"):
    encodings = get_face_embeddings(
        class_image_np,
        color_order=color_order
    )

    detected_student = {}
    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(set(y_train))

    for encoding in encodings:
        # A single registered student does not require SVC prediction.
        if len(all_students) >= 2 and clf is not None:
            predicted_id = clf.predict([encoding])[0]
        elif len(all_students) == 1:
            predicted_id = all_students[0]
        else:
            continue

        # Compare against embeddings belonging to the predicted student.
        student_embeddings = [
            np.asarray(x, dtype=np.float64)
            for x, student_id in zip(X_train, y_train)
            if student_id == predicted_id
        ]

        if not student_embeddings:
            continue

        best_match_score = min(
            np.linalg.norm(embedding - encoding)
            for embedding in student_embeddings
        )

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)
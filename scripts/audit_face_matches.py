import argparse
import hashlib
import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path
from uuid import uuid4

import numpy as np
from PIL import Image

from src.database.config import supabase
from src.pipelines.face_pipeline import (
    FACE_EMBEDDING_DIM,
    FACE_MATCH_THRESHOLD,
    get_face_embeddings,
)

NEAR_IDENTICAL_DISTANCE = 0.1


def load_student_embeddings():
    rows = []
    start = 0
    page_size = 500

    while True:
        page = (
            supabase.table("students")
            .select("student_id, face_embedding")
            .range(start, start + page_size - 1)
            .execute()
            .data
        )
        rows.extend(page)
        if len(page) < page_size:
            break
        start += page_size

    return rows


def summarize_embeddings(rows):
    valid_rows = []
    missing_ids = []
    invalid_ids = []
    ids = Counter()
    hashes = defaultdict(list)

    for row in rows:
        student_id = row.get("student_id")
        ids[str(student_id)] += 1
        embedding = row.get("face_embedding")
        if embedding is None:
            missing_ids.append(student_id)
            continue

        try:
            vector = np.asarray(embedding, dtype=np.float64)
        except (TypeError, ValueError):
            invalid_ids.append(student_id)
            continue

        if (
            vector.shape != (FACE_EMBEDDING_DIM,)
            or not np.isfinite(vector).all()
        ):
            invalid_ids.append(student_id)
            continue

        vector = np.ascontiguousarray(vector)
        digest = hashlib.sha256(vector.tobytes()).hexdigest()
        hashes[digest].append(student_id)
        valid_rows.append((student_id, vector))

    duplicate_id_counts = {
        student_id: count
        for student_id, count in ids.items()
        if count > 1
    }
    identical_embedding_groups = [
        sorted(group, key=str)
        for group in hashes.values()
        if len(group) > 1
    ]

    return (
        valid_rows,
        missing_ids,
        invalid_ids,
        duplicate_id_counts,
        identical_embedding_groups,
    )


def find_close_student_pairs(rows):
    pairs = []
    embeddings_by_id = defaultdict(list)
    original_ids = {}
    for student_id, embedding in rows:
        key = str(student_id)
        embeddings_by_id[key].append(embedding)
        original_ids[key] = student_id

    student_ids = list(embeddings_by_id)
    for index, first_key in enumerate(student_ids):
        for second_key in student_ids[index + 1 :]:
            distance = min(
                float(np.linalg.norm(first_embedding - second_embedding))
                for first_embedding in embeddings_by_id[first_key]
                for second_embedding in embeddings_by_id[second_key]
            )
            if distance <= FACE_MATCH_THRESHOLD:
                pairs.append(
                    (original_ids[first_key], original_ids[second_key], distance)
                )
    return sorted(pairs, key=lambda pair: pair[2])


def analyze_face(image_path, rows):
    with Image.open(image_path) as image:
        rgb_image = np.asarray(image.convert("RGB"), dtype=np.uint8)
    encodings = get_face_embeddings(rgb_image)
    results = []
    for encoding in encodings:
        embeddings_by_id = defaultdict(list)
        for student_id, embedding in rows:
            embeddings_by_id[str(student_id)].append((student_id, embedding))

        candidates = []
        for student_key, records in embeddings_by_id.items():
            student_id = records[0][0]
            distance = min(
                float(np.linalg.norm(embedding - encoding))
                for _, embedding in records
            )
            candidates.append(
                {
                    "student_id": student_id,
                    "distance": distance,
                    "record_count": len(records),
                    "embeddings": [embedding for _, embedding in records],
                }
            )
        candidates.sort(key=lambda candidate: candidate["distance"])

        exact_pairs = []
        near_pairs = []
        for index, first in enumerate(candidates):
            for second in candidates[index + 1 :]:
                distance = min(
                    float(np.linalg.norm(first_embedding - second_embedding))
                    for first_embedding in first["embeddings"]
                    for second_embedding in second["embeddings"]
                )
                pair = (first["student_id"], second["student_id"], distance)
                if distance == 0.0:
                    exact_pairs.append(pair)
                elif distance <= NEAR_IDENTICAL_DISTANCE:
                    near_pairs.append(pair)

        matches = [
            candidate
            for candidate in candidates
            if candidate["distance"] <= FACE_MATCH_THRESHOLD
        ]
        results.append(
            {
                "face_processing_id": uuid4().hex[:12],
                "candidates": candidates,
                "best_distance": candidates[0]["distance"] if candidates else None,
                "second_best_distance": (
                    candidates[1]["distance"] if len(candidates) > 1 else None
                ),
                "candidates_within_threshold": len(matches),
                "status": (
                    "ambiguous"
                    if len(matches) > 1
                    else ("matched" if len(matches) == 1 else "unknown")
                ),
                "exact_embedding_pairs": exact_pairs,
                "near_identical_embedding_pairs": near_pairs,
            }
        )
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Privately compare one face image to registered Supabase embeddings. "
            "Run only as an authorized SnapClass administrator."
        ),
        epilog=(
            "Example: python -m scripts.audit_face_matches "
            '--image "C:\\private\\sign-in-capture.jpg" --authorized-admin'
        ),
    )
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument(
        "--authorized-admin",
        action="store_true",
        help="Confirm you are authorized to inspect SnapClass biometric records.",
    )
    args = parser.parse_args(argv)

    if not args.authorized_admin:
        parser.error("this diagnostic is restricted to authorized administrators")
    if not args.image.is_file():
        parser.error("the specified image file does not exist")

    logging.disable(logging.CRITICAL)
    try:
        records = load_student_embeddings()
        (
            embeddings,
            missing_ids,
            invalid_ids,
            duplicate_ids,
            identical_groups,
        ) = (
            summarize_embeddings(records)
        )
        close_pairs = find_close_student_pairs(embeddings)
        faces = analyze_face(args.image, embeddings)
    except Exception as exc:
        print(
            "Diagnostic failed. No identity report was generated "
            f"({type(exc).__name__}).",
            file=sys.stderr,
        )
        return 1

    print("SnapClass private face-match diagnostic")
    print(f"Threshold: {FACE_MATCH_THRESHOLD:.3f}")
    print(f"Student records fetched: {len(records)}")
    print(f"Valid face embeddings: {len(embeddings)}")
    print(f"Missing embedding student IDs: {missing_ids}")
    print(f"Invalid embedding student IDs: {invalid_ids}")
    print(f"Repeated student ID records: {duplicate_ids}")
    print(f"Identical embedding student ID groups: {identical_groups}")
    print(
        "Near-identical embedding distance threshold "
        f"(diagnostic only): {NEAR_IDENTICAL_DISTANCE:.3f}"
    )
    print(
        "Cross-student embedding pairs within threshold "
        f"(manual review only): {len(close_pairs)}"
    )
    for first_id, second_id, distance in close_pairs:
        print(
            f"student_id_pair=({first_id}, {second_id}) "
            f"embedding_distance={distance:.6f}"
        )
    if not faces:
        print("No face was detected in the diagnostic image.")
    for face in faces:
        print(
            f"face_processing_id={face['face_processing_id']} "
            f"outcome={face['status']} "
            f"best_distance={face['best_distance']} "
            f"second_best_distance={face['second_best_distance']} "
            f"candidate_students={len(face['candidates'])} "
            f"candidates_within_threshold={face['candidates_within_threshold']} "
            f"threshold={FACE_MATCH_THRESHOLD:.3f}"
        )
        for candidate in face["candidates"]:
            print(
                f"  student_id={candidate['student_id']} "
                f"distance={candidate['distance']:.6f} "
                f"records_for_student_id={candidate['record_count']}"
            )
        if face["exact_embedding_pairs"]:
            print(
                "  exact candidate embedding pairs:",
                face["exact_embedding_pairs"],
            )
        if face["near_identical_embedding_pairs"]:
            print(
                "  near-identical candidate embedding pairs "
                f"(<= {NEAR_IDENTICAL_DISTANCE:.3f}; review only):",
                face["near_identical_embedding_pairs"],
            )
        if face["status"] == "ambiguous":
            print("  Outcome: ambiguous; continue rejecting sign-in.")
        elif face["status"] == "matched":
            best_match = next(
                candidate
                for candidate in face["candidates"]
                if candidate["distance"] <= FACE_MATCH_THRESHOLD
            )
            print(
                "  Outcome: one candidate, "
                f"student_id={best_match['student_id']}."
            )
        else:
            print("  Outcome: unknown face; no profile matched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

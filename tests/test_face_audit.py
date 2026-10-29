import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PIL import Image

from scripts import audit_face_matches
from src.pipelines import face_pipeline


class FaceAuditTests(unittest.TestCase):
    def test_summarize_detects_duplicate_embeddings_without_returning_values(self):
        first = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        second = np.ones(face_pipeline.FACE_EMBEDDING_DIM)
        rows = [
            {"student_id": 11, "face_embedding": first.tolist()},
            {"student_id": 12, "face_embedding": first.tolist()},
            {"student_id": 13, "face_embedding": second.tolist()},
            {"student_id": 13, "face_embedding": second.tolist()},
        ]

        valid, missing, invalid, duplicate_ids, identical_groups = (
            audit_face_matches.summarize_embeddings(rows)
        )

        self.assertEqual(len(valid), 4)
        self.assertEqual(missing, [])
        self.assertEqual(invalid, [])
        self.assertEqual(duplicate_ids, {"13": 2})
        self.assertEqual(identical_groups, [[11, 12], [13, 13]])

    def test_summarize_reports_missing_and_invalid_embeddings_by_id(self):
        rows = [
            {"student_id": 11, "face_embedding": None},
            {"student_id": 12, "face_embedding": [float("nan")] * 128},
        ]

        valid, missing, invalid, duplicate_ids, identical_groups = (
            audit_face_matches.summarize_embeddings(rows)
        )

        self.assertEqual(valid, [])
        self.assertEqual(missing, [11])
        self.assertEqual(invalid, [12])
        self.assertEqual(duplicate_ids, {})
        self.assertEqual(identical_groups, [])

    def test_close_pair_report_includes_distinct_ids_under_threshold(self):
        first = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        second = first.copy()
        second[0] = 0.5
        same_student = first.copy()
        same_student[0] = 0.1

        pairs = audit_face_matches.find_close_student_pairs(
            [(11, first), (12, second), (11, same_student)]
        )

        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][:2], (11, 12))
        self.assertAlmostEqual(pairs[0][2], 0.4)

    def test_captured_face_report_ranks_candidates_and_counts_threshold_matches(self):
        first = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        second = first.copy()
        second[0] = 0.2
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "face.png"
            Image.new("RGB", (4, 4)).save(image_path)
            with patch.object(
                audit_face_matches,
                "get_face_embeddings",
                return_value=[np.zeros(face_pipeline.FACE_EMBEDDING_DIM)],
            ):
                faces = audit_face_matches.analyze_face(
                    image_path, [(11, first), (12, second)]
                )

        self.assertEqual(len(faces), 1)
        face = faces[0]
        self.assertEqual(face["status"], "ambiguous")
        self.assertEqual(face["best_distance"], 0.0)
        self.assertAlmostEqual(face["second_best_distance"], 0.2)
        self.assertEqual(face["candidates_within_threshold"], 2)
        self.assertEqual(
            [candidate["student_id"] for candidate in face["candidates"]],
            [11, 12],
        )
        self.assertEqual(face["candidates"][0]["record_count"], 1)
        self.assertTrue(face["face_processing_id"])

    def test_unique_candidate_is_accepted_only_with_one_id_within_threshold(self):
        first = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        outside = first.copy()
        outside[0] = 0.8
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "face.png"
            Image.new("RGB", (4, 4)).save(image_path)
            with patch.object(
                audit_face_matches,
                "get_face_embeddings",
                return_value=[first.copy()],
            ):
                faces = audit_face_matches.analyze_face(
                    image_path,
                    [(11, first), (12, outside)],
                )

        self.assertEqual(faces[0]["status"], "matched")
        self.assertEqual(faces[0]["candidates_within_threshold"], 1)
        self.assertEqual(faces[0]["candidates"][0]["student_id"], 11)

    def test_diagnostic_assigns_distinct_opaque_ids_for_each_detected_face(self):
        first = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        second = np.ones(face_pipeline.FACE_EMBEDDING_DIM)
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "group.png"
            Image.new("RGB", (4, 4)).save(image_path)
            with patch.object(
                audit_face_matches,
                "get_face_embeddings",
                return_value=[first.copy(), second.copy()],
            ):
                faces = audit_face_matches.analyze_face(
                    image_path,
                    [(11, first), (12, second)],
                )

        self.assertEqual(len(faces), 2)
        self.assertNotEqual(
            faces[0]["face_processing_id"],
            faces[1]["face_processing_id"],
        )

    def test_identical_embeddings_are_reported_for_ambiguous_candidates(self):
        duplicate = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "face.png"
            Image.new("RGB", (4, 4)).save(image_path)
            with patch.object(
                audit_face_matches,
                "get_face_embeddings",
                return_value=[duplicate.copy()],
            ):
                faces = audit_face_matches.analyze_face(
                    image_path,
                    [(11, duplicate), (12, duplicate.copy())],
                )

        self.assertEqual(faces[0]["status"], "ambiguous")
        self.assertEqual(faces[0]["candidates_within_threshold"], 2)
        self.assertEqual(
            faces[0]["exact_embedding_pairs"],
            [(11, 12, 0.0)],
        )

    def test_unknown_face_has_no_candidates_within_threshold(self):
        registered = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        unknown = np.ones(face_pipeline.FACE_EMBEDDING_DIM)
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "face.png"
            Image.new("RGB", (4, 4)).save(image_path)
            with patch.object(
                audit_face_matches,
                "get_face_embeddings",
                return_value=[unknown],
            ):
                faces = audit_face_matches.analyze_face(
                    image_path, [(11, registered)]
                )

                self.assertEqual(len(faces), 1)
                self.assertEqual(faces[0]["status"], "unknown")
                self.assertEqual(faces[0]["candidates_within_threshold"], 0)


if __name__ == "__main__":
    unittest.main()

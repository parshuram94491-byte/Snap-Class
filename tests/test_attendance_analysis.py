import io
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

from src.components.dialog_add_photo import decode_photo
from src.pipelines import face_pipeline


def _image(marker):
    return np.full((2, 2, 3), marker, dtype=np.uint8)


class AttendanceAnalysisTests(unittest.TestCase):
    def setUp(self):
        first = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        second = np.zeros(face_pipeline.FACE_EMBEDDING_DIM)
        second[0] = 1.0
        self.records = [
            {
                "student_id": 11,
                "name": "Student One",
                "face_embedding": first.tolist(),
            },
            {
                "student_id": 22,
                "name": "Student Two",
                "face_embedding": second.tolist(),
            },
        ]
        self.model = face_pipeline._build_model_data(self.records)
        self.first_face = first.copy()
        self.first_face[0] = 0.1
        self.second_face = second.copy()
        self.second_face[0] = 0.9
        self.unknown_face = np.ones(face_pipeline.FACE_EMBEDDING_DIM)
        self.ambiguous_face = first.copy()
        self.ambiguous_face[0] = 0.5

    def _analyze(self, photos, encodings_by_marker):
        def embeddings(image, **_kwargs):
            marker = int(image[0, 0, 0])
            value = encodings_by_marker[marker]
            if isinstance(value, Exception):
                raise value
            return value

        with patch.object(
            face_pipeline, "get_trained_model", return_value=self.model
        ):
            with patch.object(
                face_pipeline, "get_face_embeddings", side_effect=embeddings
            ):
                return face_pipeline.analyze_attendance_images(photos)

    def test_one_photo_matches_multiple_registered_students(self):
        analysis = self._analyze(
            [_image(1)],
            {1: [self.first_face, self.second_face]},
        )

        self.assertEqual(analysis["photos_uploaded"], 1)
        self.assertEqual(analysis["photos_processed"], 1)
        self.assertEqual(analysis["photos"][0]["face_count"], 2)
        self.assertEqual(analysis["unique_students_matched"], 2)
        self.assertEqual(
            set(analysis["detected_students"]),
            {"11", "22"},
        )

    def test_overlapping_groups_across_photos_deduplicate_students_and_track_sources(self):
        analysis = self._analyze(
            [_image(1), _image(2), _image(3)],
            {
                1: [self.first_face, self.second_face],
                2: [self.second_face],
                3: [self.first_face],
            },
        )

        self.assertEqual(analysis["photos_uploaded"], 3)
        self.assertEqual(analysis["photos_processed"], 3)
        self.assertEqual(analysis["unique_students_matched"], 2)
        self.assertEqual(
            analysis["detected_students"]["11"]["photos"],
            ["Photo 1", "Photo 3"],
        )
        self.assertEqual(
            analysis["detected_students"]["22"]["photos"],
            ["Photo 1", "Photo 2"],
        )

    def test_unknown_and_ambiguous_faces_are_not_matched(self):
        analysis = self._analyze(
            [_image(1)],
            {1: [self.unknown_face, self.ambiguous_face]},
        )

        self.assertEqual(analysis["unique_students_matched"], 0)
        self.assertEqual(analysis["unknown_faces"], 1)
        self.assertEqual(analysis["ambiguous_faces"], 1)
        self.assertEqual(analysis["detected_students"], {})

    def test_image_failure_does_not_abort_remaining_photos(self):
        with self.assertLogs(face_pipeline.logger, level="ERROR"):
            analysis = self._analyze(
                [_image(1), _image(2)],
                {
                    1: [self.first_face],
                    2: OSError("invalid photo"),
                },
            )

        self.assertEqual(analysis["photos_uploaded"], 2)
        self.assertEqual(analysis["photos_processed"], 1)
        self.assertEqual(analysis["photos_failed"], 1)
        self.assertEqual(analysis["photos"][1]["status"], "failed")
        self.assertEqual(analysis["unique_students_matched"], 1)

    def test_photo_with_no_detectable_faces_is_processed(self):
        analysis = self._analyze([_image(1)], {1: []})

        self.assertEqual(analysis["photos_processed"], 1)
        self.assertEqual(analysis["photos"][0]["face_count"], 0)
        self.assertEqual(analysis["faces_detected"], 0)

    def test_review_records_deduplicate_matches_and_keep_absent_students_absent(self):
        analysis = self._analyze(
            [_image(1), _image(2)],
            {
                1: [self.first_face, self.second_face],
                2: [self.second_face, self.unknown_face],
            },
        )
        enrolled = [
            {"students": {"student_id": 11, "name": "Student One"}},
            {"students": {"student_id": 22, "name": "Student Two"}},
            {"students": {"student_id": 33, "name": "Student Three"}},
        ]

        rows, logs = face_pipeline.build_attendance_review_records(
            enrolled,
            analysis,
            subject_id=7,
            timestamp="2026-10-29T12:00:00",
        )

        self.assertEqual([row["ID"] for row in rows], [11, 22, 33])
        self.assertEqual([log["is_present"] for log in logs], [True, True, False])
        self.assertEqual(sum(log["is_present"] for log in logs), 2)
        self.assertEqual(sum(not log["is_present"] for log in logs), 1)
        self.assertEqual(rows[1]["Source"], "Photo 1, Photo 2")
        self.assertEqual(rows[2]["Source"], "-")

    def test_uploaded_image_decoder_returns_loaded_rgb_or_raises(self):
        image_buffer = io.BytesIO()
        Image.new("RGBA", (2, 2), (10, 20, 30, 40)).save(image_buffer, format="PNG")
        image_buffer.seek(0)

        decoded = decode_photo(image_buffer)

        self.assertEqual(decoded.mode, "RGB")
        self.assertEqual(decoded.getpixel((0, 0)), (10, 20, 30))
        with self.assertRaises(Exception):
            decode_photo(io.BytesIO(b"not an image"))


if __name__ == "__main__":
    unittest.main()

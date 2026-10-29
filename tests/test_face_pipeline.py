import unittest
from unittest.mock import patch

import numpy as np

from src.pipelines import face_pipeline


class FakeDetector:
    def __init__(self, faces):
        self.faces = faces
        self.image = None

    def __call__(self, image, upsample):
        self.image = image
        return self.faces


class FakeShapePredictor:
    def __init__(self):
        self.image = None

    def __call__(self, image, face):
        self.image = image
        return face


class FakeFaceRecognizer:
    def __init__(self):
        self.image = None

    def compute_face_descriptor(self, image, shape, num_jitters):
        self.image = image
        return np.zeros(face_pipeline.FACE_EMBEDDING_DIM)


class FakeRectangle:
    def __init__(self, left, top, right, bottom):
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom

    def left(self):
        return self._left

    def top(self):
        return self._top

    def right(self):
        return self._right

    def bottom(self):
        return self._bottom


class PrepareDlibImageTests(unittest.TestCase):
    def test_rgb_uint8_is_preserved(self):
        image = np.full((3, 5, 3), 17, dtype=np.uint8)

        prepared = face_pipeline.prepare_dlib_image(image)

        np.testing.assert_array_equal(prepared, image)
        self.assertEqual(prepared.dtype, np.uint8)
        self.assertTrue(prepared.flags.c_contiguous)

    def test_rgb_orientation_is_preserved(self):
        image = np.zeros((1, 2, 3), dtype=np.uint8)
        image[0, 0] = (255, 0, 0)
        image[0, 1] = (0, 0, 255)

        prepared = face_pipeline.prepare_dlib_image(image)

        np.testing.assert_array_equal(prepared, image)
        self.assertTrue(np.array_equal(prepared[0, 0], (255, 0, 0)))
        self.assertTrue(np.array_equal(prepared[0, 1], (0, 0, 255)))

    def test_grayscale_uint8_is_converted_to_three_rgb_channels(self):
        image = np.arange(15, dtype=np.uint8).reshape(3, 5)

        prepared = face_pipeline.prepare_dlib_image(image)

        expected = np.repeat(image[:, :, np.newaxis], 3, axis=2)
        np.testing.assert_array_equal(prepared, expected)
        self.assertEqual(prepared.shape, (3, 5, 3))
        self.assertEqual(prepared.dtype, np.uint8)

    def test_detector_failure_is_logged_with_traceback_and_reraised(self):
        image = np.zeros((20, 30, 3), dtype=np.uint8)

        with patch.object(
            face_pipeline,
            "load_dlib_models",
            return_value=(
                lambda *_args: (_ for _ in ()).throw(OSError("detector test failure")),
                FakeShapePredictor(),
                FakeFaceRecognizer(),
            ),
        ):
            with self.assertLogs(face_pipeline.logger, level="ERROR") as captured:
                with self.assertRaisesRegex(OSError, "detector test failure"):
                    face_pipeline.get_face_embeddings(image)

        self.assertIn(
            "src.pipelines.face_pipeline.get_face_embeddings",
            captured.output[0],
        )
        self.assertIn("Traceback (most recent call last)", captured.output[0])

    def test_rgba_drops_alpha_without_reordering_rgb(self):
        image = np.array([[[11, 22, 33, 44]]], dtype=np.uint8)

        prepared = face_pipeline.prepare_dlib_image(image)

        np.testing.assert_array_equal(prepared, [[[11, 22, 33]]])

    def test_confirmed_bgr_is_converted_to_rgb(self):
        image = np.array([[[3, 2, 1]]], dtype=np.uint8)

        prepared = face_pipeline.prepare_dlib_image(image, color_order="BGR")

        np.testing.assert_array_equal(prepared, [[[1, 2, 3]]])

    def test_normalized_float_is_scaled_from_its_actual_range(self):
        image = np.array([[[0.0, 0.5, 1.0]]], dtype=np.float32)

        prepared = face_pipeline.prepare_dlib_image(image)

        np.testing.assert_array_equal(prepared, [[[0, 128, 255]]])

    def test_float_intensity_values_are_not_rescaled(self):
        image = np.array([[[0.0, 128.0, 255.0]]], dtype=np.float32)

        prepared = face_pipeline.prepare_dlib_image(image)

        np.testing.assert_array_equal(prepared, [[[0, 128, 255]]])

    def test_rejects_unsupported_channel_count(self):
        with self.assertRaisesRegex(ValueError, "expected RGB"):
            face_pipeline.prepare_dlib_image(np.zeros((2, 3, 2), dtype=np.uint8))

    def test_rejects_empty_image(self):
        with self.assertRaisesRegex(ValueError, "empty image"):
            face_pipeline.prepare_dlib_image(np.zeros((0, 3, 3), dtype=np.uint8))

    def test_rejects_invalid_dimensions(self):
        for image in (
            np.zeros((3,), dtype=np.uint8),
            np.zeros((2, 3, 4, 1), dtype=np.uint8),
        ):
            with self.subTest(shape=image.shape):
                with self.assertRaisesRegex(ValueError, "dimensions"):
                    face_pipeline.prepare_dlib_image(image)

    def test_rejects_nan_and_infinite_pixels(self):
        for value in (np.nan, np.inf, -np.inf):
            image = np.full((2, 2, 3), value, dtype=np.float32)
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "NaN or infinite"):
                    face_pipeline.prepare_dlib_image(image)

    def test_rejects_out_of_range_float_pixels_instead_of_clipping(self):
        image = np.array([[[-1.0, 0.0, 256.0]]], dtype=np.float32)

        with self.assertRaisesRegex(ValueError, r"\[0, 1\].*\[0, 255\]"):
            face_pipeline.prepare_dlib_image(image)


class FacePipelineTests(unittest.TestCase):
    def tearDown(self):
        face_pipeline.get_trained_model.clear()
        face_pipeline.load_dlib_models.clear()

    def test_no_detected_faces_returns_no_embeddings(self):
        detector = FakeDetector([])
        shape_predictor = FakeShapePredictor()
        recognizer = FakeFaceRecognizer()
        image = np.zeros((20, 30, 3), dtype=np.uint8)

        with patch.object(
            face_pipeline,
            "load_dlib_models",
            return_value=(detector, shape_predictor, recognizer),
        ):
            encodings = face_pipeline.get_face_embeddings(image)

        self.assertEqual(encodings, [])
        self.assertEqual(detector.image.shape, image.shape)
        self.assertIsNone(shape_predictor.image)
        self.assertIsNone(recognizer.image)
        with patch.object(face_pipeline, "get_face_embeddings", return_value=[]):
            with patch.object(face_pipeline, "get_trained_model", return_value=None):
                self.assertEqual(
                    face_pipeline.predict_attendance(image),
                    ({}, [], 0),
                )

    def test_descriptor_extraction_uses_same_prepared_image_and_128_values(self):
        detector = FakeDetector(["face"])
        shape_predictor = FakeShapePredictor()
        recognizer = FakeFaceRecognizer()
        image = np.zeros((20, 30, 4), dtype=np.uint8)

        with patch.object(
            face_pipeline,
            "load_dlib_models",
            return_value=(detector, shape_predictor, recognizer),
        ):
            encodings = face_pipeline.get_face_embeddings(image)

        self.assertEqual(encodings[0].shape, (128,))
        self.assertIs(detector.image, shape_predictor.image)
        self.assertIs(detector.image, recognizer.image)
        self.assertEqual(detector.image.shape, (20, 30, 3))

    def test_multiscale_detection_keeps_small_faces_and_suppresses_duplicate_boxes(self):
        large_one = FakeRectangle(10, 10, 30, 30)
        large_two = FakeRectangle(50, 10, 70, 30)
        small_face = FakeRectangle(90, 10, 98, 18)
        repeated_one = FakeRectangle(11, 11, 30, 30)

        class MultiScaleDetector:
            def __init__(self):
                self.upsamples = []

            def __call__(self, _image, upsample):
                self.upsamples.append(upsample)
                return {
                    1: [large_one, large_two],
                    2: [repeated_one, large_two, small_face],
                }[upsample]

        class CountingRecognizer(FakeFaceRecognizer):
            def __init__(self):
                super().__init__()
                self.descriptor_count = 0

            def compute_face_descriptor(self, image, shape, num_jitters):
                self.descriptor_count += 1
                return super().compute_face_descriptor(image, shape, num_jitters)

        detector = MultiScaleDetector()
        recognizer = CountingRecognizer()
        image = np.zeros((120, 120, 3), dtype=np.uint8)
        with patch.object(
            face_pipeline,
            "load_dlib_models",
            return_value=(detector, FakeShapePredictor(), recognizer),
        ):
            encodings = face_pipeline.get_face_embeddings(image)

        self.assertEqual(detector.upsamples, [1, 2])
        self.assertEqual(len(encodings), 3)
        self.assertEqual(recognizer.descriptor_count, 3)

    def test_empty_student_database_is_safe(self):
        with patch.object(face_pipeline, "get_all_students", return_value=[]):
            model = face_pipeline.get_trained_model()

        self.assertIsNone(model)

    def test_single_student_is_matched_and_unknown_is_rejected(self):
        known = np.zeros(128)
        near_known = known.copy()
        near_known[0] = 0.1
        unknown = known.copy()
        unknown[0] = 1.0
        with patch.object(
            face_pipeline,
            "get_all_students",
            return_value=[{"student_id": 101, "face_embedding": known.tolist()}],
        ):
            model = face_pipeline.get_trained_model()

        with patch.object(face_pipeline, "get_trained_model", return_value=model):
            with patch.object(
                face_pipeline, "get_face_embeddings", return_value=[near_known]
            ):
                self.assertEqual(
                    face_pipeline.predict_attendance(np.zeros((2, 2, 3)))[0],
                    {101: True},
                )
            with patch.object(
                face_pipeline, "get_face_embeddings", return_value=[unknown]
            ):
                self.assertEqual(
                    face_pipeline.predict_attendance(np.zeros((2, 2, 3)))[0],
                    {},
                )

    def test_multiple_students_match_correctly_and_unknown_is_rejected(self):
        first = np.zeros(128)
        second = np.zeros(128)
        second[0] = 2.0
        students = [
            {"student_id": 101, "face_embedding": first.tolist()},
            {"student_id": 202, "face_embedding": second.tolist()},
        ]
        with patch.object(face_pipeline, "get_all_students", return_value=students):
            model = face_pipeline.get_trained_model()

        first_query = first.copy()
        first_query[0] = 0.1
        second_query = second.copy()
        second_query[0] = 1.9
        unknown_query = first.copy()
        unknown_query[0] = 1.0
        with patch.object(face_pipeline, "get_trained_model", return_value=model):
            for query, expected in (
                (first_query, {101: True}),
                (second_query, {202: True}),
                (unknown_query, {}),
            ):
                with self.subTest(expected=expected):
                    with patch.object(
                        face_pipeline,
                        "get_face_embeddings",
                        return_value=[query],
                    ):
                        detected, student_ids, face_count = (
                            face_pipeline.predict_attendance(
                                np.zeros((2, 2, 3), dtype=np.uint8)
                            )
                        )
                    self.assertEqual(detected, expected)
                    self.assertEqual(student_ids, [101, 202])
                    self.assertEqual(face_count, 1)

    def test_registered_parshuram_face_resolves_to_parshuram_record(self):
        first = np.zeros(128)
        second = np.ones(128)
        students = [
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": first.tolist(),
            },
            {
                "student_id": 202,
                "name": "Friend",
                "face_embedding": second.tolist(),
            },
        ]
        query = first.copy()
        query[0] = 0.1

        with patch.object(face_pipeline, "get_all_students", return_value=students):
            with patch.object(
                face_pipeline, "get_face_embeddings", return_value=[query]
            ):
                match = face_pipeline.identify_student(
                    np.zeros((2, 2, 3), dtype=np.uint8)
                )

        self.assertEqual(match["status"], "matched")
        self.assertEqual(match["student"], {"student_id": 101, "name": "Parshuram"})

    def test_second_students_face_resolves_to_second_students_record(self):
        first = np.zeros(128)
        second = np.zeros(128)
        second[0] = 2.0
        students = [
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": first.tolist(),
            },
            {
                "student_id": 202,
                "name": "Friend",
                "face_embedding": second.tolist(),
            },
        ]
        query = second.copy()
        query[0] = 1.9

        with patch.object(face_pipeline, "get_all_students", return_value=students):
            with patch.object(
                face_pipeline, "get_face_embeddings", return_value=[query]
            ):
                match = face_pipeline.identify_student(
                    np.zeros((2, 2, 3), dtype=np.uint8)
                )

        self.assertEqual(match["status"], "matched")
        self.assertEqual(match["student"]["student_id"], 202)
        self.assertEqual(match["student"]["name"], "Friend")

    def test_display_identity_is_from_the_matched_student_record(self):
        first = np.zeros(128)
        second = np.ones(128)
        students = [
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": first.tolist(),
            },
            {
                "student_id": 202,
                "name": "Friend",
                "face_embedding": second.tolist(),
            },
        ]

        result = face_pipeline.match_registered_face(first, students)

        self.assertEqual(result["student"]["student_id"], 101)
        self.assertEqual(result["student"]["name"], "Parshuram")
        self.assertEqual(result["student"], {
            "student_id": students[0]["student_id"],
            "name": students[0]["name"],
        })

    def test_ambiguous_match_does_not_return_an_identity(self):
        first = np.zeros(128)
        second = first.copy()
        second[0] = 0.2
        students = [
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": first.tolist(),
            },
            {
                "student_id": 202,
                "name": "Friend",
                "face_embedding": second.tolist(),
            },
        ]
        query = first.copy()
        query[0] = 0.1

        result = face_pipeline.match_registered_face(query, students)

        self.assertEqual(result["status"], "ambiguous")
        self.assertIsNone(result["student"])
        self.assertEqual(result["candidate_count"], 2)

    def test_match_result_ranks_distinct_students_and_counts_threshold_matches(self):
        first = np.zeros(128)
        second = first.copy()
        second[0] = 0.3
        third = first.copy()
        third[0] = 1.2
        model_data = face_pipeline._build_model_data(
            [
                {"student_id": 101, "name": "First", "face_embedding": first.tolist()},
                {"student_id": 202, "name": "Second", "face_embedding": second.tolist()},
                {"student_id": 303, "name": "Third", "face_embedding": third.tolist()},
            ]
        )

        result = face_pipeline.match_face_embedding(first, model_data)

        self.assertEqual(result["status"], "ambiguous")
        self.assertEqual(result["candidate_count"], 3)
        self.assertEqual(result["candidate_record_count"], 3)
        self.assertEqual(result["candidates_within_threshold"], 2)
        self.assertEqual(result["best_distance"], 0.0)
        self.assertAlmostEqual(result["second_best_distance"], 0.3)

    def test_repeated_records_for_same_student_count_as_one_candidate(self):
        first = np.zeros(128)
        second = first.copy()
        second[0] = 0.2
        model_data = face_pipeline._build_model_data(
            [
                {"student_id": 101, "name": "First", "face_embedding": first.tolist()},
                {"student_id": 101, "name": "First", "face_embedding": second.tolist()},
            ]
        )

        result = face_pipeline.match_face_embedding(first, model_data)

        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["candidate_count"], 1)
        self.assertEqual(result["candidate_record_count"], 2)
        self.assertEqual(result["candidates_within_threshold"], 1)
        self.assertEqual(result["student"]["student_id"], 101)

    def test_multiple_embeddings_for_one_student_do_not_create_identity_ambiguity(self):
        first = np.zeros(128)
        second = np.ones(128)
        query = first.copy()
        query[0] = 0.1
        student_records = [
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": first.tolist(),
            },
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": second.tolist(),
            },
        ]

        result = face_pipeline.match_registered_face(query, student_records)

        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["student"]["student_id"], 101)
        self.assertEqual(result["student"]["name"], "Parshuram")

    def test_failed_database_lookup_raises_without_fallback_identity(self):
        query = np.zeros(128)
        with patch.object(
            face_pipeline, "get_all_students", side_effect=RuntimeError("database down")
        ):
            with patch.object(
                face_pipeline, "get_face_embeddings", return_value=[query]
            ):
                with self.assertRaisesRegex(RuntimeError, "database down"):
                    face_pipeline.identify_student(
                        np.zeros((2, 2, 3), dtype=np.uint8)
                    )

    def test_duplicate_registration_match_is_not_unknown(self):
        known = np.zeros(128)
        query = known.copy()
        query[0] = 0.1
        students = [
            {
                "student_id": 101,
                "name": "Parshuram",
                "face_embedding": known.tolist(),
            }
        ]

        result = face_pipeline.match_registered_face(query, students)

        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["student"]["student_id"], 101)

    def test_actual_dlib_detects_on_valid_uint8_image_when_models_available(self):
        try:
            import dlib  # noqa: F401
            import face_recognition_models
        except ImportError as exc:
            self.skipTest(f"dlib/model package unavailable: {exc}")

        model_paths = (
            face_recognition_models.pose_predictor_model_location(),
            face_recognition_models.face_recognition_model_location(),
        )
        try:
            for model_path in model_paths:
                with open(model_path, "rb"):
                    pass
        except OSError as exc:
            self.skipTest(f"face model files unavailable: {exc}")

        detector, shape_predictor, face_recognizer = (
            face_pipeline.load_dlib_models()
        )
        image = np.zeros((256, 256, 3), dtype=np.uint8)
        self.assertEqual(len(detector(image, 1)), 0)

        def detector_with_test_face(prepared_image, upsample):
            return [dlib.rectangle(20, 20, 230, 230)]

        with patch.object(
            face_pipeline,
            "load_dlib_models",
            return_value=(
                detector_with_test_face,
                shape_predictor,
                face_recognizer,
            ),
        ):
            descriptors = face_pipeline.get_face_embeddings(image)

        self.assertEqual(len(descriptors), 1)
        self.assertEqual(descriptors[0].shape, (face_pipeline.FACE_EMBEDDING_DIM,))
        self.assertTrue(np.isfinite(descriptors[0]).all())


if __name__ == "__main__":
    unittest.main()

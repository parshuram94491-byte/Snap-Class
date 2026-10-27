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

    def test_grayscale_uint8_is_preserved(self):
        image = np.arange(15, dtype=np.uint8).reshape(3, 5)

        prepared = face_pipeline.prepare_dlib_image(image)

        np.testing.assert_array_equal(prepared, image)
        self.assertEqual(prepared.shape, image.shape)

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

        self.assertIsNone(model["clf"])
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

        self.assertIsNotNone(model["clf"])
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

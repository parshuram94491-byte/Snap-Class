import unittest
from unittest.mock import patch

from src.components import dialog_attendance_results as attendance_review
from src.database import db


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeSupabaseQuery:
    def __init__(self, client, table):
        self.client = client
        self.table_name = table
        self.action = "select"
        self.filters = {}
        self.student_ids = None
        self.values = None

    def select(self, _columns):
        return self

    def eq(self, key, value):
        self.filters[key] = value
        return self

    def in_(self, key, values):
        if key == "student_id":
            self.student_ids = {str(value) for value in values}
        return self

    def insert(self, values):
        self.action = "insert"
        self.values = values
        return self

    def upsert(self, values, on_conflict):
        self.action = "upsert"
        self.values = values
        self.on_conflict = on_conflict
        return self

    def update(self, values):
        self.action = "update"
        self.values = values
        return self

    def execute(self):
        if self.client.fail_on_execute:
            raise OSError("database unavailable")
        if self.table_name == "subjects":
            if self.client.authorized:
                return FakeResponse([{"subject_id": self.filters["subject_id"]}])
            return FakeResponse([])
        if self.action == "upsert" and self.client.execute_error is not None:
            raise self.client.execute_error

        rows = self.client.attendance
        def matches(row, key, value):
            if key in {"student_id", "subject_id", "timestamp"}:
                return str(row.get(key)) == str(value)
            return row.get(key) == value

        if self.action == "select":
            return FakeResponse(
                [
                    dict(row)
                    for row in rows
                    if all(matches(row, key, value) for key, value in self.filters.items())
                    and (
                        self.student_ids is None
                        or str(row["student_id"]) in self.student_ids
                    )
                ]
            )
        if self.action == "insert":
            rows.extend(dict(row) for row in self.values)
            return FakeResponse(self.values)
        if self.action == "upsert":
            conflict_columns = self.on_conflict.split(",")
            for value in self.values:
                existing = next(
                    (
                        row for row in rows
                        if all(
                            str(row.get(column)) == str(value.get(column))
                            for column in conflict_columns
                        )
                    ),
                    None,
                )
                if existing is None:
                    rows.append(dict(value))
                else:
                    existing.update(value)
            return FakeResponse(self.values)
        if self.action == "update":
            for row in rows:
                if all(matches(row, key, value) for key, value in self.filters.items()):
                    row.update(self.values)
            return FakeResponse([])
        raise AssertionError(f"Unsupported action: {self.action}")


class FakeSupabase:
    def __init__(self):
        self.attendance = []
        self.authorized = True
        self.fail_on_execute = False
        self.execute_error = None

    def table(self, table_name):
        return FakeSupabaseQuery(self, table_name)


class FakeColumn:
    def __init__(self, ui):
        self.ui = ui

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def write(self, _value):
        return None

    def caption(self, _value):
        return None

    def selectbox(self, _label, options, key, **_kwargs):
        self.ui.selectbox_calls += 1
        value = self.ui.selected_values.get(key, self.ui.state[key])
        if value not in options:
            raise AssertionError(f"Unexpected status option: {value}")
        self.ui.state[key] = value
        return value

    def button(self, label, **kwargs):
        return self.ui.button(label, **kwargs)


class FakeStreamlit:
    def __init__(self, state, clicked=(), selected_values=None):
        self.session_state = state
        self.state = state
        self.clicked = set(clicked)
        self.selected_values = selected_values or {}
        self.errors = []
        self.successes = []
        self.selectbox_calls = 0

    def columns(self, spec):
        count = len(spec) if isinstance(spec, (list, tuple)) else spec
        return [FakeColumn(self) for _ in range(count)]

    def container(self, **_kwargs):
        return FakeColumn(self)

    def write(self, _value):
        return None

    def caption(self, _value):
        return None

    def button(self, label, **kwargs):
        return label in self.clicked and not kwargs.get("disabled", False)

    def error(self, message):
        self.errors.append(message)

    def success(self, message):
        self.successes.append(message)

    def rerun(self):
        return None


class AttendanceReviewStateTests(unittest.TestCase):
    def setUp(self):
        self.logs = [
            {
                "student_id": 1,
                "subject_id": 7,
                "timestamp": "2026-10-26T22:00:00",
                "is_present": False,
            },
            {
                "student_id": 2,
                "subject_id": 7,
                "timestamp": "2026-10-26T22:00:00",
                "is_present": True,
            },
        ]
        self.rows = [
            {"Name": "Student One", "ID": 1, "Source": "-", "Status": "Absent"},
            {"Name": "Student Two", "ID": 2, "Source": "Photo 1", "Status": "Present"},
        ]

    def test_status_initializes_from_automatic_result_and_can_override_each_way(self):
        state = {}
        _, automatic, keys = attendance_review._initialize_review(
            self.rows, self.logs, state
        )
        self.assertEqual(automatic, {"1": False, "2": True})
        self.assertEqual(state[keys["1"]], "Absent")
        self.assertEqual(state[keys["2"]], "Present")

        state[keys["1"]] = "Present"
        state[keys["2"]] = "Absent"
        corrected = attendance_review._finalize_attendance(
            self.logs, {student_id: state[key] for student_id, key in keys.items()}
        )
        self.assertEqual([row["is_present"] for row in corrected], [True, False])

    def test_unchanged_statuses_preserve_predictions_and_no_detection_is_editable(self):
        state = {}
        _, _, keys = attendance_review._initialize_review(self.rows, self.logs, state)
        unchanged = attendance_review._finalize_attendance(
            self.logs, {sid: state[key] for sid, key in keys.items()}
        )
        self.assertEqual([row["is_present"] for row in unchanged], [False, True])

        no_detection = [{"Name": "Student One", "ID": 1, "Source": "-"}]
        _, _, keys = attendance_review._initialize_review(no_detection, self.logs[:1], state)
        self.assertEqual(state[keys["1"]], "Absent")
        state[keys["1"]] = "Present"
        reviewed = attendance_review._finalize_attendance(
            self.logs[:1], {"1": state[keys["1"]]}
        )
        self.assertTrue(reviewed[0]["is_present"])

    def test_multiple_edits_survive_rerun_and_new_session_resets(self):
        state = {}
        first_session, _, keys = attendance_review._initialize_review(
            self.rows, self.logs, state
        )
        state[keys["1"]] = "Present"
        second_session, _, rerun_keys = attendance_review._initialize_review(
            self.rows, self.logs, state
        )
        self.assertEqual(first_session, second_session)
        self.assertEqual(state[rerun_keys["1"]], "Present")
        self.assertEqual(state[rerun_keys["2"]], "Present")

        new_logs = [dict(row, timestamp="2026-10-26T22:01:00") for row in self.logs]
        new_session, _, new_keys = attendance_review._initialize_review(
            self.rows, new_logs, state
        )
        self.assertNotEqual(first_session, new_session)
        self.assertEqual(state[new_keys["1"]], "Absent")
        self.assertEqual(state[new_keys["2"]], "Present")
        self.assertFalse(any(key in state for key in keys.values()))

    def test_discard_clears_pending_review_without_persisting(self):
        state = {"attendance_images": ["image"], "voice_attendance_results": ("rows", "logs")}
        attendance_review._initialize_review(self.rows, self.logs, state)
        attendance_review._discard_review(state)
        self.assertEqual(state["attendance_images"], [])
        self.assertIsNone(state["voice_attendance_results"])
        self.assertNotIn(attendance_review._ACTIVE_REVIEW_KEY, state)
        self.assertFalse(any(key.startswith(attendance_review._REVIEW_STATUS_PREFIX) for key in state))


class AttendancePersistenceTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeSupabase()
        self.logs = [
            {
                "student_id": 1,
                "subject_id": 7,
                "timestamp": "2026-10-26T22:00:00",
                "is_present": True,
            },
            {
                "student_id": 2,
                "subject_id": 7,
                "timestamp": "2026-10-26T22:00:00",
                "is_present": False,
            },
        ]
        self.patch_client = patch.object(db, "supabase", self.client)
        self.patch_client.start()
        self.addCleanup(self.patch_client.stop)

    def test_confirm_persists_corrected_records_and_repeat_does_not_duplicate(self):
        self.assertTrue(db.create_attendance(self.logs, teacher_id=99))
        self.assertTrue(db.create_attendance(self.logs, teacher_id=99))
        self.assertEqual(len(self.client.attendance), 2)
        self.assertEqual(
            [row["is_present"] for row in self.client.attendance],
            [True, False],
        )

    def test_duplicate_rows_for_existing_session_are_updated_not_inserted(self):
        self.client.attendance.append(dict(self.logs[0], is_present=False))
        db.create_attendance(self.logs[:1], teacher_id=99)
        self.assertEqual(len(self.client.attendance), 1)
        self.assertTrue(self.client.attendance[0]["is_present"])

    def test_partial_retry_inserts_only_missing_student_records(self):
        self.client.attendance.append(dict(self.logs[0]))
        db.create_attendance(self.logs, teacher_id=99)
        self.assertEqual(len(self.client.attendance), 2)

    def test_database_failure_propagates_without_success_result(self):
        self.client.fail_on_execute = True
        with self.assertRaises(db.AttendancePersistenceError):
            db.create_attendance(self.logs, teacher_id=99)

    def test_missing_conflict_index_error_names_required_migration(self):
        class MissingConflictIndexError(RuntimeError):
            code = "42P10"

        self.client.execute_error = MissingConflictIndexError(
            "no unique or exclusion constraint matching the ON CONFLICT specification"
        )
        with self.assertRaisesRegex(
            db.AttendancePersistenceError, "20261026230000_attendance_session_unique.sql"
        ):
            db.create_attendance(self.logs, teacher_id=99)

    def test_unauthorized_teacher_cannot_save_attendance(self):
        self.client.authorized = False
        with self.assertRaises(PermissionError):
            db.create_attendance(self.logs, teacher_id=99)
        self.assertEqual(self.client.attendance, [])

    def test_missing_teacher_is_rejected_before_database_write(self):
        with self.assertRaises(PermissionError):
            db.create_attendance(self.logs, teacher_id=None)
        self.assertEqual(self.client.attendance, [])

    def test_new_session_creates_separate_attendance_records(self):
        db.create_attendance(self.logs, teacher_id=99)
        new_session = [
            dict(row, timestamp="2026-10-26T22:01:00") for row in self.logs
        ]
        db.create_attendance(new_session, teacher_id=99)
        self.assertEqual(len(self.client.attendance), 4)


class AttendanceReviewDialogTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"Name": "Student One", "ID": 1, "Source": "-", "Status": "Absent"},
            {"Name": "Student Two", "ID": 2, "Source": "Photo 1", "Status": "Present"},
        ]
        self.logs = [
            {
                "student_id": 1,
                "subject_id": 7,
                "timestamp": "2026-10-26T22:00:00",
                "is_present": False,
            },
            {
                "student_id": 2,
                "subject_id": 7,
                "timestamp": "2026-10-26T22:00:00",
                "is_present": True,
            },
        ]
        self.state = {
            "user_role": "teacher",
            "teacher_data": {"teacher_id": 99},
        }

    def test_confirm_saves_selected_statuses_once_and_shows_success(self):
        ui = FakeStreamlit(
            self.state,
            clicked={"Confirm & Save"},
            selected_values={
                f"{attendance_review._REVIEW_STATUS_PREFIX}"
                f"{attendance_review._review_session_id(self.rows, self.logs)}_1": "Present",
                f"{attendance_review._REVIEW_STATUS_PREFIX}"
                f"{attendance_review._review_session_id(self.rows, self.logs)}_2": "Absent",
            },
        )
        with patch.object(attendance_review, "st", ui):
            with patch.object(attendance_review, "create_attendance") as save:
                attendance_review.show_attendance_result(self.rows, self.logs)

        final_rows = save.call_args.args[0]
        self.assertEqual([row["is_present"] for row in final_rows], [True, False])
        self.assertEqual([row["student_id"] for row in final_rows], [1, 2])
        self.assertEqual(save.call_args.kwargs, {"teacher_id": 99})
        self.assertTrue(ui.successes)
        self.assertEqual(
            self.state[attendance_review._SAVED_REVIEW_KEY],
            attendance_review._review_session_id(self.rows, self.logs),
        )

    def test_database_failure_keeps_review_and_does_not_show_success(self):
        ui = FakeStreamlit(self.state, clicked={"Confirm & Save"})
        with patch.object(attendance_review, "st", ui):
            with patch.object(
                attendance_review,
                "create_attendance",
                side_effect=db.AttendancePersistenceError("database unavailable"),
            ):
                attendance_review.show_attendance_result(self.rows, self.logs)

        self.assertFalse(ui.successes)
        self.assertTrue(any("remains available" in message for message in ui.errors))
        self.assertNotIn(attendance_review._SAVED_REVIEW_KEY, self.state)

    def test_discard_button_does_not_save(self):
        ui = FakeStreamlit(self.state, clicked={"Discard"})
        with patch.object(attendance_review, "st", ui):
            with patch.object(attendance_review, "create_attendance") as save:
                attendance_review.show_attendance_result(self.rows, self.logs)

        save.assert_not_called()
        self.assertNotIn(attendance_review._ACTIVE_REVIEW_KEY, self.state)
        self.assertEqual(self.state["attendance_images"], [])

    def test_unauthorized_user_cannot_confirm(self):
        self.state["user_role"] = "student"
        ui = FakeStreamlit(self.state, clicked={"Confirm & Save"})
        with patch.object(attendance_review, "st", ui):
            with patch.object(attendance_review, "create_attendance") as save:
                attendance_review.show_attendance_result(self.rows, self.logs)

        save.assert_not_called()
        self.assertTrue(any("authenticated teacher" in message for message in ui.errors))

    def test_voice_attendance_review_does_not_enable_manual_face_correction(self):
        ui = FakeStreamlit(self.state, clicked={"Confirm & Save"})
        with patch.object(attendance_review, "st", ui):
            with patch.object(attendance_review, "create_attendance") as save:
                attendance_review.show_attendance_result(
                    self.rows,
                    self.logs,
                    allow_manual_correction=False,
                )

        self.assertEqual(ui.selectbox_calls, 0)
        self.assertEqual(
            [row["is_present"] for row in save.call_args.args[0]],
            [False, True],
        )




    def test_summary_counts_and_search_filter_with_rich_streamlit(self):
        markdown_calls = []
        text_input_calls = []

        class RichFakeColumn(FakeColumn):
            def markdown(self, val, **kwargs):
                markdown_calls.append(val)

        class RichFakeStreamlit(FakeStreamlit):
            def columns(self, spec):
                count = len(spec) if isinstance(spec, (list, tuple)) else spec
                return [RichFakeColumn(self) for _ in range(count)]

            def markdown(self, val, **kwargs):
                markdown_calls.append(val)

            def text_input(self, label, **kwargs):
                text_input_calls.append((label, kwargs))
                return "Student One"

        ui = RichFakeStreamlit(
            self.state,
            clicked={"Confirm & Save"},
            selected_values={
                f"{attendance_review._REVIEW_STATUS_PREFIX}"
                f"{attendance_review._review_session_id(self.rows, self.logs)}_1": "Present",
            },
        )

        with patch.object(attendance_review, "st", ui):
            with patch.object(attendance_review, "create_attendance") as save:
                attendance_review.show_attendance_result(self.rows, self.logs)

        # Check summary cards in markdown
        summary_html = next(c for c in markdown_calls if "attendance-summary-cards" in c)
        self.assertIn("Total Students", summary_html)
        self.assertIn("Present", summary_html)
        self.assertIn("Absent", summary_html)
        # Student 1 was edited to Present, Student 2 was detected as Present: Total=2, Present=2, Absent=0
        self.assertIn(">2</span>", summary_html)
        self.assertIn(">0</span>", summary_html)

        # Confirm & Save still saved both students even with search query active
        final_rows = save.call_args.args[0]
        self.assertEqual(len(final_rows), 2)
        self.assertEqual([row["is_present"] for row in final_rows], [True, True])

    def test_discard_restores_pre_edit_state_on_next_init(self):
        state = {
            "user_role": "teacher",
            "teacher_data": {"teacher_id": 99},
            "attendance_images": ["photo1.jpg"],
            "voice_attendance_results": ("res", "logs"),
        }
        _, auto, keys = attendance_review._initialize_review(self.rows, self.logs, state)
        self.assertEqual(state[keys["1"]], "Absent")
        state[keys["1"]] = "Present"  # Teacher edits status

        ui = FakeStreamlit(state, clicked={"Discard"})
        with patch.object(attendance_review, "st", ui):
            attendance_review.show_attendance_result(self.rows, self.logs)

        # State should be discarded
        self.assertNotIn(attendance_review._ACTIVE_REVIEW_KEY, state)
        self.assertNotIn(attendance_review._SAVED_REVIEW_KEY, state)
        self.assertEqual(state["attendance_images"], [])
        self.assertIsNone(state["voice_attendance_results"])

        # Re-initializing restores detected statuses
        _, auto2, new_keys = attendance_review._initialize_review(self.rows, self.logs, state)
        self.assertEqual(state[new_keys["1"]], "Absent")
        self.assertEqual(state[new_keys["2"]], "Present")


if __name__ == "__main__":
    unittest.main()

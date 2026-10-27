import hashlib
import json
import textwrap

import streamlit as st

from src.database.db import AttendancePersistenceError, create_attendance

_REVIEW_STATUS_PREFIX = "_attendance_review_status_"
_ACTIVE_REVIEW_KEY = "_attendance_review_active_session"
_SAVED_REVIEW_KEY = "_attendance_review_saved_session"


def _records_from_table(table):
    if hasattr(table, "to_dict"):
        return table.to_dict(orient="records")
    return [dict(row) for row in table]


def _status_label(is_present):
    return "Present" if is_present else "Absent"


def _review_session_id(rows, logs):
    identity = {
        "rows": [
            {"student_id": str(row["ID"]), "name": row.get("Name", "")}
            for row in rows
        ],
        "logs": [
            {
                "student_id": str(log["student_id"]),
                "subject_id": str(log["subject_id"]),
                "timestamp": str(log["timestamp"]),
                "is_present": bool(log["is_present"]),
            }
            for log in logs
        ],
        "sources": [str(row.get("Source", "-")) for row in rows],
    }
    serialized = json.dumps(identity, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def _initialize_review(rows, logs, state):
    session_id = _review_session_id(rows, logs)
    if state.get(_ACTIVE_REVIEW_KEY) != session_id:
        for key in list(state):
            if key.startswith(_REVIEW_STATUS_PREFIX):
                del state[key]
        state[_ACTIVE_REVIEW_KEY] = session_id
        state.pop(_SAVED_REVIEW_KEY, None)

    automatic_statuses = {
        str(log["student_id"]): bool(log["is_present"])
        for log in logs
    }
    status_keys = {}
    for row in rows:
        student_id = str(row["ID"])
        if student_id not in automatic_statuses:
            raise ValueError(f"Missing attendance record for student {student_id}.")
        key = f"{_REVIEW_STATUS_PREFIX}{session_id}_{student_id}"
        state.setdefault(key, _status_label(automatic_statuses[student_id]))
        status_keys[student_id] = key

    return session_id, automatic_statuses, status_keys


def _finalize_attendance(logs, status_by_student):
    final_logs = []
    for log in logs:
        student_id = str(log["student_id"])
        if student_id not in status_by_student:
            raise ValueError(f"Missing reviewed status for student {student_id}.")
        final_log = dict(log)
        final_log["is_present"] = status_by_student[student_id] == "Present"
        final_logs.append(final_log)
    return final_logs


def _discard_review(state):
    for key in list(state):
        if key.startswith(_REVIEW_STATUS_PREFIX):
            del state[key]
    state.pop(_ACTIVE_REVIEW_KEY, None)
    state.pop(_SAVED_REVIEW_KEY, None)
    state["voice_attendance_results"] = None
    state["attendance_images"] = []


def show_attendance_result(df, logs, allow_manual_correction=True):
    rows = _records_from_table(df)
    logs = [dict(log) for log in logs]
    if not rows or not logs:
        st.error("There are no attendance records to review.")
        return

    teacher = st.session_state.get("teacher_data")
    if (
        st.session_state.get("user_role") != "teacher"
        or not isinstance(teacher, dict)
        or teacher.get("teacher_id") is None
    ):
        st.error("Only an authenticated teacher can review and save attendance.")
        return

    try:
        session_id, automatic_statuses, status_keys = _initialize_review(
            rows, logs, st.session_state
        )
    except (KeyError, ValueError) as exc:
        st.error(f"Could not prepare attendance review: {exc}")
        return

    saved = st.session_state.get(_SAVED_REVIEW_KEY) == session_id

    # Compute current statuses for all students across the review session
    current_statuses = {}
    for row in rows:
        sid = str(row["ID"])
        key = status_keys[sid]
        if hasattr(st, "selected_values") and key in st.selected_values:
            val = st.selected_values[key]
        elif key in st.session_state:
            val = st.session_state[key]
        else:
            val = _status_label(automatic_statuses[sid])
        current_statuses[sid] = val

    total_count = len(rows)
    present_count = sum(1 for s in current_statuses.values() if s == "Present")
    absent_count = sum(1 for s in current_statuses.values() if s == "Absent")

    # Render Subtitle & Dynamic Summary Cards
    if hasattr(st, "markdown"):
        st.markdown(
            textwrap.dedent(f"""
            <div class="attendance-review-container">
                <p class="attendance-review-subtitle">Review and correct attendance before saving.</p>
                <div class="attendance-summary-cards">
                    <div class="summary-card card-total">
                        <span class="summary-card-label">Total Students</span>
                        <span class="summary-card-value">{total_count}</span>
                    </div>
                    <div class="summary-card card-present">
                        <span class="summary-card-label">Present</span>
                        <span class="summary-card-value">{present_count}</span>
                    </div>
                    <div class="summary-card card-absent">
                        <span class="summary-card-label">Absent</span>
                        <span class="summary-card-value">{absent_count}</span>
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )
    else:
        st.write("Review each student's status before confirming attendance.")

    # Search filter field
    search_query = ""
    if hasattr(st, "text_input") and len(rows) > 1:
        search_query = st.text_input(
            "Search student by name or ID",
            placeholder="🔍  Search by student name or ID...",
            label_visibility="collapsed",
            key=f"_review_search_{session_id}",
        ).strip().lower()

    if search_query:
        filtered_rows = [
            r for r in rows
            if search_query in str(r.get("Name", "")).lower()
            or search_query in str(r.get("ID", "")).lower()
        ]
        if hasattr(st, "caption"):
            st.caption(f"Showing {len(filtered_rows)} of {len(rows)} students")
    else:
        filtered_rows = rows

    selected_statuses = dict(current_statuses)

    with st.container(
        key="attendance-review-list",
        border=False,
    ):
        with st.container(key="attendance-review-header", border=False):
            header = st.columns([2.2, 1.1, 1.15, 1.3, 1.45])
            header_labels = (
                "Student",
                "Student ID",
                "Source",
                "Detected Status",
                "Final Status",
            )
            for column, label in zip(header, header_labels):
                if hasattr(column, "markdown"):
                    column.markdown(
                        f'<span class="table-header-cell">{label}</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    column.caption(label)

        if not filtered_rows and search_query:
            if hasattr(st, "info"):
                st.info(f"No students found matching '{search_query}'.")
            else:
                st.write(f"No students found matching '{search_query}'.")
        else:
            for row in filtered_rows:
                student_id = str(row["ID"])
                student_name = str(row.get("Name", ""))
                automatic_label = _status_label(automatic_statuses[student_id])
                with st.container(
                    key=f"attendance-review-row-{session_id}-{student_id}",
                    border=False,
                ):
                    columns = st.columns([2.2, 1.1, 1.15, 1.3, 1.45])

                    if hasattr(columns[0], "markdown"):
                        columns[0].markdown(
                            f'<span class="student-name-cell" title="{student_name}">{student_name}</span>',
                            unsafe_allow_html=True,
                        )
                        columns[1].markdown(
                            f'<span class="student-id-cell">{student_id}</span>',
                            unsafe_allow_html=True,
                        )
                        src = row.get("Source", "-")
                        src_icon = (
                            "📷 "
                            if "photo" in str(src).lower()
                            else ("🎙️ " if "voice" in str(src).lower() else "")
                        )
                        columns[2].markdown(
                            f'<span class="badge-source">{src_icon}{src}</span>',
                            unsafe_allow_html=True,
                        )
                        status_class = (
                            "badge-present" if automatic_label == "Present" else "badge-absent"
                        )
                        columns[3].markdown(
                            f'<span class="badge-status {status_class}">● {automatic_label}</span>',
                            unsafe_allow_html=True,
                        )
                    else:
                        columns[0].write(student_name)
                        columns[1].write(student_id)
                        columns[2].write(row.get("Source", "-"))
                        columns[3].write(automatic_label)

                    if allow_manual_correction:
                        selected = columns[4].selectbox(
                            f"Final status for {student_name or student_id}",
                            options=("Present", "Absent"),
                            key=status_keys[student_id],
                            label_visibility="collapsed",
                            disabled=saved,
                        )
                    else:
                        selected = automatic_label
                        if hasattr(columns[4], "markdown"):
                            status_class = (
                                "badge-present" if selected == "Present" else "badge-absent"
                            )
                            columns[4].markdown(
                                f'<span class="badge-status {status_class}">● {selected}</span>',
                                unsafe_allow_html=True,
                            )
                        else:
                            columns[4].write(selected)

                    selected_statuses[student_id] = selected

                    if allow_manual_correction and selected != automatic_label:
                        if hasattr(columns[4], "markdown"):
                            columns[4].markdown(
                                '<span class="badge-override">Manual override</span>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.caption(f"Manual Override — {student_name or student_id}")

    with st.container(key="attendance-review-footer", border=False):
        if saved:
            st.success("Attendance saved successfully.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Discard", width="stretch", disabled=saved):
                _discard_review(st.session_state)
                st.rerun()

        with col2:
            if st.button(
                "Confirm & Save",
                width="stretch",
                type="primary",
                icon=":material/check:",
                disabled=saved,
            ):
                try:
                    final_logs = _finalize_attendance(logs, selected_statuses)
                    create_attendance(final_logs, teacher_id=teacher["teacher_id"])
                except (AttendancePersistenceError, PermissionError, ValueError) as exc:
                    st.error(
                        "Attendance could not be saved. Review remains available. "
                        f"{exc}"
                    )
                else:
                    st.session_state[_SAVED_REVIEW_KEY] = session_id
                    st.success("Attendance saved successfully.")


@st.dialog("Attendance Review", width="large")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)

import io
import re
from datetime import datetime

import pandas as pd

from src.database.config import supabase
import bcrypt


def _parse_timestamp(value):
    if value is None:
        return None, None, None

    timestamp_text = str(value)
    try:
        parsed = datetime.fromisoformat(timestamp_text.replace('Z', '+00:00'))
    except ValueError:
        return timestamp_text, '', timestamp_text

    return (
        parsed.date().isoformat(),
        parsed.strftime('%H:%M:%S'),
        parsed.strftime('%Y-%m-%d %I:%M %p'),
    )


def _sanitize_filename_component(value):
    text = str(value or '').strip()
    sanitized = re.sub(r'[^A-Za-z0-9._-]+', '_', text)
    sanitized = sanitized.strip('._')
    return sanitized or 'attendance'


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 



def create_teacher(username, password, name):

    data = { "username" : username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data



def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


class AttendancePersistenceError(RuntimeError):
    pass


def create_attendance(logs, teacher_id):
    required_fields = {'student_id', 'subject_id', 'timestamp', 'is_present'}
    if not logs:
        raise ValueError("Attendance records cannot be empty.")
    if teacher_id is None:
        raise PermissionError("An authenticated teacher is required to save attendance.")

    seen_records = set()
    records_by_session = {}
    for log in logs:
        if not required_fields.issubset(log):
            raise ValueError("Attendance record is missing required fields.")
        record_key = (
            str(log['student_id']),
            str(log['subject_id']),
            str(log['timestamp']),
        )
        if record_key in seen_records:
            raise ValueError("Attendance contains duplicate student session records.")
        seen_records.add(record_key)
        records_by_session.setdefault(
            (str(log['subject_id']), str(log['timestamp'])), []
        ).append(log)

    try:
        for session_key, session_logs in records_by_session.items():
            subject_id = session_key[0]
            authorization = (
                supabase.table('subjects')
                .select('subject_id')
                .eq('subject_id', subject_id)
                .eq('teacher_id', teacher_id)
                .execute()
            )
            if not authorization.data:
                raise PermissionError(
                    "You are not authorized to save attendance for this subject."
                )

            (
                supabase.table('attendance_logs')
                .upsert(
                    session_logs,
                    on_conflict='student_id,subject_id,timestamp',
                )
                .execute()
            )
    except PermissionError:
        raise
    except Exception as exc:
        error_code = getattr(exc, 'code', None)
        error_message = str(exc).lower()
        if (
            error_code == '42P10'
            or 'no unique or exclusion constraint matching the on conflict specification'
            in error_message
        ):
            raise AttendancePersistenceError(
                "The attendance session unique index is missing. Apply "
                "supabase/migrations/20261026230000_attendance_session_unique.sql "
                "to the Supabase project, then retry."
            ) from exc
        raise AttendancePersistenceError(
            "The attendance records could not be synchronized with the database."
        ) from exc

    return True

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data


def get_teacher_attendance_sessions(teacher_id):
    response = supabase.table('attendance_logs').select(
        '*, subjects!inner(*), students(*)'
    ).eq('subjects.teacher_id', teacher_id).execute()

    sessions = []
    seen = set()
    for row in response.data:
        subject = row.get('subjects') or {}
        data_ts = row.get('timestamp')
        if not data_ts:
            continue

        subject_id = row.get('subject_id')
        session_key = (str(subject_id), str(data_ts))
        if session_key in seen:
            continue
        seen.add(session_key)

        session_date, session_time, session_label = _parse_timestamp(data_ts)
        sessions.append({
            'subject_id': subject_id,
            'subject_name': subject.get('name'),
            'subject_code': subject.get('subject_code'),
            'timestamp': data_ts,
            'date': session_date,
            'time': session_time,
            'display_label': session_label or str(data_ts),
        })

    return sorted(sessions, key=lambda item: item['timestamp'], reverse=True)


def get_attendance_session_rows(subject_id, timestamp):
    response = supabase.table('attendance_logs').select(
        '*, students(*), subjects(*)'
    ).eq('subject_id', subject_id).eq('timestamp', timestamp).execute()

    rows = []
    for record in response.data:
        student = record.get('students') or {}
        subject = record.get('subjects') or {}
        session_date, session_time, session_label = _parse_timestamp(record.get('timestamp'))
        rows.append({
            'Student ID': record.get('student_id'),
            'Student Name': student.get('name') or 'Unknown Student',
            'Subject': subject.get('name') or '',
            'Subject Code': subject.get('subject_code') or '',
            'Date': session_date or '',
            'Time': session_time or '',
            'Attendance Status': 'Present' if record.get('is_present') else 'Absent',
        })

    return rows


def build_attendance_export_file(rows, subject_name, subject_code, timestamp):
    if not rows:
        raise ValueError('No attendance records are available for this session.')

    df = pd.DataFrame(
        rows,
        columns=[
            'Student ID',
            'Student Name',
            'Subject',
            'Subject Code',
            'Date',
            'Time',
            'Attendance Status',
        ],
    )

    session_date, _, _ = _parse_timestamp(timestamp)
    filename_base = f"SnapClass_Attendance_{_sanitize_filename_component(subject_name)}_{_sanitize_filename_component(subject_code)}_{session_date or 'session'}"

    output = io.BytesIO()
    try:
        from openpyxl.styles import Font
    except ModuleNotFoundError as exc:
        raise RuntimeError('openpyxl is required to generate Excel exports.') from exc

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Attendance', index=False)
        worksheet = writer.sheets['Attendance']
        worksheet.freeze_panes = 'A2'
        for cell in worksheet[1]:
            cell.font = Font(bold=True)
        for column_cells in worksheet.columns:
            column_letter = column_cells[0].column_letter
            max_length = max(
                (len(str(cell.value)) if cell.value is not None else 0) for cell in column_cells
            )
            worksheet.column_dimensions[column_letter].width = max(max_length + 2, 14)
        worksheet.auto_filter.ref = worksheet.dimensions

    output.seek(0)
    return output, f"{filename_base}.xlsx"

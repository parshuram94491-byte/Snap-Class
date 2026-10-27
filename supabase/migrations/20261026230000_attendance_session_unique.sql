create unique index if not exists attendance_logs_student_subject_timestamp_key
on public.attendance_logs (student_id, subject_id, timestamp);

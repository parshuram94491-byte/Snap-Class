import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

from src.database import db


class AttendanceExportTests(unittest.TestCase):
    def test_get_attendance_session_rows_uses_saved_records_for_selected_session(self):
        rows = [
            {
                'student_id': 101,
                'subject_id': 7,
                'timestamp': '2026-10-27T09:00:00',
                'is_present': True,
                'students': {'name': 'Asha Patel'},
                'subjects': {'name': 'Maths', 'subject_code': 'BCS101'},
            },
            {
                'student_id': 102,
                'subject_id': 7,
                'timestamp': '2026-10-27T09:00:00',
                'is_present': False,
                'students': {'name': 'Kabir Singh'},
                'subjects': {'name': 'Maths', 'subject_code': 'BCS101'},
            },
        ]

        class FakeQuery:
            def __init__(self, data):
                self.data = data
                self.filters = {}

            def select(self, *_args, **_kwargs):
                return self

            def eq(self, key, value):
                self.filters[key] = value
                return self

            def execute(self):
                filtered = [
                    row for row in self.data
                    if all(row.get(key) == value for key, value in self.filters.items())
                ]
                return SimpleNamespace(data=filtered)

        with patch.object(db.supabase, 'table', return_value=FakeQuery(rows)):
            export_rows = db.get_attendance_session_rows(7, '2026-10-27T09:00:00')

        self.assertEqual(len(export_rows), 2)
        self.assertEqual(export_rows[0]['Attendance Status'], 'Present')
        self.assertEqual(export_rows[1]['Attendance Status'], 'Absent')
        self.assertEqual(export_rows[0]['Student Name'], 'Asha Patel')
        self.assertEqual(export_rows[1]['Student ID'], 102)

    def test_build_attendance_export_file_creates_xlsx_with_expected_columns(self):
        rows = [
            {
                'Student ID': 101,
                'Student Name': 'Asha Patel',
                'Subject': 'Maths',
                'Subject Code': 'BCS101',
                'Date': '2026-10-27',
                'Time': '09:00:00',
                'Attendance Status': 'Present',
            },
            {
                'Student ID': 102,
                'Student Name': 'Kabir Singh',
                'Subject': 'Maths',
                'Subject Code': 'BCS101',
                'Date': '2026-10-27',
                'Time': '09:00:00',
                'Attendance Status': 'Absent',
            },
        ]

        buffer, filename = db.build_attendance_export_file(
            rows,
            'Maths',
            'BCS101',
            '2026-10-27T09:00:00',
        )

        self.assertEqual(filename, 'SnapClass_Attendance_Maths_BCS101_2026-10-27.xlsx')
        buffer.seek(0)
        dataframe = pd.read_excel(buffer, engine='openpyxl')

        self.assertEqual(list(dataframe.columns), [
            'Student ID',
            'Student Name',
            'Subject',
            'Subject Code',
            'Date',
            'Time',
            'Attendance Status',
        ])
        self.assertEqual(len(dataframe), 2)
        self.assertEqual(dataframe.iloc[0].to_dict()['Attendance Status'], 'Present')
        self.assertEqual(dataframe.iloc[1].to_dict()['Attendance Status'], 'Absent')


if __name__ == '__main__':
    unittest.main()

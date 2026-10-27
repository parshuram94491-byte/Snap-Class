import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_dashboard, footer_home
from src.ui.base_layout import style_background_home, style_base_layout
from src.screens.home_screen import home_screen


class TestLandingPage(unittest.TestCase):
    def setUp(self):
        if 'login_type' in st.session_state:
            del st.session_state['login_type']

    def test_footer_home_branding(self):
        with patch('streamlit.markdown') as mock_markdown:
            footer_home()
            mock_markdown.assert_called_once()
            call_content = mock_markdown.call_args[0][0]
            self.assertIn("Created with ❤️ by", call_content)
            self.assertIn("Parshuram Prajapati", call_content)
            self.assertNotIn("apnacollege", call_content.lower())
            self.assertNotIn("apna college", call_content.lower())

    def test_dashboard_footer_branding(self):
        with patch('streamlit.markdown') as mock_markdown:
            footer_dashboard()
            mock_markdown.assert_called_once()
            call_content = mock_markdown.call_args[0][0]
            self.assertIn("Created with ❤️ by", call_content)
            self.assertIn("Parshuram Prajapati", call_content)
            self.assertNotIn("apnacollege", call_content.lower())
            self.assertNotIn("apna college", call_content.lower())
            self.assertNotIn("<img", call_content.lower())

    def test_header_home_branding(self):
        with patch('streamlit.markdown') as mock_markdown:
            header_home()
            mock_markdown.assert_called_once()
            call_content = mock_markdown.call_args[0][0]
            self.assertIn("SNAP", call_content)
            self.assertIn("CLASS", call_content)
            self.assertIn("Smart Attendance. Smarter Classrooms.", call_content)
            self.assertIn("snap-pill", call_content)
            self.assertIn("snap-dot", call_content)
            self.assertIn("logo.png", call_content)
            self.assertIn("aria-label=\"SnapClass graduation cap\"", call_content)
            self.assertIn("onerror=", call_content)

    def test_style_background_home(self):
        with patch('streamlit.markdown') as mock_markdown:
            style_background_home()
            mock_markdown.assert_called_once()
            call_content = mock_markdown.call_args[0][0]
            self.assertIn("radial-gradient", call_content)
            self.assertIn("data:image/svg+xml", call_content)
            self.assertIn(".stApp:has(.snap-home-page)::before", call_content)
            # Check buttons and portal cards
            self.assertIn("st-key-btn_student_portal", call_content)
            self.assertIn("st-key-btn_teacher_portal", call_content)

    def test_mobile_attendance_review_styles_keep_cards_and_footer_accessible(self):
        with patch('streamlit.markdown') as mock_markdown:
            style_base_layout()
            css = mock_markdown.call_args[0][0]

        self.assertIn("width: calc(100vw - 24px)", css)
        self.assertIn("max-height: calc(100dvh - 24px)", css)
        self.assertIn(".st-key-attendance-review-list", css)
        self.assertIn("[class*=\"st-key-attendance-review-row-\"]", css)
        self.assertIn("word-break: normal !important", css)
        self.assertIn("min-height: 44px !important", css)
        self.assertIn(".st-key-attendance-review-footer", css)

    def test_home_screen_renders_columns_and_cards(self):
        with patch('src.screens.home_screen.header_home') as mock_header, \
             patch('src.screens.home_screen.style_background_home') as mock_bg, \
             patch('src.screens.home_screen.style_base_layout') as mock_base, \
             patch('src.screens.home_screen.footer_home') as mock_footer, \
             patch('streamlit.columns') as mock_cols, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.button', return_value=False) as mock_button:
            
            col1 = MagicMock()
            col2 = MagicMock()
            mock_cols.return_value = (col1, col2)

            home_screen()

            mock_header.assert_called_once()
            mock_bg.assert_called_once()
            mock_base.assert_called_once()
            mock_footer.assert_called_once()
            mock_cols.assert_called_once_with(2, gap="large")
            self.assertEqual(mock_button.call_count, 2)


if __name__ == '__main__':
    unittest.main()

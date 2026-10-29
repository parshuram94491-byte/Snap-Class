import logging

import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import (
    get_face_embeddings,
    identify_student,
    match_registered_face,
    refresh_face_model,
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

logger = logging.getLogger(__name__)

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()


    st.space()

    c1, c2 =st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()


    st.divider()


    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid,{"total":0, "attended": 0} )
        def unenroll_button():
                if st.button(
                    "Unenroll from this course",
                    type='tertiary',
                    width='stretch',
                    icon=':material/delete_forever:',
                    key=f"unenroll_{student_id}_{sid}",
                ):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f'Unenrolled from {sub['name']} successfully!')
                    st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()


def student_screen():


    style_background_dashboard()
    style_base_layout()


    student_data = st.session_state.get("student_data")
    if (
        st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
        and isinstance(student_data, dict)
        and student_data.get("student_id") is not None
        and student_data.get("name")
    ):
        student_dashboard()
        return
    if "student_data" in st.session_state:
        logger.warning(
            "Discarding student session data without a valid authenticated student identity."
        )
        st.session_state.pop("student_data", None)
    if (
        st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
    ):
        logger.error("Student session is missing a valid database identity.")
        st.session_state["is_logged_in"] = False
        st.session_state["user_role"] = None
        st.error("Your sign-in session is invalid. Please sign in again.")
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()
    
    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        try:
            img = np.asarray(Image.open(photo_source).convert("RGB"), dtype=np.uint8)
            with st.spinner('AI is scanning..'):
                match = identify_student(img)
        except Exception:
            logger.exception(
                "Student face sign-in failed in "
                "src.screens.student_screen.student_screen"
            )
            st.error(
                "Face recognition could not be completed. Please retry; "
                "if it continues, contact support."
            )
            return

        if match["status"] == "no_face":
            st.warning('Face not found!')
        elif match["status"] == "multiple_faces":
            st.warning('Multiple faces found')
        elif match["status"] == "ambiguous":
            st.warning(
                'This face matches multiple student profiles. Please contact support '
                'to resolve the duplicate profiles before signing in.'
            )
        elif match["status"] == "unknown":
            st.info('Face not recognized! You might be a new student!')
            show_registration = True
        else:
            student = match["student"]
            if student is None:
                logger.error(
                    "Student face sign-in matched without a database identity; refusing login."
                )
                st.error(
                    "The matched student profile could not be loaded. Please retry "
                    "or contact support."
                )
                return

            st.session_state.is_logged_in = True
            st.session_state.user_role = 'student'
            st.session_state.student_data = student
            st.toast(f'Welcome Back {student["name"]}')
            time.sleep(1)
            st.rerun()
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Akash.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        try:
                            img = np.asarray(
                                Image.open(photo_source).convert("RGB"),
                                dtype=np.uint8,
                            )
                            encodings = get_face_embeddings(img)
                        except Exception:
                            logger.exception(
                                "Face enrollment image processing failed in "
                                "src.screens.student_screen.student_screen"
                            )
                            st.error(
                                "Face enrollment could not be completed. Please retry; "
                                "if it continues, contact support."
                            )
                            return

                        if len(encodings) != 1:
                            if encodings:
                                st.warning(
                                    'Only one face can be registered at a time. '
                                    'Please capture a photo with one face.'
                                )
                            else:
                                st.error('Could not capture facial features for registration')
                            return

                        face_emb = encodings[0].tolist()
                        try:
                            existing_students = get_all_students()
                            existing_match = match_registered_face(
                                encodings[0], existing_students
                            )
                        except Exception:
                            logger.exception(
                                "Duplicate face enrollment check failed in "
                                "src.screens.student_screen.student_screen"
                            )
                            st.error(
                                "Existing profiles could not be checked. The new "
                                "profile was not created; please retry."
                            )
                            return

                        if existing_match["status"] == "matched":
                            st.warning(
                                "This face is already registered to a student profile. "
                                "Sign in with that profile or contact support."
                            )
                            return
                        if existing_match["status"] == "ambiguous":
                            st.warning(
                                "This face matches multiple existing profiles. "
                                "Registration was stopped; please contact support."
                            )
                            return

                        voice_emb = None
                        if audio_data:
                            voice_emb = get_voice_embedding(audio_data.read())

                        try:
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                        except Exception:
                            logger.exception(
                                "Student profile creation failed in "
                                "src.screens.student_screen.student_screen"
                            )
                            st.error(
                                "The student profile could not be saved. Please retry."
                            )
                            return

                        if response_data:
                            try:
                                refresh_face_model()
                            except Exception:
                                logger.exception(
                                    "Face model refresh failed in "
                                    "src.screens.student_screen.student_screen"
                                )
                                st.error(
                                    "Your profile was saved, but face recognition "
                                    "could not be initialized. Please contact support."
                                )
                                return
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = response_data[0]
                            st.toast(f'Profile Created! Hi {response_data[0]["name"]}!')
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error('Student profile was not saved; please retry.')

                else:
                    st.warning('Please enter your name!')


        
    footer_dashboard()
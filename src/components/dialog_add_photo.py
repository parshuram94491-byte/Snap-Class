import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog("Capture or upload photos", width="large")
def add_photos_dialog():

    st.markdown('<div class="photo-upload-dialog"></div>', unsafe_allow_html=True)
    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    st.segmented_control(
        'Choose how to add photos',
        options=('camera', 'upload'),
        format_func=lambda option: 'Take a photo' if option == 'camera' else 'Upload photos',
        width='stretch',
        label_visibility='collapsed',
        key='photo_tab',
    )

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input(
            'Take Snapshot',
            key='dialog_cam',
            resolution='720p',
            width='stretch',
        )
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured')
            st.rerun()


    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload',
        )

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            
            st.toast('Photo Uploaded Successfully')
            st.rerun()

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()

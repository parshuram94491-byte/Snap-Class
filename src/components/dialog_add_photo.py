import streamlit as st
from PIL import Image


def decode_photo(image_source):
    with Image.open(image_source) as image:
        image.load()
        return image.convert("RGB")


@st.dialog("Capture or upload photos", width="large")
def add_photos_dialog():
    if "attendance_photo_decode_failures" not in st.session_state:
        st.session_state.attendance_photo_decode_failures = 0

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
            try:
                st.session_state.attendance_images.append(decode_photo(cam_photo))
            except Exception:
                st.session_state.attendance_photo_decode_failures += 1
                st.error("The captured photo could not be decoded. Please try again.")
            else:
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
            loaded_count = 0
            failed_count = 0
            for uploaded_file in uploaded_files:
                try:
                    st.session_state.attendance_images.append(
                        decode_photo(uploaded_file)
                    )
                    loaded_count += 1
                except Exception:
                    failed_count += 1

            if loaded_count:
                st.toast(f'{loaded_count} photo(s) uploaded successfully')
            if failed_count:
                st.session_state.attendance_photo_decode_failures += failed_count
                st.warning(
                    f'{failed_count} photo(s) could not be decoded and were skipped.'
                )
            if loaded_count:
                st.rerun()

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()

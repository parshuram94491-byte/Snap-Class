import streamlit as st
from PIL import Image

MAX_ATTENDANCE_PHOTOS = 10
MAX_ATTENDANCE_IMAGE_SIZE_MB = 10
MAX_ATTENDANCE_IMAGE_DIMENSION = 1600


def _select_upload_batch(uploaded_files, current_photo_count):
    remaining = max(0, MAX_ATTENDANCE_PHOTOS - current_photo_count)
    return uploaded_files[:remaining], max(0, len(uploaded_files) - remaining)


def decode_photo(image_source):
    with Image.open(image_source) as image:
        image.thumbnail(
            (MAX_ATTENDANCE_IMAGE_DIMENSION, MAX_ATTENDANCE_IMAGE_DIMENSION),
            Image.Resampling.LANCZOS,
        )
        return image.convert("RGB")


@st.dialog("Capture or upload photos", width="large")
def add_photos_dialog():
    if "attendance_photo_decode_failures" not in st.session_state:
        st.session_state.attendance_photo_decode_failures = 0
    if "attendance_photo_widget_generation" not in st.session_state:
        st.session_state.attendance_photo_widget_generation = 0

    st.markdown('<div class="photo-upload-dialog"></div>', unsafe_allow_html=True)
    st.write('Add classroom photos to scan for attendance')
    st.caption(
        f"{len(st.session_state.attendance_images)} of "
        f"{MAX_ATTENDANCE_PHOTOS} photos added"
    )

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
            key=(
                f"dialog_cam_"
                f"{st.session_state.attendance_photo_widget_generation}"
            ),
            resolution='720p',
            width='stretch',
        )
        if cam_photo:
            if len(st.session_state.attendance_images) >= MAX_ATTENDANCE_PHOTOS:
                st.warning(
                    f"Attendance is limited to {MAX_ATTENDANCE_PHOTOS} photos. "
                    "Clear the current photos before adding more."
                )
            else:
                try:
                    st.session_state.attendance_images.append(decode_photo(cam_photo))
                except Exception:
                    st.session_state.attendance_photo_decode_failures += 1
                    st.session_state.attendance_photo_widget_generation += 1
                    st.error("The captured photo could not be decoded. Please try again.")
                else:
                    st.session_state.attendance_photo_widget_generation += 1
                    st.toast('Photo Captured')
                    st.rerun()


    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            max_upload_size=MAX_ATTENDANCE_IMAGE_SIZE_MB,
            key=(
                f"dialog_upload_"
                f"{st.session_state.attendance_photo_widget_generation}"
            ),
            help=(
                f"Up to {MAX_ATTENDANCE_PHOTOS} photos per attendance session, "
                f"with a {MAX_ATTENDANCE_IMAGE_SIZE_MB} MB limit per photo."
            ),
        )

        if uploaded_files:
            loaded_count = 0
            failed_count = 0
            selected_files, excess_count = _select_upload_batch(
                uploaded_files, len(st.session_state.attendance_images)
            )
            for uploaded_file in selected_files:
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
                st.session_state.attendance_upload_notice = (
                    f'{failed_count} photo(s) could not be decoded and were skipped.'
                )
            if excess_count:
                st.session_state.attendance_upload_notice = (
                    f'{excess_count} extra photo(s) were not added because attendance '
                    f'is limited to {MAX_ATTENDANCE_PHOTOS} photos.'
                )
            st.session_state.attendance_photo_widget_generation += 1
            st.rerun()

    upload_notice = st.session_state.pop("attendance_upload_notice", None)
    if upload_notice:
        st.warning(upload_notice)

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()

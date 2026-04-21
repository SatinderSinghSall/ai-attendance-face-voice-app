import streamlit as st
from PIL import Image


MAX_IMAGES = 20

@st.dialog("Capture or Upload Photos.")
def add_photos_dialog():

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    st.write("Add classroom photos to scan for attendance.")

    t1, t2 = st.columns(2)

    with t1:
        if st.button("Camera", type="primary" if st.session_state.photo_tab=="camera" else "tertiary", width="stretch"):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:
        if st.button("Upload Photos", type="primary" if st.session_state.photo_tab=="upload" else "tertiary", width="stretch"):
            st.session_state.photo_tab = "upload"
            st.rerun()

    if len(st.session_state.attendance_images) >= MAX_IMAGES:
        st.warning("Maximum 20 photos allowed.")
        return

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take Snapshot")

        if cam_photo:
            try:
                img = Image.open(cam_photo)
                st.session_state.attendance_images.append(img)
                st.toast("Photo captured!", icon="📷")
                st.rerun()
            except Exception:
                st.error("Failed to process captured image.")

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg","png","jpeg"],
            accept_multiple_files=True
        )

        if uploaded_files:
            for f in uploaded_files:
                try:
                    img = Image.open(f)
                    st.session_state.attendance_images.append(img)
                except Exception:
                    st.error(f"Failed to load {f.name}")

            st.toast("Photos uploaded successfully!")
            st.rerun()

    if st.session_state.attendance_images:
        st.image(st.session_state.attendance_images, width=200)

    st.divider()

    if st.button("Done", type="primary", width="stretch"):
        if not st.session_state.attendance_images:
            st.warning("Please add at least one photo.")
        else:
            st.rerun()


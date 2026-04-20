import streamlit as st
import numpy as np
from PIL import Image
import time

from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipeline.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipeline.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student


def student_screen():
    style_base_layout()
    style_background_dashboard()

    if "student" in st.session_state:
        student_dashboard()
        return

    col, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with col:
        header_dashboard()

    with col2:
        if st.button(
            "Go Back to Home",
            type="secondary",
            key="login-back-button",
            shortcut="control+backspace"
        ):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()
    st.space()

    st.header("Login using FaceId", text_alignment="center")

    photo_source = st.camera_input("Position your face in the Center")
    show_student_registration = False

    if photo_source:

        img = np.array(Image.open(photo_source).convert("RGB"))

        with st.spinner("AI is Scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

        if num_faces == 0:
            st.warning("Face not found.")

        elif num_faces > 1:
            st.warning("Multiple faces found.")

        else:
            if detected:

                student_id = list(detected.keys())[0]

                all_students = get_all_students()

                student = next(
                    (s for s in all_students if s['student_id'] == student_id),
                    None
                )

                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'student'
                    st.session_state.student = student

                    st.toast(f"Welcome, {student['name']}!")

                    time.sleep(2)
                    st.rerun()

            else:
                st.error("Face not recognized. You might be a new Student.")
                show_student_registration = True

    if show_student_registration:
        with st.container(border=True):
            st.header("Register new profile.")
            student_name = st.text_input("Enter your name", placeholder="Satinder Singh Sall")

            st.subheader("Optional: Voice Enrollment.")
            st.info("Enroll for voice ONLY attendance.")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short phase like 'I am present, my name is Satinder Singh Sall' kind of voice record.")
            except Exception:
                st.error("Audio record / data Failed.")

            if st.button("Crate your account.", type="primary"):
                if student_name:
                    with st.spinner("Creating your new Profile..."):

                        img = np.array(Image.open(photo_source).convert("RGB"))

                        embeddings = get_face_embeddings(img)

                        if embeddings:
                            face_emb = embeddings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                student_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:
                                train_classifier()

                                new_student = response_data[0]

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student = new_student

                                st.toast(f"Hi, {new_student['name']}! Your new profile is created successfully.")

                                time.sleep(2)
                                st.rerun()
                        else:
                            st.error("Could not capture your facial features for registration.")
                else:
                    st.warning("Please enter your name.")

    footer_dashboard()


# Method for Student Dashboard Screen:
def student_dashboard():
    st.header("Student Dashboard:")


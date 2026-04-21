import streamlit as st
from src.database.db import create_subject


@st.dialog("Create a New Subject")
def create_subject_dialog(teacher_id):

    st.write("Enter the details of the new Subject:")

    sub_id = st.text_input("Enter Subject id:", placeholder="CS101")
    sub_name = st.text_input("Enter Subject name:", placeholder="Full-Stack Mobile App Development")
    sub_sec = st.text_input("Enter Subject section:", placeholder="A")

    create_btn = st.button(
        "Create a New Subject Now.",
        type="primary",
        use_container_width=True
    )

    if create_btn:
        if sub_id and sub_name and sub_sec:
            try:
                create_subject(sub_id, sub_name, sub_sec, teacher_id)
                st.toast("Subject Created Successfully! 🎉")
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)} while creating the Subject.")

        else:
            st.warning("Please fill all the fields.")


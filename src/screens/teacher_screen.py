import streamlit as st
import time

from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_background_dashboard

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog

from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects


def teacher_screen():
    style_base_layout()
    style_background_dashboard()

    st.session_state.setdefault("teacher_login_type", "login")

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

    footer_dashboard()


# Method for Register Teacher:
def register_teacher(teacher_name, teacher_username, teacher_password, teacher_password_confirm):
    if not teacher_name or not teacher_username or not teacher_password or not teacher_password_confirm:
        return False, "Please enter all the input fields and try again."
    if check_teacher_exists(teacher_username):
        return False, "Username is already taken."
    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Account crated successfully. Login now."
    except Exception as e:
        return False, "Unexpected Error Occured."


# Method to Login a Teacher:
def login_teacher(teacher_username, teacher_password):
    if not teacher_username or not teacher_password:
        return False

    teacher = teacher_login(teacher_username, teacher_password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True


# Function / Method for Teacher Login Screen:
def teacher_screen_login():
    col, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with col:
        header_dashboard()

    with col2:
        if st.button("Go Back to Home", type="secondary", key="login-back-button", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using Password", text_alignment="center")

    st.space()
    st.space()

    teacher_username = st.text_input("Enter your username", placeholder="satindersinghsall")
    teacher_password = st.text_input("Enter your password", placeholder="MyPassword@123", type="password")

    st.divider()

    btnCol1, btnCol2 = st.columns(2)

    with btnCol1:
        if st.button("Login", icon=":material/passkey:", shortcut="command+enter", width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="👋🏻")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid username and password combination.")

    with btnCol2:
        if st.button("Register", icon=":material/passkey:", width="stretch", type="primary"):
            st.session_state.teacher_login_type = 'register'
            st.rerun()


# Function / Method for Teacher Register Screen:
def teacher_screen_register():
    col, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with col:
        header_dashboard()

    with col2:
        if st.button("Go Back to Home", type="secondary", key="login-back-button", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your Teacher Profile")

    st.space()
    st.space()

    teacher_name = st.text_input("Enter your name", placeholder="Satinder Singh Sall")
    teacher_username = st.text_input("Enter your username", placeholder="satindersinghsall")
    teacher_password = st.text_input("Enter your password", placeholder="MyPassword@123", type="password")
    teacher_password_confirm = st.text_input("Confirm your password", placeholder="MyPassword@123", type="password")

    st.divider()

    btnCol1, btnCol2 = st.columns(2)

    with btnCol1:
        if st.button("Register Now", icon=":material/passkey:", shortcut="command+enter", width="stretch"):
            success, message = register_teacher(teacher_name, teacher_username, teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                time.sleep(3)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)

    with btnCol2:
        if st.button("Login", icon=":material/passkey:", width="stretch", type="primary"):
            st.session_state.teacher_login_type = 'login'
            st.rerun()


# Method for Teacher Dashboard Screen:
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    col, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with col:
        header_dashboard()

    with col2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button("Log Out", type="secondary", key="login-back-button", shortcut="control+backspace"):
            st.session_state['is_login'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
        st.rerun()

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button("Attendance Records", type=type3, width="stretch", icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
       teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
       teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
       teacher_tab_attendance_records()


# Method for Teacher Take Attendance Screen:
def teacher_tab_take_attendance():
    st.header("Take AI Attendance:")


# Method for Teacher Manage Student Screen:
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header("Manage Subjects")

    with col2:
        if st.button("Create New Subject", use_container_width=True):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:

            stats = [
            ("👥", "Students", sub['total_students']),
            ("🕜", "Classes", sub['total_classes'])
            ]

            def share_button():
                if st.button(
                    f"Share Code: {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_button
            )

    else:
        st.info("No subjects created yet.")


# Method for Teacher Attendance Records Screen:
def teacher_tab_attendance_records():
    st.header("Attendance Records:")


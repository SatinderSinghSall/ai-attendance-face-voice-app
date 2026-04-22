from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import time

from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_background_dashboard

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photos import add_photos_dialog
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.dialog_attendance_details import attendance_details_dialog

from src.database.config import supabase

from src.pipeline.face_pipeline import predict_attendance

from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher


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
        if st.button("Log Out", type="secondary", key="teacher-logout-button", shortcut="control+backspace"):
            st.session_state.is_logged_in = False
            st.session_state.login_type = None
            st.session_state.pop("teacher_data", None)
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


# Method for Teacher Take Attendance Screen
def teacher_tab_take_attendance():

    st.header("Take AI Attendance")

    teacher_id = st.session_state.teacher_data['teacher_id']

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You have not created any subjects yet, please create one to begin.")
        return

    subjects_options = {
        f"{s['name']} - {s['subject_code']}": s['subject_id']
        for s in subjects
    }

    col1, col2 = st.columns([3,1], vertical_alignment="bottom")

    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subjects_options.keys())
        )

    with col2:
        st.write("")
        if st.button(
            "Add Photos",
            icon=":material/add_circle:",
            use_container_width=True,
            type="primary"
        ):
            add_photos_dialog()

    selected_subject_id = subjects_options[selected_subject_label]

    st.divider()

    # -------------------------
    # PHOTO GALLERY
    # -------------------------

    if st.session_state.attendance_images:

        st.subheader("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx+1}")

    c1, c2, c3 = st.columns(3)

    # -------------------------
    # CLEAR PHOTOS
    # -------------------------

    has_photos = bool(st.session_state.attendance_images)

    with c1:
        if st.button(
            "Clear All Photos",
            icon=":material/delete:",
            use_container_width=True,
            type="tertiary",
            disabled= not has_photos
        ):
            st.session_state.attendance_images = []
            st.rerun()

    # -------------------------
    # FACE ANALYSIS
    # -------------------------

    with c2:
        if st.button(
            "Run Face Analysis",
            icon=":material/analytics:",
            use_container_width=True,
            type="secondary",
            disabled= not has_photos
        ):

            with st.spinner("Deep scanning classroom photos..."):

                all_detected_photos = {}

                for idx, img in enumerate(st.session_state.attendance_images):

                    img_np = np.array(img.convert("RGB"))

                    detected, _, _ = predict_attendance(img_np)

                    if detected:

                        for sid in detected.keys():

                            student_id = int(sid)

                            all_detected_photos.setdefault(student_id, []).append(
                                f"Photo {idx+1}"
                            )

            # -------------------------
            # FETCH ENROLLED STUDENTS
            # -------------------------

            enrolled_res = supabase.table("subject_students") \
                .select("*, students(*)") \
                .eq("subject_id", selected_subject_id) \
                .execute()

            enrolled_students = enrolled_res.data

            if not enrolled_students:

                st.warning("No students enrolled in this course.")

            else:

                results = []
                attendance_to_log = []

                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                for node in enrolled_students:

                    student = node["students"]

                    sources = all_detected_photos.get(
                        int(student["student_id"]), []
                    )

                    is_present = len(sources) > 0

                    results.append({

                        "Name": student["name"],
                        "Student ID": student["student_id"],
                        "Detected In": ", ".join(sources) if is_present else "-",
                        "Status": "✅ Present" if is_present else "❌ Absent"
                    })

                    attendance_to_log.append({

                        "student_id": student["student_id"],
                        "subject_id": selected_subject_id,
                        "timestamp": current_timestamp,
                        "is_present": is_present

                    })

                attendance_result_dialog(
                    pd.DataFrame(results),
                    attendance_to_log
                )

    # -------------------------
    # VOICE ATTENDANCE
    # -------------------------

    with c3:

        if st.button(
            "Use Voice Attendance",
            icon=":material/mic:",
            use_container_width=True,
            type="primary"
        ):
            voice_attendance_dialog(selected_subject_id)


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
    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet.")
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        try:
            dt_obj = datetime.fromisoformat(ts) if ts else None
            formatted_time = dt_obj.strftime("%Y-%m-%d %I:%M %p") if dt_obj else "N/A"
            ts_group = dt_obj.replace(microsecond=0) if dt_obj else None
        except Exception:
            formatted_time = "Invalid Time"
            ts_group = None

        subject = r.get('subjects') or {}

        data.append({
            "ts_group": ts_group,
            "Time": formatted_time,
            "Subject": subject.get('name', 'Unknown'),
            "Subject Code": subject.get('subject_code', 'N/A'),
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + " Students"
    )

    summary['Percentage'] = (
        (summary['Present_Count'] / summary['Total_Count']) * 100
    ).round(1).astype(str) + '%'

    display_df = summary.sort_values(by='ts_group', ascending=False)

    selected_index = st.selectbox(
        "Select a record to view details",
        options=display_df.index,
        format_func=lambda i: f"{display_df.loc[i, 'Time']} | {display_df.loc[i, 'Subject']}"
    )

    selected_row = display_df.loc[selected_index]

    if st.button("View Details", type="primary"):
        from src.components.dialog_attendance_details import attendance_details_dialog

        attendance_details_dialog(
            selected_row['ts_group'],
            selected_row['Subject Code'],
            selected_row['Subject']
        )

    st.dataframe(
        display_df[['Time', 'Subject', 'Subject Code', 'Attendance Stats', 'Percentage']],
        use_container_width=True,
        hide_index=True
    )


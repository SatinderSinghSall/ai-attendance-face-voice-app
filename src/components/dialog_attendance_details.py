import streamlit as st
import pandas as pd
from datetime import datetime

from src.database.config import supabase


@st.dialog("📊 Attendance Details")
def attendance_details_dialog(ts_group, subject_code, subject_name):

    if not ts_group:
        st.error("Invalid session selected.")
        return

    try:
        res = (
            supabase.table("attendance_logs")
            .select("*, students(*), subjects(*)")  # ✅ FIXED (removed teachers)
            .eq("timestamp", ts_group.isoformat())
            .execute()
        )

        data = res.data

    except Exception as e:
        st.error(f"Error fetching attendance data: {e}")
        return

    if not data:
        st.warning("No attendance data found for this session.")
        return

    first = data[0]

    st.subheader("Class Information")

    teacher_name = st.session_state.teacher_data.get("name", "N/A")

    try:
        formatted_time = ts_group.strftime("%Y-%m-%d %I:%M %p")
    except Exception:
        formatted_time = "Invalid Time"

    st.write(f"**Subject:** {subject_name}")
    st.write(f"**Subject Code:** {subject_code}")
    st.write(f"**Teacher:** {teacher_name}")
    st.write(f"**Time:** {formatted_time}")

    st.divider()

    table_data = []

    for row in data:
        student = row.get("students", {})

        table_data.append({
            "Student Name": student.get("name", "Unknown"),
            "Student ID": student.get("student_id", "N/A"),
            "Status": "✅ Present" if row.get("is_present") else "❌ Absent"
        })

    df = pd.DataFrame(table_data)

    st.subheader("Student Attendance")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    present_count = df["Status"].str.contains("Present").sum()
    total_count = len(df)

    percentage = (present_count / total_count * 100) if total_count > 0 else 0

    st.divider()

    st.write(
        f"### 📊 Summary: ✅ {present_count} / {total_count} Students ({percentage:.1f}%)"
    )


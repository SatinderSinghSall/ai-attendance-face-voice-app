import streamlit as st

from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def teacher_screen():
    style_base_layout()
    style_background_dashboard()

    st.session_state.setdefault("teacher_login_type", "login")

    if st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

    footer_dashboard()

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
        st.button("Login", icon=":material/passkey:", shortcut="command+enter", width="stretch")

    with btnCol2:
        if st.button("Register", icon=":material/passkey:", width="stretch", type="primary"):
            st.session_state.teacher_login_type = 'register'
            st.rerun()


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
        st.button("Register Now", icon=":material/passkey:", shortcut="command+enter", width="stretch")

    with btnCol2:
        if st.button("Login", icon=":material/passkey:", width="stretch", type="primary"):
            st.session_state.teacher_login_type = 'login'
            st.rerun()


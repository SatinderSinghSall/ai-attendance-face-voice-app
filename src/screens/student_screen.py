import streamlit as st
import numpy as np
from PIL import Image
import time

from src.ui.base_layout import style_base_layout
from src.ui.base_layout import style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def student_screen():
    style_base_layout()
    style_background_dashboard()
    
    col, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with col:
        header_dashboard()

    with col2:
        if st.button("Go Back to Home", type="secondary", key="login-back-button", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()
    st.space()

    st.header("Login using FaceId", text_alignment="center")
    photo_source =  st.camera_input("Position your face in the Center")

    if photo_source:
        np.array(Image.open())

    footer_dashboard()

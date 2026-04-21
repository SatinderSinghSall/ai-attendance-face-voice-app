import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>

        .stApp {
            background: #5865F2 !important;
        }

        .stApp div[data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            padding: 2rem !important;
            border-radius: 3rem !important;
            max-width: 800px;
            margin: auto;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
            .stApp {
                background: #E0E3FF !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        /* Hide Streamlit default top bar */
        # #MainMenu, footer, header {
        #     visibility: hidden;
        # }

        /* Center content and limit width */
        .block-container {
            max-width: 900px;
            margin: auto;
            padding-top: 2rem !important;
        }

        /* Title styling */
        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0.5rem !important;
            text-align: center;
        }

        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 1.9rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0.5rem !important;
        }

        h3, h4, p, label {
            font-family: 'Outfit', sans-serif;
        }

        /* Inputs look cleaner */
        input {
            border-radius: 1rem !important;
            border: none !important;
            padding: 0.6rem !important;
            font-size: 0.95rem !important;
        }

        /* Make inputs less stretched */
        div[data-baseweb="input"] {
            max-width: 100%;
        }

        /* Improve spacing */
        div[data-testid="stTextInput"] {
            margin-bottom: 0.8rem;
        }

        /* Your original button style (unchanged) */
        button {
            border-radius: 1.5rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
            font-weight: 500 !important;
        }

        button[kind="secondary"] {
            background-color: #EB459E !important;
        }

        button[kind="tertiary"] {
            background-color: black !important;
        }

        button:hover {
            transform: scale(1.05);
        }

        /* Better divider spacing */
        hr {
            margin-top: 1.2rem;
            margin-bottom: 1.2rem;
            opacity: 0.4;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

import streamlit as st
from supabase import create_clint, Client

supabase: Client = create_clint(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
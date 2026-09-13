import streamlit as st
from supabase import Client, create_client


def get_supabase_client() -> Client:
    """One Supabase client per browser session (not cached across users) —
    a logged-in client carries that user's session token internally, so
    sharing one instance across sessions would leak it between users."""
    if "supabase_client" not in st.session_state:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        st.session_state["supabase_client"] = create_client(url, key)
    return st.session_state["supabase_client"]

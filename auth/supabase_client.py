import streamlit as st
from supabase import Client, create_client


@st.cache_resource
def get_supabase_client() -> Client:
    """Uses the service_role (secret) key, not the publishable/anon key.

    This is safe here because Streamlit code runs entirely server-side —
    the browser never sees this key or talks to Supabase directly. We're
    doing our own email/password auth (see auth/security.py) instead of
    Supabase Auth, so there's no per-user session to isolate: every
    request uses this same static key, and authorization (who can see
    what) is enforced in application code, not RLS/auth.uid().
    """
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)

import streamlit as st

from auth.supabase_client import get_supabase_client
from auth.validators import is_valid_college_email

COLLEGE_EMAIL_HINT = "Please enter your correct institution email address."


def is_logged_in() -> bool:
    return st.session_state.get("auth_user") is not None


def current_user():
    return st.session_state.get("auth_user")


def logout():
    supabase = get_supabase_client()
    supabase.auth.sign_out()
    st.session_state.pop("auth_session", None)
    st.session_state.pop("auth_user", None)


def _set_session(session, user):
    st.session_state["auth_session"] = session
    st.session_state["auth_user"] = user


def _ensure_student_profile(supabase, user):
    """Create the student's profile row on first login, now that they have
    an authenticated session (RLS requires auth.uid() == id)."""
    full_name = (user.user_metadata or {}).get("full_name", "")
    try:
        supabase.table("students").upsert(
            {"id": user.id, "full_name": full_name, "email": user.email}
        ).execute()
    except Exception as e:
        st.warning(f"Profile sync failed: {e}")


def login_form():
    with st.form("login_form"):
        email = st.text_input("College email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")

    if not submitted:
        return

    if not is_valid_college_email(email):
        st.error(COLLEGE_EMAIL_HINT)
        return

    supabase = get_supabase_client()
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    except Exception as e:
        st.error(f"Login failed: {e}")
        return

    _set_session(result.session, result.user)
    _ensure_student_profile(supabase, result.user)
    st.rerun()


def signup_form():
    with st.form("signup_form"):
        full_name = st.text_input("Full name")
        email = st.text_input("College email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Sign up")

    if not submitted:
        return

    if not full_name.strip():
        st.error("Full name is required.")
        return
    if not is_valid_college_email(email):
        st.error(COLLEGE_EMAIL_HINT)
        return
    if len(password) < 8:
        st.error("Password must be at least 8 characters.")
        return
    if password != confirm_password:
        st.error("Passwords do not match.")
        return

    email = email.strip().lower()
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": {"full_name": full_name.strip()}},
            }
        )
    except Exception as e:
        st.error(f"Sign up failed: {e}")
        return

    st.success("Account created! Check your email to confirm, then log in.")


def auth_page():
    st.title("Lens")
    tab_login, tab_signup = st.tabs(["Log in", "Sign up"])
    with tab_login:
        login_form()
    with tab_signup:
        signup_form()


def require_login():
    if not is_logged_in():
        auth_page()
        st.stop()

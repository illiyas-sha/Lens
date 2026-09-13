import streamlit as st

from auth.security import hash_password, verify_password
from auth.supabase_client import get_supabase_client
from auth.validators import is_valid_college_email
from config import SECTIONS

COLLEGE_EMAIL_HINT = "Please enter your correct institution email address."


def is_logged_in() -> bool:
    return st.session_state.get("auth_user") is not None


def current_user():
    return st.session_state.get("auth_user")


def logout():
    st.session_state.pop("auth_user", None)


def login_form():
    with st.form("login_form"):
        email = st.text_input("College email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")

    if not submitted:
        return

    email = email.strip().lower()
    if not is_valid_college_email(email):
        st.error(COLLEGE_EMAIL_HINT)
        return

    supabase = get_supabase_client()
    result = supabase.table("students").select("*").eq("email", email).execute()
    rows = result.data

    if not rows or not verify_password(password, rows[0]["password_hash"]):
        st.error("Incorrect email or password.")
        return

    student = rows[0]
    st.session_state["auth_user"] = {
        "id": student["id"],
        "email": student["email"],
        "full_name": student["full_name"],
        "section": student.get("section"),
        "is_admin": student.get("is_admin", False),
    }
    st.rerun()


def signup_form():
    with st.form("signup_form"):
        full_name = st.text_input("Full name")
        section = st.selectbox(
            "Section", SECTIONS, index=None, placeholder="Select a section"
        )
        email = st.text_input("College email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Sign up")

    if not submitted:
        return

    email = email.strip().lower()
    if not full_name.strip():
        st.error("Full name is required.")
        return
    if not section:
        st.error("Please select a section.")
        return
    if not email:
        st.error("College email is required.")
        return
    if not is_valid_college_email(email):
        st.error(COLLEGE_EMAIL_HINT)
        return
    if not password or not confirm_password:
        st.error("Password and confirm password are required.")
        return
    if len(password) < 8:
        st.error("Password must be at least 8 characters.")
        return
    if password != confirm_password:
        st.error("Passwords do not match.")
        return

    supabase = get_supabase_client()
    existing = supabase.table("students").select("id").eq("email", email).execute()
    if existing.data:
        st.error("An account with that email already exists.")
        return

    supabase.table("students").insert(
        {
            "full_name": full_name.strip(),
            "section": section,
            "email": email,
            "password_hash": hash_password(password),
        }
    ).execute()

    st.success("Account created! You can log in now.")


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

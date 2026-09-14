import streamlit as st

from admin.ui import render as render_admin
from analytics.ui import render as render_overview
from auth.ui import auth_page, current_user, is_logged_in, logout
from scores.ui import render as render_scores

st.set_page_config(page_title="Lens", page_icon="🔍", layout="wide")


def home_page():
    st.title("Lens")
    st.write("Base Streamlit app is up and running.")


if not is_logged_in():
    st.navigation([st.Page(auth_page, title="Lens")], position="hidden").run()
else:
    user = current_user()

    with st.sidebar:
        st.write(f"Logged in as **{user['full_name']}**")
        if st.button("Log out"):
            logout()
            st.rerun()

    pages = [
        st.Page(home_page, title="Home", url_path="home", default=True),
        st.Page(render_scores, title="Score Entry", url_path="score-entry"),
        st.Page(render_overview, title="Term Overview", url_path="term-overview"),
    ]
    if user.get("is_admin"):
        pages.append(st.Page(render_admin, title="Admin", url_path="admin"))

    st.navigation(pages).run()

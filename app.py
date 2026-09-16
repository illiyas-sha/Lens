import streamlit as st

from admin.ui import render as render_admin
from analytics.ui import render as render_overview
from auth.ui import auth_page, current_user, is_logged_in, logout
from scores.ui import render as render_scores

st.set_page_config(page_title="Lens", page_icon="🔍", layout="wide")


def home_page():
    user = current_user()
    st.title("🔍 Lens")
    st.subheader(f"Welcome, {user['full_name'].split()[0]}!")
    st.write(
        "Lens is your academic tracker and analytics dashboard for the program — PGPBM.  "
        "Submit your component scores and see exactly where you stand "
        "term by term."
    )

    st.divider()
    st.subheader("What you can do here")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**📝 Score Entry**")
            st.write(
                "Submit your marks for a component (quiz, midterm, assignment, "
                "etc.) under a course. "
            )
    with col2:
        with st.container(border=True):
            st.markdown("**📊 Term Overview**")
            st.write(
                "Pick a term and course to see batch stats per component — "
                "mean, median, max, min — with your own score marked clearly "
                "against them."
            )

    if user.get("is_admin"):
        with st.container(border=True):
            st.markdown("**🛠️ Admin**")
            st.write(
                "Add terms, courses, and components so students have something "
                "to submit scores against."
            )

    st.divider()
    st.subheader("Coming soon")
    st.write(
        "The personal analytics layer is next — where you'll be able to see:"
    )
    st.markdown(
        "- **Strength/weakness insights** — where you're ahead or behind, "
        "course by course\n"
        "- **Radar chart** — your relative performance across all courses "
        "at a glance\n"
        "- **Trend chart** — your improvement analytics term by term"
    )

    st.divider()
    st.subheader("How to navigate")
    st.write(
        "Use the sidebar on the left to switch between pages. "
        f"You're logged in as **{user['email']}**, and can log out any time "
        "from the sidebar."
    )


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

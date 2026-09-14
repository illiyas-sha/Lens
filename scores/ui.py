import streamlit as st

from auth.ui import current_user, require_login
from catalog import list_components, list_courses, list_terms
from scores.queries import get_existing_score, submit_score


def render():
    require_login()
    user = current_user()

    st.title("Submit Your Scores")

    terms = list_terms()
    if not terms:
        st.info("No terms available yet — check back once your admin sets one up.")
        return
    term_options = {t["name"]: t["id"] for t in terms}
    selected_term_id = term_options[st.selectbox("Term", list(term_options.keys()))]

    courses = list_courses(selected_term_id)
    if not courses:
        st.info("No courses available for this term yet.")
        return
    course_options = {c["name"]: c["id"] for c in courses}
    selected_course_id = course_options[
        st.selectbox("Course", list(course_options.keys()))
    ]

    components = list_components(selected_course_id)
    if not components:
        st.info("No components available for this course yet.")
        return
    component_options = {c["name"]: c for c in components}
    selected_component = component_options[
        st.selectbox("Component", list(component_options.keys()))
    ]

    max_marks = float(selected_component["max_marks"])
    existing = get_existing_score(selected_component["id"], user["id"])

    with st.form("score_entry_form"):
        marks = st.number_input(
            f"Marks obtained (out of {max_marks:g})",
            min_value=0.0,
            max_value=max_marks,
            value=float(existing["marks_obtained"]) if existing else 0.0,
            step=1.0,
        )
        submitted = st.form_submit_button("Submit")

    if existing:
        st.caption(
            f"You previously submitted {existing['marks_obtained']:g}. "
            "Submitting again will update it."
        )

    if submitted:
        submit_score(selected_component["id"], user["id"], marks, max_marks)
        st.success("Score submitted!")
        st.rerun()

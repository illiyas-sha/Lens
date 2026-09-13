import streamlit as st

from admin import queries
from auth.ui import current_user, require_login


def require_admin():
    require_login()
    if not current_user().get("is_admin"):
        st.error("You don't have access to this page.")
        st.stop()


def render():
    require_admin()
    st.title("Admin")

    st.header("Terms")
    terms = queries.list_terms()
    if terms:
        st.table(terms)

    with st.form("add_term_form"):
        name = st.text_input("Term name")
        start_date = st.date_input("Start date")
        end_date = st.date_input("End date")
        if st.form_submit_button("Add term") and name.strip():
            queries.add_term(name.strip(), start_date, end_date)
            st.success(f"Added term '{name}'")
            st.rerun()

    if not terms:
        return

    st.divider()
    st.header("Courses")
    term_options = {t["name"]: t["id"] for t in terms}
    selected_term_name = st.selectbox("Term", list(term_options.keys()))
    selected_term_id = term_options[selected_term_name]

    courses = queries.list_courses(selected_term_id)
    if courses:
        st.table(courses)

    with st.form("add_course_form"):
        course_name = st.text_input("Course name")
        course_code = st.text_input("Course code (optional)")
        credits = st.number_input("Credits", min_value=0.0, step=0.5)
        if st.form_submit_button("Add course") and course_name.strip():
            queries.add_course(
                selected_term_id, course_name.strip(), course_code.strip(), credits
            )
            st.success(f"Added course '{course_name}'")
            st.rerun()

    if not courses:
        return

    st.divider()
    st.header("Components")
    course_options = {c["name"]: c["id"] for c in courses}
    selected_course_name = st.selectbox("Course", list(course_options.keys()))
    selected_course_id = course_options[selected_course_name]

    components = queries.list_components(selected_course_id)
    if components:
        st.table(components)

    with st.form("add_component_form"):
        comp_name = st.text_input("Component name")
        max_marks = st.number_input("Max marks", min_value=0.01, step=1.0)
        weightage_marks = st.number_input(
            "Weightage marks (converted marks toward course total)",
            min_value=0.0,
            step=1.0,
        )
        if st.form_submit_button("Add component") and comp_name.strip():
            queries.add_component(
                selected_course_id, comp_name.strip(), max_marks, weightage_marks
            )
            st.success(f"Added component '{comp_name}'")
            st.rerun()

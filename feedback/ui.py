import streamlit as st

from auth.ui import current_user, require_login
from feedback.queries import submit_feedback


def render():
    require_login()
    user = current_user()

    st.title("Feedback")
    st.write(
        "Help us improve Lens — rate your experience and let us know what "
        "to add or fix."
    )

    with st.form("feedback_form"):
        rating = st.slider("How would you rate the app?", 1, 10, value=8)
        comments = st.text_area("Feedback / comments")
        enhancement_request = st.text_area(
            "Enhancement requests (anything you'd like added?)"
        )
        submitted = st.form_submit_button("Submit feedback")

    if not submitted:
        return

    submit_feedback(
        student_id=user["id"],
        full_name=user["full_name"],
        email=user["email"],
        rating=rating,
        comments=comments.strip(),
        enhancement_request=enhancement_request.strip(),
    )
    st.success("Thanks for your feedback!")

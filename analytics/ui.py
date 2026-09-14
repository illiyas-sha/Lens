import base64

import altair as alt
import pandas as pd
import streamlit as st

from analytics.queries import get_scores_for_components
from auth.ui import current_user, require_login
from catalog import list_components, list_courses, list_terms

COLOR_SCALE = alt.Scale(
    domain=["Your score", "Mean", "Median", "Max", "Min", "Total"],
    range=["#e91e63", "#000000", "#1f77b4", "#2ca02c", "#d62728", "#ff9800"],
)
LEGEND = alt.Legend(title=None, orient="bottom", direction="horizontal")

# A small runner icon (facing right, matching "Your score"'s pink). Uses
# Google's Material Design "directions_run" glyph (Apache-2.0) embedded
# directly, rather than an emoji font, since emoji direction/support vary
# across viewers' devices/browsers.
_RUNNER_COLOR = "#e91e63"
_RUNNER_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    f'<path fill="{_RUNNER_COLOR}" d="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 '
    ".9 2 2 2zm-3.6 13.9l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c"
    "-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1l-5.2 2.2v4.7h2v-3.4l"
    '1.8-.7-1.6 8.1-4.9-1-.4 2 7 1.4z"/></svg>'
)
RUNNER_ICON_URI = "data:image/svg+xml;base64," + base64.b64encode(
    _RUNNER_SVG.encode("utf-8")
).decode("ascii")


def render():
    require_login()
    user = current_user()

    st.title("Term Overview")

    terms = list_terms()
    if not terms:
        st.info("No terms available yet.")
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

    component_ids = [c["id"] for c in components]
    scores = get_scores_for_components(component_ids)
    if not scores:
        st.info("No scores submitted yet for this course.")
        return

    scores_df = pd.DataFrame(scores)
    component_names = {c["id"]: c["name"] for c in components}
    scores_df["Component"] = scores_df["component_id"].map(component_names)

    summary = (
        scores_df.groupby("Component")["marks_obtained"]
        .agg(Mean="mean", Median="median", Max="max", Min="min", Submissions="count")
        .round(2)
        .reset_index()
    )

    your_scores = scores_df[scores_df["student_id"] == user["id"]].set_index(
        "Component"
    )["marks_obtained"]
    summary.insert(1, "Your score", summary["Component"].map(your_scores))

    max_marks_per_component = scores_df.groupby("Component")["max_marks"].first()
    summary["Max Marks"] = summary["Component"].map(max_marks_per_component)

    # One self-contained board per component, in the order components were
    # added, rather than one combined table/chart that's hard to scan.
    component_order = [c["name"] for c in components]
    summary["Component"] = pd.Categorical(
        summary["Component"], categories=component_order, ordered=True
    )
    summary = summary.sort_values("Component")

    for _, row in summary.iterrows():
        with st.container(border=True):
            st.subheader(row["Component"])
            cols = st.columns(5)
            cols[0].metric("Your score", _fmt(row["Your score"]))
            cols[1].metric("Mean", _fmt(row["Mean"]))
            cols[2].metric("Median", _fmt(row["Median"]))
            cols[3].metric("Max", _fmt(row["Max"]))
            cols[4].metric("Min", _fmt(row["Min"]))
            st.caption(
                f"Out of {row['Max Marks']:g} · {row['Submissions']:g} submission(s)"
            )
            st.altair_chart(_component_chart(row), use_container_width=True)


def _fmt(value) -> str:
    return "—" if pd.isna(value) else f"{value:g}"


Y_DOMAIN = ["icon", "track"]
Y_SCALE = alt.Scale(domain=Y_DOMAIN)


def _component_chart(row: pd.Series) -> alt.Chart:
    """A single horizontal track from 0 to the component's total marks, with
    Median/Max/Min as colored dots, Mean as a bold black benchmark tick, a
    square marking the total, and a runner icon (on its own row above the
    track, so it isn't obscured by the other marks) for the student's own
    score."""
    right = float(row["Max Marks"]) * 1.05
    x_scale = alt.Scale(domain=[0, right])

    def y_enc():
        return alt.Y("y:N", axis=None, title=None, scale=Y_SCALE, sort=Y_DOMAIN)

    range_df = pd.DataFrame({"y": ["track"], "Zero": [0], "Total": [row["Max Marks"]]})
    range_layer = (
        alt.Chart(range_df)
        .mark_rule(color="#e5e5e5", strokeWidth=16)
        .encode(
            y=y_enc(),
            x=alt.X("Zero:Q", title="Marks", scale=x_scale),
            x2="Total:Q",
        )
    )

    dots_df = pd.DataFrame(
        {
            "y": ["track"] * 3,
            "Metric": ["Median", "Max", "Min"],
            "Value": [row["Median"], row["Max"], row["Min"]],
        }
    )
    dots_layer = (
        alt.Chart(dots_df)
        .mark_point(size=220, filled=True, opacity=0.9)
        .encode(
            y=y_enc(),
            x=alt.X("Value:Q", scale=x_scale),
            color=alt.Color("Metric:N", scale=COLOR_SCALE, legend=LEGEND),
            tooltip=["Metric", "Value"],
        )
    )

    total_df = pd.DataFrame(
        {"y": ["track"], "Metric": ["Total"], "Value": [row["Max Marks"]]}
    )
    total_layer = (
        alt.Chart(total_df)
        .mark_point(size=180, filled=True, shape="square", opacity=0.9)
        .encode(
            y=y_enc(),
            x=alt.X("Value:Q", scale=x_scale),
            color=alt.Color("Metric:N", scale=COLOR_SCALE, legend=LEGEND),
            tooltip=["Metric", "Value"],
        )
    )

    mean_df = pd.DataFrame({"y": ["track"], "Metric": ["Mean"], "Value": [row["Mean"]]})
    mean_layer = (
        alt.Chart(mean_df)
        .mark_tick(thickness=3, size=32)
        .encode(
            y=y_enc(),
            x=alt.X("Value:Q", scale=x_scale),
            color=alt.Color("Metric:N", scale=COLOR_SCALE, legend=LEGEND),
            tooltip=["Metric", "Value"],
        )
    )

    your_track_df = pd.DataFrame(
        {"y": ["track"], "Metric": ["Your score"], "Value": [row["Your score"]]}
    )
    # An invisible point purely to register "Your score" in the shared
    # legend (image marks below don't support a color/legend encoding).
    your_legend_layer = (
        alt.Chart(your_track_df)
        .mark_point(opacity=0)
        .encode(
            y=y_enc(),
            x=alt.X("Value:Q", scale=x_scale),
            color=alt.Color("Metric:N", scale=COLOR_SCALE, legend=LEGEND),
        )
    )

    your_icon_df = pd.DataFrame(
        {
            "y": ["icon"],
            "Metric": ["Your score"],
            "Value": [row["Your score"]],
            "icon": [RUNNER_ICON_URI],
        }
    )
    your_icon_layer = (
        alt.Chart(your_icon_df)
        .mark_image(width=30, height=30)
        .encode(
            y=y_enc(),
            x=alt.X("Value:Q", scale=x_scale),
            url="icon:N",
            tooltip=["Metric", "Value"],
        )
    )
    your_layer = your_legend_layer + your_icon_layer

    return (
        range_layer + dots_layer + total_layer + mean_layer + your_layer
    ).properties(height=190)

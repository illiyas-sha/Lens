"""General app configuration (not login-eligibility rules — see auth/config.py).

Values come from st.secrets["app"]. Edit secrets.toml to change them.
"""

import streamlit as st

_app_secrets = st.secrets.get("app", {})

SECTIONS = list(_app_secrets.get("sections", []))

"""Email eligibility rules for who can register/log in.

Values come from st.secrets["auth"] (see .streamlit/secrets.toml.example)
so the actual domain/roll-number rules aren't visible in the public repo.
Edit secrets.toml — locally and in Streamlit Cloud's app settings — not
this file, to change the rules.
"""

import streamlit as st

_auth_secrets = st.secrets.get("auth", {})

ALLOWED_DOMAINS = list(_auth_secrets.get("allowed_domains", []))
ROLL_NUMBER_LENGTH = int(_auth_secrets.get("roll_number_length", 7))
ROLL_NUMBER_PREFIX = str(_auth_secrets.get("roll_number_prefix", "260"))
EXCEPTION_EMAILS = set(_auth_secrets.get("exception_emails", []))

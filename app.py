import streamlit as st

from auth.ui import current_user, logout, require_login

st.set_page_config(page_title="Lens", page_icon="🔍", layout="wide")

require_login()

user = current_user()

with st.sidebar:
    st.write(f"Logged in as **{user['full_name']}**")
    if st.button("Log out"):
        logout()
        st.rerun()

st.title("Lens")
st.write("Base Streamlit app is up and running.")

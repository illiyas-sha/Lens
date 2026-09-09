import streamlit as st

st.set_page_config(page_title="Lens", page_icon="🔍", layout="wide")

st.title("Lens")
st.write("Base Streamlit app is up and running.")

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")

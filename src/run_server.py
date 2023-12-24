import subprocess

import streamlit as st


def start_uvicorn():
    subprocess.Popen(["uvicorn", "server:app"])


@st.cache_resource
def start_server():
    start_uvicorn()

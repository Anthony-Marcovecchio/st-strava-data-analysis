import streamlit as st
from models import initialize_models
from strava_auth import authenticate

st.set_page_config(layout="wide")


def app():
    st.title("Strava Dashboard")

    if "strava_auth" not in st.session_state:
        authenticate()

    else:
        if st.session_state.strava_auth is not None:
            initialize_models()

        athlete = st.session_state.athlete
        if athlete:
            st.write(f" #### Welcome, {athlete.firstname}")


app()

import streamlit as st
from data import strava_oauth_session, get_athlete_data


def app():
    # on app start-up, make user authenticate with Strava
    if "strava_session" not in st.session_state:
        st.session_state.strava_session = strava_oauth_session()

    if st.session_state.strava_session is not None:
        data = get_athlete_data(st.session_state.strava_session)
        st.write(data)


app()

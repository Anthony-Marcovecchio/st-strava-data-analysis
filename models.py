import streamlit as st


def initialize_models():
    if "athlete" not in st.session_state:
        st.session_state.athlete = athlete()


class athlete:
    def __init__(self):
        self.id = 0
        self.firstname = ""
        self.lastname = ""
        self.weight = 0

        self.set_athlete_data()

    def set_athlete_data(self):
        session = st.session_state.strava_auth
        data = self.get_athlete_data(session)
        self.id = data["id"]
        self.firstname = data["firstname"]
        self.lastname = data["lastname"]
        self.weight = data["weight"]

    def get_athlete_data(self, session):
        response = session.get("https://www.strava.com/api/v3/athlete/")
        data = response.json()
        return data

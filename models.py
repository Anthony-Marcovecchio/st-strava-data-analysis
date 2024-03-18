import streamlit as st


def initialize_models():
    if "athlete" not in st.session_state:
        st.session_state.athlete = athlete()
    # if "athlete_stats" not in st.session_state:
    #     st.session_state.athlete_stats = athlete_stats()


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


class athlete_stats:
    def __init__(self):
        self.recent_run_totals = ""
        self.all_run_totals = ""
        self.ytd_run_totals = ""
        self.get_stats()

    def get_stats(self):
        session = st.session_state.strava_auth
        data = self.stats_response(session)
        print(data)
        self.recent_run_totals = data["recent_run_totals"]
        self.all_run_totals = data["all_run_totals"]
        self.ytd_run_totals = data["ytd_run_totals"]

    def stats_response(self, session):
        print(st.session_state.athlete.id)
        response = session.get(
            f"https://www.strava.com/api/v3/athlete/{st.session_state.athlete.id}/stats"
        )
        data = response.json()

        return data

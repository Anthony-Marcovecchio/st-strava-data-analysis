import streamlit as st
import pandas as pd


def initialize_models():
    if "athlete" not in st.session_state:
        st.session_state.athlete = athlete()
    # if "athlete_stats" not in st.session_state: # can't get response from stats api endpoint
    #     st.session_state.athlete_stats = athlete_stats()
    if "activities" not in st.session_state:
        st.session_state.activities = activities()


class activities:
    def __init__(self):
        self.activities = []
        self.get_activities()
        self.runs_df = self.process_runs()

    def get_activities(self):
        session = st.session_state.strava_auth
        data = self.get_activities_data(session)
        self.activities = data

    def get_activities_data(self, session):
        response = session.get("https://www.strava.com/api/v3/athlete/activities")
        data = response.json()
        return data

    def process_runs(self):
        runs = []
        for activity in self.activities:
            if activity["type"] == "Run":
                selected_item = {
                    "start_date_local": activity["start_date_local"][:10],
                    "distance": activity["distance"],
                    "moving_time": activity["moving_time"],
                    "elapsed_time": activity["elapsed_time"],
                    "average_speed": activity["average_speed"],
                    "max_speed": activity["max_speed"],
                    "average_heartrate": activity["average_heartrate"],
                    "max_heartrate": activity["max_heartrate"],
                    "total_elevation_gain": activity["total_elevation_gain"],
                }
                runs.append(selected_item)

        # create pandas dataframe
        data = pd.DataFrame(runs)

        # set column data types
        data["start_date_local"] = pd.to_datetime(data["start_date_local"])
        data["distance"] = data["distance"].astype(float)
        data["moving_time"] = data["moving_time"].astype(float)
        data["elapsed_time"] = data["elapsed_time"].astype(float)
        data["average_speed"] = data["average_speed"].astype(float)
        data["max_speed"] = data["max_speed"].astype(float)
        data["average_heartrate"] = data["average_heartrate"].astype(float)
        data["max_heartrate"] = data["max_heartrate"].astype(float)
        data["total_elevation_gain"] = data["total_elevation_gain"].astype(float)

        return data


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

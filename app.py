import streamlit as st
from models import initialize_models
from strava_auth import authentication_needed
from utils import get_url_from_s3
from data import display_training_plan, display_progress_graph


def main():
    athlete = st.session_state.athlete
    if athlete:
        st.write(f" #### 👋 Welcome, {athlete.firstname}")

    tab1, tab2, tab3 = st.tabs(["Current Week", "Full Training Plan", "Progress Graph"])
    with tab1:  # display current week's training plan
        display_training_plan(timerange="current_week")

    with tab2:  # display training plan with Strava data completion
        display_training_plan(timerange="all_weeks")

    with tab3:  # display progress graph
        display_progress_graph()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Percision Training. Powered by Strava.", layout="wide"
    )
    st.title("🏃‍♂️ Percision Training. Powered by Strava.")

    # html to place required Strava logo in bottom right of page
    strava_logo = get_url_from_s3(usage="logo")
    st.markdown(
        f'<img src="{strava_logo}" style="position: fixed; bottom: 0; right: 0; width: 200px;">',
        unsafe_allow_html=True,
    )

    authentication_needed()  # Strava token expires every 6 hours (21600 seconds)

    if "strava_auth" in st.session_state:
        initialize_models()  # initalize users class data
        main()  # main function to display training plan and progress graph

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from utils import get_url_from_s3
from datetime import datetime

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
S3_BUCKET_IMAGE = os.getenv("S3_BUCKET_IMAGE")

REDIRECT_URI = "http://localhost:8501/"
AUTH_URL = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&approval_prompt=auto&scope=activity:write,read"

# STRAVA API GUIDELINES
# https://developers.strava.com/guidelines/


def authentication_needed():
    current_time = datetime.now()

    if "time" in st.session_state:
        # Strava access token expires after 6 hours
        time_difference = current_time - st.session_state.time
        if time_difference.seconds > 21600:
            authenticate()

    elif "strava_auth" not in st.session_state:
        authenticate()


def authenticate():
    try:
        # STRAVA REQUIRED - clickable image button
        # 1.1 Connect with Strava buttons
        image_url = get_url_from_s3(usage="auth")

        content = f"""
            <a href="{AUTH_URL}" id="image_link">
                <img src="{image_url}">
            </a>
        """

        st.markdown(content, unsafe_allow_html=True)

        # Parse query parameters from URL
        query_code = st.query_params.get_all(key="code")

        # Create session variable
        session = strava_oauth_session(query_code)
        if session is not None:
            st.session_state.strava_auth = session
            st.session_state.time = datetime.now()
            st.rerun()

    except Exception as e:
        print(e)


def strava_oauth_session(query_code):
    # If code is present in query parameters, exchange it for an access token
    access_token = exchange_code_for_token(query_code)

    if access_token:
        # Create session variable
        session = OAuth2Session(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            token={"access_token": access_token},
        )

        return session


def exchange_code_for_token(code):
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]

    else:
        print(response.status_code)

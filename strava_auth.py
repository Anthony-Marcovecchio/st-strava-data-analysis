import streamlit as st
import requests
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501/"
AUTH_URL = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&approval_prompt=auto&scope=activity:write,read"


def authenticate():
    if "strava_auth" not in st.session_state:
        if st.link_button("Authenticate with Strava", url=AUTH_URL):
            # Parse query parameters from URL
            query_code = st.query_params.get_all(key="code")

            # Create session variable
            session = strava_oauth_session(query_code)
            if session is not None:
                st.session_state.strava_auth = session
                st.rerun()

        else:
            st.session_state.strava_auth = None


def strava_oauth_session(query_code):
    # Button to initiate Strava authentication

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
        st.write("Failed to obtain access token:", response.text)
import streamlit as st
import requests
import os
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session


# Constants for Strava authentication
# Load environment variables from .env file
load_dotenv()

# Constants for Strava authentication
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = "http://localhost:8501/"


SCOPE = "activity:write,read"
# Strava authorization URL
AUTH_URL = f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&approval_prompt=auto&scope={SCOPE}"


# Main Streamlit app
def strava_oauth_session():
    # Button to initiate Strava authentication
    if st.link_button(label="Authenticate with Strava", url=AUTH_URL):
        # Parse query parameters from URL
        query_params = st.query_params.get_all("code")

        # If code is present in query parameters, exchange it for an access token
        if query_params:
            code = query_params[0]
            access_token = exchange_code_for_token(code)
            if access_token:
                # Create session variable
                session = OAuth2Session(
                    client_id=client_id,
                    redirect_uri=redirect_url,
                    token={"access_token": access_token},
                )

                return session


def get_athlete_data(session):
    response = session.get("https://www.strava.com/api/v3/athlete/")
    data = response.json()
    return data


# Function to exchange authorization code for access token
def exchange_code_for_token(code):
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.write("Failed to obtain access token:", response.text)

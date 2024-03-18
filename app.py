import streamlit as st
import pandas as pd
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

        # display training plan
        display_training_plan(timerange="current_week")


def display_training_plan(timerange):
    plan = pd.read_csv("training_plan.csv")

    plan.rename(
        columns={
            "Start of Week (Day/Month/Year)": "start_of_week",
            "Total Weekly Mileage (km)": "total_week_km",
        },
        inplace=True,
    )

    # strip leading and trailing whitespaces from start_of_week column
    plan["start_of_week"] = plan["start_of_week"].str.strip()

    # replace NaN with REST
    plan.fillna("REST", inplace=True)

    if timerange == "current_week":
        # get start of current week in "day_number month_name" format
        start_of_week = (
            pd.to_datetime("today").to_period("W").start_time.strftime("%d %B")
        )
        plan = plan[plan["start_of_week"] == start_of_week]

        st.markdown(
            '<div style="height: 2px;"></div>'
            '<div style="display: flex;"><div style="width: 200px;">WEEK START</div>\
        <div style="width: 100px;">MON</div>\
           <div style="width: 100px;">TUE</div>\
              <div style="width: 100px;">WED</div>\
                 <div style="width: 100px;">THU</div>\
                    <div style="width: 100px;">FRI</div>\
                       <div style="width: 100px;">SAT</div>\
                          <div style="width: 100px;">SUN</div>\
        <div style="width: 50px;">TOTAL</div>\
        <div style="height: 30px;"></div>',
            unsafe_allow_html=True,
        )

        # st markdown a horizontal bar
        st.markdown(
            '<div style="height: 2px; background-color: black;"></div>',
            unsafe_allow_html=True,
        )

    for _, row in plan.iterrows():
        start_of_week = row["start_of_week"]
        mon_km = row["Monday"]
        tue_km = row["Tuesday"]
        wed_km = row["Wednesday"]
        thu_km = row["Thursday"]
        fri_km = row["Friday"]
        sat_km = row["Saturday"]
        sun_km = row["Sunday"]
        total_week_km = row["total_week_km"]

        st.markdown(
            '<div style="height: 2px;"></div>'
            f'<div style="display: flex;"><div style="width: 200px;">{start_of_week}</div>\
        <div style="width: 100px;">{mon_km}</div>\
           <div style="width: 100px;">{tue_km}</div>\
              <div style="width: 100px;">{wed_km}</div>\
                 <div style="width: 100px;">{thu_km}</div>\
                    <div style="width: 100px;">{fri_km}</div>\
                       <div style="width: 100px;">{sat_km}</div>\
                          <div style="width: 100px;">{sun_km}</div>\
        <div style="width: 50px;">{total_week_km}</div>\
        <div style="height: 30px;"></div>',
            unsafe_allow_html=True,
        )


app()

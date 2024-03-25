import pandas as pd
import streamlit as st


def display_progress_graph():
    # pull strava/plan data
    strava_runs = st.session_state.activities.runs_df
    plan = pd.read_csv("training_plan.csv")

    # setup columns for join
    plan.rename(
        columns={
            "Start of Week (Day/Month/Year)": "start_of_week",
            "Total Weekly Mileage (km)": "total_week_km",
        },
        inplace=True,
    )
    plan["start_of_week"] = plan["start_of_week"].str.strip()

    # convert plan start_of_week to datetime
    plan["start_of_week_dt"] = pd.to_datetime(
        plan["start_of_week"] + " " + str(pd.to_datetime("today").year)
    )

    # add week_number-year column to plan and strava_runs
    plan["week_number"] = plan["start_of_week_dt"].dt.isocalendar().week
    strava_runs["week_number"] = strava_runs["start_date_local"].dt.isocalendar().week

    # merge plan and strava_runs on week_number
    merged = pd.merge(
        plan,
        strava_runs,
        how="left",
        on="week_number",
        suffixes=("_plan", "_strava"),
    )

    # group by start_of_week and sum distance
    merged = merged.groupby("start_of_week").agg(
        {
            "start_of_week": "first",
            "total_week_km": "first",
            "distance": "sum",
            "week_number": "first",
        }
    )

    # drop where distance is NaN or 0
    merged = merged[merged["distance"].notna()]
    merged = merged[merged["distance"] != 0]

    # divide by 1000 to convert to km
    merged["distance"] = merged["distance"] / 1000

    # rename x columns
    merged.rename(
        columns={
            "distance": "Strava KM",
            "total_week_km": "Plan KM",
        },
        inplace=True,
    )

    # sort by week_number
    current_year = pd.to_datetime("today").year
    merged["start_of_week"] = pd.to_datetime(
        merged["start_of_week"] + " " + str(current_year), format="%d %B %Y"
    )

    # convert start_of_week to string in mm/dd format
    merged["Start of Week"] = merged["start_of_week"].dt.strftime("%m/%d")

    # data up to current week only, based on week number
    current_week = pd.to_datetime("today").week + 1
    merged = merged[merged["week_number"] <= current_week]

    st.line_chart(
        data=merged,
        x="Start of Week",
        y=["Plan KM", "Strava KM"],
        color=["#0276fd", "#fc4c02"],
    )


def display_training_plan(timerange):
    plan = pd.read_csv("training_plan.csv")
    runs_df = st.session_state.activities.runs_df

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

    col1, col2 = st.columns([4, 1])

    with col1:
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
            <div style="width: 25px;"></div>\
            <div style="width: 150px; "><b>PLANNED</b></div>\
            <div style="width: 150px; color: #fc4c02;"><b>STRAVA</b></div>\
            <div style="width: 150px;"><b>COMPLETION</b></div>\
            <div style="height: 30px;"></div>',
            unsafe_allow_html=True,
        )

        # st markdown a horizontal bar
        st.markdown(
            '<div style="height: 2px; background-color: black;"></div>',
            unsafe_allow_html=True,
        )

        for _, row in plan.iterrows():
            # PLAN DATA
            start_of_week = row["start_of_week"]
            mon_km = row["Monday"]
            tue_km = row["Tuesday"]
            wed_km = row["Wednesday"]
            thu_km = row["Thursday"]
            fri_km = row["Friday"]
            sat_km = row["Saturday"]
            sun_km = row["Sunday"]
            total_week_km = row["total_week_km"]

            # convert to float if not REST
            mon_km = float(mon_km) if mon_km != "REST" else mon_km
            tue_km = float(tue_km) if tue_km != "REST" else tue_km
            wed_km = float(wed_km) if wed_km != "REST" else wed_km
            thu_km = float(thu_km) if thu_km != "REST" else thu_km
            fri_km = float(fri_km) if fri_km != "REST" else fri_km
            sat_km = float(sat_km) if sat_km != "REST" else sat_km
            sun_km = float(sun_km) if sun_km != "REST" else sun_km

            # STRAVA DATA
            # using start_of_week as 'day month' format + current year, find the associated
            # strava run from runs_df in 'yyyy-mm-dd' format
            row_date = pd.to_datetime(
                f"{start_of_week} {pd.to_datetime('today').year}", format="%d %B %Y"
            )

            # get week number from start_of_week (starting from Monday)
            row_week_number = row_date.week
            # compare to current day week number
            curr_week_number = pd.to_datetime("today").week

            curr_run_week = True if row_week_number == curr_week_number else False
            next_run_week = True if row_week_number == curr_week_number + 1 else False

            # create dates for each weekday in 'yyyy-mm-dd' format
            monday_date = (row_date + pd.DateOffset(days=0)).date()
            tuesday_date = (row_date + pd.DateOffset(days=1)).date()
            wednesday_date = (row_date + pd.DateOffset(days=2)).date()
            thursday_date = (row_date + pd.DateOffset(days=3)).date()
            friday_date = (row_date + pd.DateOffset(days=4)).date()
            saturday_date = (row_date + pd.DateOffset(days=5)).date()
            sunday_date = (row_date + pd.DateOffset(days=6)).date()

            # get strava data for each weekday
            mon_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == monday_date
            ]
            tue_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == tuesday_date
            ]
            wed_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == wednesday_date
            ]
            thu_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == thursday_date
            ]
            fri_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == friday_date
            ]
            sat_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == saturday_date
            ]
            sun_strava_data = runs_df[
                runs_df["start_date_local"].dt.date == sunday_date
            ]

            # get total km for each weekday
            mon_strava_km = (
                mon_strava_data["distance"].sum() if not mon_strava_data.empty else 0
            )
            tue_strava_km = (
                tue_strava_data["distance"].sum() if not tue_strava_data.empty else 0
            )
            wed_strava_km = (
                wed_strava_data["distance"].sum() if not wed_strava_data.empty else 0
            )
            thu_strava_km = (
                thu_strava_data["distance"].sum() if not thu_strava_data.empty else 0
            )
            fri_strava_km = (
                fri_strava_data["distance"].sum() if not fri_strava_data.empty else 0
            )
            sat_strava_km = (
                sat_strava_data["distance"].sum() if not sat_strava_data.empty else 0
            )
            sun_strava_km = (
                sun_strava_data["distance"].sum() if not sun_strava_data.empty else 0
            )

            def set_colour_codes(strava_km, plan_km):
                # set colour as purple if next run week from current week
                if curr_run_week and strava_km == 0:
                    return "white"
                elif next_run_week:
                    return "#8A2BE2"
                if plan_km == "REST" and strava_km > 0:
                    return "#0276fd"
                elif plan_km == "REST":
                    return "grey"
                elif strava_km >= plan_km:
                    return "green"
                elif row_date.date() > pd.to_datetime("today").date():
                    return "grey"
                else:
                    return "#FFC300"

            # set colours codes for each weekday if strava_km >= plan_km
            mon_colour = set_colour_codes(mon_strava_km, mon_km)
            tue_colour = set_colour_codes(tue_strava_km, tue_km)
            wed_colour = set_colour_codes(wed_strava_km, wed_km)
            thu_colour = set_colour_codes(thu_strava_km, thu_km)
            fri_colour = set_colour_codes(fri_strava_km, fri_km)
            sat_colour = set_colour_codes(sat_strava_km, sat_km)
            sun_colour = set_colour_codes(sun_strava_km, sun_km)

            # calculate total KM
            total_week_strava_km = round(
                (
                    mon_strava_km
                    + tue_strava_km
                    + wed_strava_km
                    + thu_strava_km
                    + fri_strava_km
                    + sat_strava_km
                    + sun_strava_km
                )
                / 1000,
                2,
            )

            total_week_colour = set_colour_codes(total_week_strava_km, total_week_km)

            if row_date.date() <= pd.to_datetime("today").date():
                completion_percent = (
                    f"{round((total_week_strava_km / total_week_km) * 100, 1)}%"
                )
            else:
                completion_percent = "--"
                total_week_strava_km = "--"

            st.markdown(
                f'<div style="display: flex;"><div style="width: 200px;">{start_of_week}</div>\
                <div style="width: 100px; color: {mon_colour};">{mon_km}</div>\
                <div style="width: 100px; color: {tue_colour};">{tue_km}</div>\
                <div style="width: 100px; color: {wed_colour};">{wed_km}</div>\
                <div style="width: 100px; color: {thu_colour};">{thu_km}</div>\
                <div style="width: 100px; color: {fri_colour};">{fri_km}</div>\
                <div style="width: 100px; color: {sat_colour};">{sat_km}</div>\
                <div style="width: 100px; color: {sun_colour};">{sun_km}</div>\
                <div style="width: 2px; background-color: black;"></div>\
                <div style="width: 25px;"></div>\
                <div style="width: 150px; color: {total_week_colour};"><b>{total_week_km}</b></div>\
                <div style="width: 150px; color: {total_week_colour};"><b>{total_week_strava_km}</b></div>\
                <div style="width: 150px; color: {total_week_colour};"><b>{completion_percent}</b></div>',
                unsafe_allow_html=True,
            )

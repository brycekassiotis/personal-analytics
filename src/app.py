import pandas as pd
import streamlit as st
from main import read_data, add_data
from plots import plot_menu
from analysis import analysis_menu
from variables import variables_menu
from helpers import refresh_data

st.markdown(
    """
    <style>
    /* Hide the anchor link icon entirely */
    .st-emotion-cache-17lntkn a {
        display: none !important;
    }
    .st-emotion-cache-6qob1r a {
        display: none !important;
    }
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Personal Analytics", layout="wide")
st.title("Personal Analytics Dashboard")

# Load data
df, csv_data = read_data()

# Tabs
tab_collect, tab_stats, tab_settings = st.tabs(["Collect", "Stats", "Settings"])

# --- Collect Tab: Add Data ---
with tab_collect:
    st.header("Add Today's Data")
    
    with st.form("collect_form"):
        sleep_hours = st.number_input("Hours slept", min_value=0.0, max_value=24.0)
        sleep_quality = st.slider("Sleep quality (1-10)", 1, 10)
        exercise = st.checkbox("Did you exercise today?")
        steps = st.number_input("Steps", min_value=0)
        calories = st.number_input("Calories consumed", min_value=0)
        productivity = st.slider("Productivity (1-10)", 1, 10)
        stress = st.slider("Stress (1-10)", 1, 10)
        day_rating = st.slider("Day rating (1-10)", 1, 10)
        mood = st.slider("Mood (1-10)", 1, 10)
        screen_time = st.number_input("Screen time (hours)", min_value=0.0)
        social = st.slider("Socialness (1-10)", 1, 10)
        notes = st.text_area("Notes")
        creatine = st.checkbox("Took Creatine")
        vitamin_d = st.checkbox("Took Vitamin D")
        magnesium = st.checkbox("Took Magnesium")
        
        submitted = st.form_submit_button("Add Data")
        
        if submitted:
            date_obj = pd.to_datetime(pd.Timestamp.today().date())
            values = [
                date_obj, sleep_hours, sleep_quality, steps, exercise, calories,
                productivity, stress, day_rating, mood, screen_time,
                None, None, None, date_obj.strftime("%A"), social,
                notes, creatine, vitamin_d, magnesium
            ]
            df = add_data(df, csv_data, manual_values=values)
            st.success("Data added!")

# --- Stats tab ---
with tab_stats:
    st.header("Stats")

    stats_subtab = st.radio("Select View", ["Plots", "Analysis"], horizontal=True)

    if stats_subtab == "Plots":
        st.subheader("Plots")
        plot_menu(df, streamlit=True)

    elif stats_subtab == "Analysis":
        st.subheader("Analysis")
        analysis_menu(df, streamlit=True)

# --- Settings Tab ---
with tab_settings:
    st.header("Settings")
    
    st.write("Manage variables and preferences here.")
    
    if st.button("Refresh Data from Google Sheet"):
        df = refresh_data(csv_data)
        st.success("Data refreshed!")
    
    if st.button("Edit Variables"):
        variables_menu(streamlit=True)  # You’d adapt your variables menu to Streamlit
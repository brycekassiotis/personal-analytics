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


# Load data, support demo mode
import os

# Demo mode toggle logic (for instant feedback)
if 'offline_mode' not in st.session_state:
    # default to offline if credentials.json is missing
    try:
        has_creds = pd.io.common.file_exists('credentials.json')
    except Exception:
        has_creds = False
    st.session_state.offline_mode = not has_creds

offline = st.session_state.offline_mode

# Show demo info popup instantly when toggled
if offline:
    st.info('Demo mode is enabled. You are using sample data and changes will not be saved to Google Sheets.')
    df = pd.read_csv('demo_data.csv')
    csv_data = 'demo_data.csv'
else:
    df, csv_data = read_data()

# Tabs
tab_collect, tab_stats, tab_settings = st.tabs(["Collect", "Stats", "Settings"])

# Collect tab
with tab_collect:
    st.header("Add Today's Data")
    
    # --- Sliders first (0-10) ---
    # make sliders fluid (allow two decimal places)
    sleep_quality = st.slider("Sleep quality (0-10)", 0.0, 10.0, step=0.01)
    productivity = st.slider("Productivity (0-10)", 0.0, 10.0, step=0.01)
    stress = st.slider("Stress (0-10)", 0.0, 10.0, step=0.01)
    day_rating = st.slider("Day rating (0-10)", 0.0, 10.0, step=0.01)
    mood = st.slider("Mood (0-10)", 0.0, 10.0, step=0.01)
    social = st.slider("Socialness (0-10)", 0.0, 10.0, step=0.01)

    # --- Numeric inputs next (order: hours slept, screen time, steps, calories) ---
    sleep_hours = st.number_input("Hours slept", min_value=0.0, max_value=24.0, step=1.0)
    screen_time = st.number_input("Screen time (hours)", min_value=0.0, step=1.0)
    steps = st.number_input("Steps", min_value=0, step=100)
    calories = st.number_input("Calories consumed", min_value=0, step=100)

    # --- Booleans ---
    # Place booleans outside a form so they update immediately when toggled
    exercise_bool = st.checkbox("Did you exercise today?")
    exercise_text = ''
    if exercise_bool:
        exercise_text = st.text_input("Exercise type (e.g., legs, push, pull)")

    creatine = st.checkbox("Took Creatine")
    vitamin_d = st.checkbox("Took Vitamin D")
    magnesium = st.checkbox("Took Magnesium")

    # --- Notes at the bottom ---
    notes = st.text_area("Notes")

    # Submit button
    submitted = st.button("Add Data")

    if submitted:
        # ensure exercise has a sensible fallback if checkbox was checked but no text provided
        if exercise_bool and (exercise_text is None or str(exercise_text).strip() == ""):
            exercise_val = 'other'
        elif exercise_bool:
            exercise_val = exercise_text
        else:
            exercise_val = 'rest'

        date_obj = pd.to_datetime(pd.Timestamp.today().date())

        # Build a mapping of column -> value and then order it to match df.columns
        col_map = {
            'date': date_obj,
            'sleep_hours': sleep_hours,
            'sleep_quality': sleep_quality,
            'steps': steps,
            'exercise': exercise_val,
            'calories': calories,
            'productivity': productivity,
            'stress': stress,
            'day_rating': day_rating,
            'mood': mood,
            'screen_time': screen_time,
            # placeholder min/max temp and weather handled by None if not present
            'weather': None,
            'day_of_week': date_obj.strftime("%A"),
            'social': social,
            'notes': notes,
            'creatine': creatine,
            'vitamin_d': vitamin_d,
            'magnesium': magnesium,
            'min_temp': None,
            'max_temp': None
        }

        ordered_values = [col_map.get(c, None) for c in df.columns]

        df = add_data(df, csv_data, manual_values=ordered_values)
        st.success("Data added!")

# Stats tab
with tab_stats:
    st.header("Stats")

    stats_subtab = st.radio("Select View", ["Plots", "Analysis"], horizontal=True)

    if stats_subtab == "Plots":
        st.subheader("Plots")
        plot_menu(df, streamlit=True)

    elif stats_subtab == "Analysis":
        st.subheader("Analysis")
        analysis_menu(df, streamlit=True)

# Settings tab
with tab_settings:
    st.header("Settings")
    
    st.write("Manage variables and preferences here.")


    # Offline / Demo Mode toggle (instant update)
    offline = st.checkbox("Offline / demo mode (disable Google Sheets)", value=st.session_state.offline_mode, key="offline_mode")
    # The checkbox automatically updates st.session_state.offline_mode via the key parameter
    os.environ['PERSONAL_ANALYTICS_OFFLINE'] = '1' if st.session_state.offline_mode else '0'

    if st.button("Refresh Data from Google Sheet", disabled=st.session_state.offline_mode):
        df = refresh_data(csv_data)
        st.success("Data refreshed!")

    # if st.button("Edit Variables", disabled=st.session_state.offline_mode):
    #     variables_menu(df, csv_data, streamlit=True)
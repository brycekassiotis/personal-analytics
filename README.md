## personal-analytics

A Python-based system for tracking and analyzing daily habits to explore how factors of lifestyle impact productivity, mood, and well-being.

There are multiple ways to collect daily metrics for the project. For practicality, each night I have an iPhone automation trigger, surveying me for data, then activating a Make.com workflow that logs daily metrics into Google Sheets. This includes data that is both self-reported (e.g., mood rating, stress level) and automated (e.g., steps, hours slept).

The data is then synced to a Google Sheet and analyzed locally with Python, allowing for visualization, pattern detection, and deeper insights over time.


## Features:
- Multiple data entry options: Streamlit UI, terminal interface, or automated iPhone triggers
- Streamlit dashboard: Interactive web-based UI for manual data entry and real-time visualization
- Visual analysis & plotting tools for exploring trends
- Local syncing and data backup with live Google Sheets integration


## Installation
Clone the repo and install dependencies:
```powershell
git clone https://github.com/brycekassiotis/personal-analytics.git
cd personal-analytics
pip install -r requirements.txt

# Offline demo and demo data

This project supports an offline/demo mode so anyone can run the Streamlit demo without Google Sheets credentials.

- To run the demo without Google Sheets, open the app's Settings tab and enable the "Offline / demo mode" checkbox

Demo data is provided at the repository root as `demo_data.csv`. To run the demo with the bundled data (so you don't need to connect Google Sheets), copy it into the `data/` folder and then run Streamlit:

Example:

```powershell
# copy demo data into the tracked data location
Copy-Item .\demo_data.csv .\data\data.csv -Force

# run the Streamlit app
streamlit run src/app.py
```


## Notes:
- The app will warn and skip Google Sheets sync while offline mode is enabled. You can toggle offline mode back off and provide `credentials.json` (a Google service account) to re-enable syncing.
- Keep any real credentials out of version control — they're ignored via `.gitignore` and you should supply them locally for syncing


## Tech Stack
- Python: For data analysis, visualization, and local syncing
- Streamlit: For building an interactive web-based data entry and visualization dashboard
- Pandas & Matplotlib: For data manipulation and visualization
- Google Sheets API: For cloud-based data storage and real-time syncing
- Make.com: For workflow automation and webhook processing
- iPhone Shortcuts: For automated daily data collection triggers

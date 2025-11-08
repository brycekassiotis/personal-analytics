## personal-analytics

A Python-based system for tracking and analyzing daily habits to explore how factors of lifestyle impact productivity, mood, and well-being.

Each night, an iPhone automation triggers, surveying me for data, then triggering a Make.com workflow that logs daily metrics into Google Sheets. This includes self-reported (e.g., mood rating, stress level, calories consumed) and automated (e.g., steps, hours slept, weather) data.

The data is then synced and analyzed locally with Python, allowing for visualization, pattern detection, and deeper insights over time.


## Features:
- Automated data collection via iPhone -> Make.com webhook -> Google Sheets
- Early visual analysis & plotting tools for exploring trends
- Local syncing and data backup with live Google Sheets integration
- Dynamic variable management: add, remove, or edit variables easily

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
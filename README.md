# personal-analytics
A Python-based system for tracking and analyzing daily habits to explore how factors of lifestyle impact productivity, mood, and well-being.

Each night, an iPhone automation triggers, surveying me for data, then triggering a Make.com workflow that logs daily metrics into Google Sheets. This includes self-reported (e.g., mood rating, stress level, calories consumed) and automated (e.g., steps, hours slept, weather) data.

The data is then synced and analyzed locally with Python, allowing for visualization, pattern detection, and deeper insights over time.


Features:
- Automated data collection via iPhone -> Make.com webhook -> Google Sheets
- Early visual analysis & plotting tools for exploring trends
- Local syncing and data backup with live Google Sheets integration
- Dynamic variable management: add, remove, or edit variables easily
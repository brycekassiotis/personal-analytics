variables = {
    "sleep_hours": {"label": "Sleep Hours", "type": "numeric"},
    "sleep_quality": {"label": "Sleep Quality", "type": "numeric"},
    "steps": {"label": "Steps", "type": "numeric"},
    "exercise": {"label": "Exercise", "type": "boolean"},
    "calories": {"label": "Calories", "type": "numeric"},
    "productivity": {"label": "Productivity", "type": "numeric"},
    "stress": {"label": "Stress", "type": "numeric"},
    "day_rating": {"label": "Day Rating", "type": "numeric"},
    "mood": {"label": "Mood", "type": "numeric"},
    "screen_time": {"label": "Screen Time", "type": "numeric"},
    "avg_temp": {"label": "Average Temperature", "type": "numeric"},
    "weather": {"label": "Weather", "type": "text"},
    "day_of_week": {"label": "Day of Week", "type": "text"},
    "social": {"label": "Socialness", "type": "numeric"},
    "notes": {"label": "Notes", "type": "text"}
}

# used for menus
def get_numeric_variables():
    numeric_variables = {}

    i = 0

    for key, val in variables.items():
        if val['type'] == 'numeric':
            i+=1
            numeric_variables[i] = key

    return numeric_variables

# used for dataframes
def get_numeric_keys():
    numeric_variables = {}

    i = 0

    for key, val in variables.items():
        if val['type'] == 'numeric':
            i+=1
            numeric_variables[i] = key

    return numeric_variables
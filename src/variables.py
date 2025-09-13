variables = {
    "sleep_hours": {"label": "Sleep Hours", "type": "numeric"},
    "sleep_quality": {"label": "Sleep Quality", "type": "numeric"},
    "calories": {"label": "Calories", "type": "numeric"},
    "productivity": {"label": "Productivity", "type": "numeric"},
    "stress": {"label": "Stress", "type": "numeric"},
    "exercise": {"label": "Exercise", "type": "boolean"},
}

# used for menus
def get_numeric_variables():
    numeric_variables = {}

    i = 0

    for key, val in variables.items():
        if val['type'] == 'numeric':
            i+=1
            numeric_variables[i] = val['label']

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
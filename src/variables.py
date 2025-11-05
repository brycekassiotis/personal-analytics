import pandas as pd
import gspread
from main import push_to_sheet, sync_sheet
from helpers import pick_var

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


def variables_menu(df):

    # loop until user quits
    while True:
        inp = input('\nSelect: \n'
        '1. View variables \n'
        '2. Add new variable \n'
        '3. Edit variable\n'
        '4. Quit \n'
        '\nNumber: ')

        if inp == '1':
            print("\nCurrent Variables:\n")
            for key, val in variables.items():
                print(f"- {val['label']} ({val['type']})\n")
        elif inp == '2':
            add_variable(df)
        elif inp == '3':
            edit_variable(df)
        elif inp == '4':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


# to add new variable
def add_variable(df, csv_data):
    key = input("Enter the variable key: ").strip()
    if key in variables:
        print("This variable key already exists.")
        return df
    
    label = input("Enter the display label for the variable: ").strip()
    var_type = input("Enter the variable type (numeric, text, boolean): ").lower().strip()
    if var_type not in ["numeric", "text", "boolean"]:
        print("Invalid type.")
        return df

    # add var to dict
    variables[key] = {"label": label, "type": var_type}
    
    # add col to df
    df[key] = ''

    df.to_csv(csv_data, index=False)
    push_to_sheet(df)

    print(f"Variable '{label}' added successfully!")
    return df


def edit_variable(df, csv_data):
    selected_key = pick_var("Select variable number to edit: ")
    if selected_key is None: return df

    selected_var = variables[selected_key]

    print(f"\nEditing '{selected_var['label']}' ({selected_var['type']})")
    print("Options:\n1. Edit label\n2. Edit type\n3. Delete variable\n4. Cancel")
    action = input("Select option: ").strip()

    if action == "1":
        new_label = input("Enter new label: ").strip()
        variables.variables[selected_key]['label'] = new_label
        print("Label updated.")

    elif action == "2":
        new_type = input("Enter new type (numeric, text, boolean): ").strip().lower()
        if new_type in ["numeric", "text", "boolean"]:
            variables.variables[selected_key]['type'] = new_type
            print("Type updated.")
        else:
            print("Invalid type!")
            return df

    elif action == "3":
        confirm = input(f"Are you sure you want to delete '{selected_var['label']}'? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            if selected_key in df.columns:
                df.drop(columns=[selected_key], inplace=True)
            del variables.variables[selected_key]
            print("Variable deleted.")
        else:
            print("Delete cancelled.")
            return df

    elif action == "4":
        print("Cancelled.")
        return df
    else:
        print("Invalid option.")
        return df

    # Save CSV and push changes to Google Sheet
    df.to_csv(csv_data, index=False)
    from main import push_to_sheet
    push_to_sheet(df)

    return df

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
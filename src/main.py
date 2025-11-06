import os
import pandas as pd
from datetime import datetime
import plots
import analysis
import variables
import helpers

# setting directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'data.csv')


def main():
    df, csv_data = read_data()
    df = helpers.sync_sheet(csv_data, sheet_name='Daily Analytics')
    return df, csv_data

columns = list(variables.variables.keys())

numeric_columns = list(variables.get_numeric_keys().values())

def menu(df, csv_data):

    while True:
        inp = input("Select: \n"
        "1. Add today's data \n"
        "2. Show past week's data \n"
        "3. Plot menu\n"
        "4. Analysis menu\n"
        "5. Variables menu\n"
        "6. Quit\n\n"
        "Number: ")

        if inp == '1':
            add_data(df, csv_data)
        elif inp == '2':
            show_week(df, csv_data)
        elif inp == '3':
            plots.plot_menu(df)
        elif inp == '4':
            df = analysis.analysis_menu(df)
        elif inp == '5':
            variables.variables_menu()
        elif inp == '6':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


def get_user_input(df):

    date_obj = datetime.now().date()
    
    # loop for sleep hours
    while True:
        try:
            sleep_hours = float(input('How many hours did you sleep? '))
            if sleep_hours < 0 or sleep_hours > 24:
                print('Please enter a valid number.')
                continue
            break
        except ValueError:
            print('Please enter a valid number.')

    sleep_quality = rating_helper('Rate your sleep quality 1 to 10: ')
    
    # loop for exercise boolean
    exercise_bool = helpers.get_bool("Did you exercise today?")
    
    steps = input('How many steps did you take today? ')
    calories = number_helper('How many calories did you consume today? ')
    productivity = rating_helper('Rate your productivity today 1 to 10: ')
    stress = rating_helper('Rate your stress levels today 1 to 10: ')
    day_rating = rating_helper('Rate your day today 1 to 10: ')
    mood = rating_helper('Rate your mood today 1 to 10: ')
    screen_time = rating_helper('How many hours of screen time did you have today? ')
    min_temp = None
    max_temp = None
    weather = None
    day_of_week = date_obj.strftime("%A")
    social = rating_helper("How social were you today from 1 to 10: ")
    notes = input('Notes: ')
    creatine = helpers.get_bool("Did you take creatine today?")
    vitamin_d = helpers.get_bool("Did you take vitamin D today?")
    magnesium = helpers.get_bool("Did you take magnesium today?")

    return [date_obj, sleep_hours, sleep_quality, steps, exercise_bool, calories, productivity, stress, 
            day_rating, mood, screen_time, min_temp, max_temp, weather, day_of_week, social, notes, creatine, vitamin_d, magnesium]


# Rating helper to check if value is within 0-10
def rating_helper(prompt):
    while True:
        try:
            inp = float(input(prompt))
            if inp < 0 or inp > 10:
                print('Please enter a number from 0 to 10.')
                continue
            return inp
        except ValueError:
            print('Please enter a number from 0 to 10.')

# Number helper to check if value is a float
def number_helper(prompt):
    while True:
        try:
            inp = float(input(prompt))
            if inp < 0:
                print('Please enter a valid number.')
                continue
            return inp
        except ValueError:
            print('Please enter a valid number.')


def read_data():
    csv_data = CSV_PATH
    data_dir = os.path.join(BASE_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    variable_keys = [k for k in variables.variables.keys() if k != 'date']
    initial_columns = ['date'] + variable_keys

    if not os.path.exists(csv_data):
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(columns=initial_columns)
        df.to_csv(csv_data, index=False)
    else:
        df = pd.read_csv(csv_data)
        for col in variable_keys:
            if col not in df.columns:
                df[col] = None
        df['date'] = pd.to_datetime(df['date'])

    return df, csv_data


def add_data(df, csv_data, manual_values=None):

    # if manual values provided from Streamlit, use those
    if manual_values is not None:
        values = manual_values
        date_obj = pd.to_datetime(values[0])
    else:
        # CLI mode — get values interactively
        values = get_user_input(df)
        if values is None:
            return df
        date_obj = pd.to_datetime(values[0])
        
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # if overwritten replace old data
    if date_obj in df['date'].values:
        index = df.index[df['date'] == date_obj][0]
        df.loc[index, df.columns[1:]] = values[1:]

    # make and add new row otherwise
    else:
        new_row = pd.DataFrame([values], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)

    # sort by date
    df.sort_values('date', inplace=True)

    # update csv
    df.to_csv(csv_data, index=False)
    helpers.push_to_sheet(df)

    return df


# Shows last 7 days of data
def show_week(df, csv_data):
    from variables import get_numeric_keys  # ensure access

    # Convert date column safely
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Filter last 7 days
    df_last_week = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]

    # Get numeric columns dynamically
    numeric_columns = list(get_numeric_keys().values())

    # Convert numeric columns to numbers (ignore errors)
    df_last_week[numeric_columns] = df_last_week[numeric_columns].apply(
        pd.to_numeric, errors='coerce'
    )

    # Print averages cleanly
    print("Last week's averages:")
    averages = df_last_week[numeric_columns].mean()

    for col, val in averages.items():
        print(f"{col}: {val:.2f}")

    print("\nRaw last 7 days:")
    print(df_last_week)



if __name__ == '__main__':
    df, csv_data = main()
    menu(df, csv_data)
    
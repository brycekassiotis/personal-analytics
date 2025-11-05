import os
import pandas as pd
from datetime import datetime
import gspread
import plots
import analysis
import variables
import supplements
from google.oauth2.service_account import Credentials

# setting directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'data.csv')


def main():
    df, csv_data = read_data()
    df = sync_sheet(csv_data, sheet_name='Daily Analytics')
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
        "5. Supplements menu\n"
        "6. Variables menu\n"
        "7. Quit\n\n"
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
            supplements.supplements_menu()
        elif inp == '6':
            variables.variables_menu()
        elif inp == '7':
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
    while True:
        exercise_inp = str(input('Did you exercise yesterday? (y/n) ')).lower()
        if exercise_inp in ('y', 'yes'):
            exercise_bool = True
            break
        elif exercise_inp in ('n', 'no'):
            exercise_bool = False
            break
        else:
            print('Please enter (y/n).')
    
    steps = input('How many steps did you take today? ')
    calories = number_helper('How many calories did you consume today? ')
    productivity = rating_helper('Rate your productivity today 1 to 10: ')
    stress = rating_helper('Rate your stress levels today 1 to 10: ')
    day_rating = rating_helper('Rate your day today 1 to 10: ')
    mood = rating_helper('Rate your mood today 1 to 10: ')
    screen_time = rating_helper('How many hours of screen time did you have today? ')
    avg_temp = None
    weather = None
    day_of_week = date_obj.strftime("%A")
    social = rating_helper("How social were you today from 1 to 10: ")
    notes = input('Notes: ')

    # supplements
    sups = supplements.load_supplements()
    supplement_values = []

    if sups:
        print("\n--- Supplements ---")

        for name, info in sups.items():
            label = info['label']
            sup_type = info['type']

            if sup_type == 'boolean':
                while True:
                    val = input(f'{label} (y/n): ').lower().strip()
                    if val in ('y', 'yes'):
                        supplement_values.append(True)
                        break
                    elif val in ('n', 'no'):
                        supplement_values.append(False)
                        break
                    else:
                        print('Please enter (y/n).')
            
            elif sup_type == 'numeric':
                while True:

                    try:
                        val = float(input(f'{label}: '))
                        supplement_values.append(val)
                        break
                    except ValueError:
                        print ('Please enter a valid number.')
    else:
        print('\nNo supplements.')

    return [date_obj, sleep_hours, sleep_quality, steps, exercise_bool, calories, productivity, stress, 
            day_rating, mood, screen_time, avg_temp, weather, day_of_week, social, notes, *supplement_values]


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
    if not os.path.exists(csv_data):
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(columns=list(variables.variables.keys()))
        df.to_csv(csv_data, index=False)
    else:
        df = pd.read_csv(csv_data)
        for col in list(variables.variables.keys()):
            if col not in df.columns:
                df[col] = None
        df['date'] = pd.to_datetime(df['date'])

    supplements.check_supplement_columns(csv_data)

    return df, csv_data


def read_google_sheet(sheet_name, creds_path="credentials.json"):
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df


# helper that allows me to add data from both the automation and manually
def sync_sheet(csv_data, sheet_name='Daily Analytics'):
    try:
        sheet_df = read_google_sheet(sheet_name, creds_path="credentials.json")

        # read the csv if it exists
        if os.path.exists(csv_data):
            local_df = pd.read_csv(csv_data)
            local_df['date'] = pd.to_datetime(local_df['date'])
        else:
            local_df = pd.DataFrame(columns=list(variables.variables.keys()))
        
        # merge by date to only keep new rows from the sheet
        combined_df = pd.concat([local_df, sheet_df]).drop_duplicates(subset=['date'], keep='last')

        combined_df.sort_values('date', inplace=True)
        combined_df.to_csv(csv_data, index=False)

        new_rows = len(combined_df) - len(local_df)
        if new_rows > 0:
            print(f"Synced {new_rows} new rows from Google Sheet.")
        else:
            print('No new data to sync.')

        return combined_df
    
    except Exception as e:
        print(f"Could not sync from Google Sheet: {e}")
        return pd.read_csv(csv_data) if os.path.exists(csv_data) else pd.DataFrame(columns=list(variables.variables.keys()))

# Pushes the changes made to google sheet
def push_to_sheet(df, sheet_name='Daily Analytics', creds_file='credentials.json'):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(creds_file, scopes=scope)
        client = gspread.authorize(creds)

        sheet = client.open(sheet_name).sheet1
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())

        print("Uploaded latest data to Google Sheet.")
    except Exception as e:
        print(f"Could not push data to Google Sheet: {e}")


def add_data(df, csv_data):

    # check supplements
    supplements.check_supplement_columns(csv_data)

    # add row for today
    values = get_user_input(df)
    if values is None:
        return df
    date_obj = values[0]

    # if overwritten replace old data
    if date_obj in df['date'].values:
        index = df.index[df['date'] == date_obj][0]
        df.loc[index, df.columns[1:]] = values[1:]

    # make and add new row otherwise
    else:
        new_row = [date_obj] + values[1:]
        df.loc[len(df)] = new_row

    # sort by date
    df.sort_values('date', inplace=True)

    # update csv
    df.to_csv(csv_data, index=False)
    push_to_sheet(df)

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

    
    
# Helper to refresh and add new data
def refresh_data(csv_data):
    supplements.check_supplement_columns(csv_data)
    return sync_sheet(csv_data, sheet_name='Daily Analytics')




if __name__ == '__main__':
    df, csv_data = main()
    menu(df, csv_data)
    
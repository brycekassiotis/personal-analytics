import os
import variables
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

# Helper to refresh and add new data
def refresh_data(csv_data):
    return sync_sheet(csv_data, sheet_name='Daily Analytics')

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

# Helper to read the sheet
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


# helper to pick variables
def pick_var(var_question, df=None, streamlit=False):
    
    if streamlit and df is not None:
        return st.selectbox(var_question, df.columns)

    numeric_vars = variables.get_numeric_keys()
    
    print(f'{var_question}\n')


    for i, key in numeric_vars.items():
        print(f"{i}. {variables.variables[key]['label']}")

    print(f"{len(numeric_vars) + 1}. Quit\n")

    inp = input('Number: ').strip()
    
    try:
        ind = int(inp)
        if ind == len(numeric_vars) + 1:
            print('Quitting...')
            return None
        if ind not in numeric_vars:
            print('Please enter a valid option.')
            return None
    except ValueError:
        print('Please enter a valid option.')
        return None
        
    print(f'\nSelected {numeric_vars[ind].replace("_", " ").title()}')
    return numeric_vars[ind]
    

# Helper to ask for boolean
def get_bool(question):
    while True:
        exercise_inp = str(input(f'{question} (y/n) ')).lower().strip()
        if exercise_inp in ('y', 'yes'):
            exercise_bool = True
            break
        elif exercise_inp in ('n', 'no'):
            exercise_bool = False
            break
        else:
            print('Please enter (y/n).')
    
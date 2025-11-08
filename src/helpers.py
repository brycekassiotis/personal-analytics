# Utility: re-upload local CSV to Google Sheet (for recovery)
def reupload_csv_to_sheet(csv_data, sheet_name='Daily Analytics'):
    import pandas as pd
    df = pd.read_csv(csv_data)
    # Ensure 'date' is string for upload
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    push_to_sheet(df, sheet_name=sheet_name)
import os
import variables
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
import numpy as np

# Helper to refresh and add new data
def refresh_data(csv_data):
    return sync_sheet(csv_data, sheet_name='Daily Analytics')

# Pushes the changes made to google sheet
def push_to_sheet(df, sheet_name='Daily Analytics', creds_file='credentials.json'):
    # Respect offline/demo override
    if os.environ.get('PERSONAL_ANALYTICS_OFFLINE', '0') == '1':
        print('Offline mode enabled: skipping push_to_sheet.')
        return

    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(creds_file, scopes=scope)
        client = gspread.authorize(creds)

        # Always overwrite the Google Sheet with only the columns present in the DataFrame
        sheet = client.open(sheet_name).sheet1

        # Convert all pd.Timestamp to string (ISO format) for Google Sheets JSON compliance
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]' or df[col].dtype == 'datetime64[ns, UTC]':
                df[col] = df[col].dt.strftime('%Y-%m-%d')

        # Convert all NaN/None to empty string for Google Sheets JSON compliance
        df = df.where(pd.notnull(df), '')

        # SAFEGUARD: Only clear and update if DataFrame is not empty and has 'date' column
        if not df.empty and 'date' in df.columns:
            sheet.clear()
            sheet.update([df.columns.values.tolist()] + df.values.tolist())
            print("Uploaded latest data to Google Sheet.")
        else:
            print("Skipped Google Sheet update: DataFrame is empty or missing 'date' column.")
    except Exception as e:
        print(f"Could not push data to Google Sheet: {e}")


# helper that allows me to add data from both the automation and manually
def sync_sheet(csv_data, sheet_name='Daily Analytics'):
    try:
        # If offline mode, skip Google Sheets and use local CSV only
        if os.environ.get('PERSONAL_ANALYTICS_OFFLINE', '0') == '1':
            print('Offline mode enabled: skipping sync from Google Sheet.')
            if os.path.exists(csv_data):
                local_df = pd.read_csv(csv_data)
                local_df['date'] = pd.to_datetime(local_df['date'])
                variables.sync_variables_with_df(local_df)
                return local_df
            else:
                return pd.DataFrame(columns=list(variables.variables.keys()))

        # Always overwrite local CSV with Google Sheet data (source of truth)
        sheet_df = read_google_sheet(sheet_name, creds_path="credentials.json")
        if not sheet_df.empty:
            sheet_df['date'] = pd.to_datetime(sheet_df['date'], errors='coerce')
        sheet_df.sort_values('date', inplace=True)
        sheet_df.to_csv(csv_data, index=False)
        variables.sync_variables_with_df(sheet_df)
        print('Local CSV overwritten with Google Sheet data.')
        return sheet_df
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
def pick_var(var_question, df=None, numeric_only=False, streamlit=False):
    if streamlit and df is not None:
        return st.selectbox(var_question, df.columns)

    if numeric_only:
        var_keys = variables.get_numeric_keys()  # only numeric
    else:
        var_keys = list(variables.variables.keys())  # all current variables

    print(f'{var_question}\n')

    for i, key in enumerate(var_keys, start=1):
        print(f"{i}. {variables.variables[key]['label']}")

    print(f"{len(var_keys) + 1}. Quit\n")

    inp = input('Number: ').strip()

    try:
        ind = int(inp)
        if ind == len(var_keys) + 1:
            print('Quitting...')
            return None
        if ind < 1 or ind > len(var_keys):
            print('Please enter a valid option.')
            return None
    except ValueError:
        print('Please enter a valid option.')
        return None

    selected_key = var_keys[ind - 1]
    print(f'\nSelected {selected_key.replace("_", " ").title()}')
    return selected_key


    

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


def clean_and_coerce(df):
    
    if df is None:
        return pd.DataFrame()

    df = df.copy()

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # numeric columns
    try:
        numeric_keys = variables.get_numeric_keys()
    except Exception:
        numeric_keys = [k for k, v in variables.variables.items() if v.get('type') == 'numeric']

    for key in numeric_keys:
        if key in df.columns:
            df[key] = pd.to_numeric(df[key], errors='coerce')

    # boolean columns
    bool_keys = [k for k, v in variables.variables.items() if v.get('type') == 'boolean']
    text_keys = [k for k, v in variables.variables.items() if v.get('type') == 'text']

    def _to_bool(val):
        if pd.isna(val):
            return False
        if isinstance(val, bool):
            return val
        s = str(val).strip().lower()
        if s in ('1', 'true', 't', 'yes', 'y'):
            return True
        if s in ('0', 'false', 'f', 'no', 'n'):
            return False
        # fallback: try numeric
        try:
            return float(s) != 0
        except Exception:
            return False
            
    # Ensure text columns stay as text
    for key in text_keys:
        if key in df.columns:
            df[key] = df[key].astype(str)

    for key in bool_keys:
        if key in df.columns:
            df[key] = df[key].apply(_to_bool)

    return df
    
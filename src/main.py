import os
import pandas as pd
from datetime import datetime

def menu():
    inp = input("Select: " \
    "1. Add today's data" \
    "2. Show averages")

    if inp == '1':
        get_user_input()
    if inp == '2':
        show_stats(df)

def get_user_input():

    date_str = str(input('Enter date (YYYY-MM-DD) or leave blank for today: '))
    sleep_hours = float(input('How many hours did you sleep? '))
    sleep_quality = float(input('Rate your sleep quality 1 to 10: '))
    exercise_bool = str(input('Did you exercise yesterday? (y/n) ')).lower()
    calories = int(input('How many calories did you consume yesterday? '))
    productivity = float(input('Rate your productivity yesterday 1 to 10: '))
    stress = float(input('Rate your stress levels yesterday 1 to 10: '))

    return date_str, [sleep_hours, sleep_quality, exercise_bool, calories, productivity, stress]

def main():

    csv_data = 'data/data.csv' 

    # will add more in the future, automate others like weather
    columns = ['date', 'sleep_hours', 'sleep_quality', 'exercise', 'calories', 'productivity', 'stress']

    # load / create csv
    if not os.path.exists(csv_data) or os.path.getsize(csv_data) == 0:
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(columns=columns)
        df.to_csv(csv_data, index=False)
    else:
        df = pd.read_csv(csv_data)

    # convert to datetime, set date index
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)


    # today's date
    date_str, values = get_user_input()
    if date_str ==  '':
        date_str = pd.Timestamp(datetime.now().date())
    else:
        date_str = pd.to_datetime(date_str)

    # add row for today
    df.loc[date_str] = values

    # update csv
    df.to_csv(csv_data)
    return df

def show_stats(df):
    print(f"Average sleep hours: {df['sleep_hours'].mean()}")
    print(f"Average stress level: {df[['stress']].mean()}")
    print(f"Average calories: {df[['calories']].mean()}")


if __name__ == '__main__':
    df = main()
    show_stats(df)
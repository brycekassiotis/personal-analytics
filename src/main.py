import os
import pandas as pd
from datetime import datetime
import plots
import analysis
import variables

def main():
    df, csv_data = read_data()
    return df, csv_data

# will add more in the future, automate others
columns = ['date', 'sleep_hours', 'sleep_quality', 'exercise', 'calories', 'productivity', 'stress']
numeric_columns = list(variables.get_numeric_keys().values())

def menu(df, csv_data):

    while True:
        inp = input("Select: \n"
        "1. Add today's data \n"
        "2. Show past week's data \n"
        "3. Show averages\n"
        "4. Plot menu\n"
        "5. Analysis menu\n"
        "6. Quit\n\n"
        "Number: ")

        if inp == '1':
            add_data(df, csv_data)
        elif inp == '2':
            show_week(df, csv_data)
        elif inp == '3':
            show_averages(df)
        elif inp == '4':
            plots.plot_menu(df)
        elif inp == '5':
            analysis.analysis_menu(df)
        elif inp == '6':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


def get_user_input(df):

    # loop for date
    while True:
        date_str = str(input('Enter date (YYYY-MM-DD) or leave blank for today: '))

        if date_str == '':
            date_obj = datetime.now().date() # default to today
        else:
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d", "%B %d", "%b %d"):
                try:
                    date_obj = datetime.strptime(date_str, fmt)

                    if fmt in ("%m/%d", "%B %d", "%b %d"):
                        date_obj = date_obj.replace(year=datetime.now().year)
                    break

                except ValueError:
                    continue
            else:
                print('Please enter a valid date.')
                continue

        date_obj = pd.to_datetime(date_obj)

        # check if date already exists
        if date_obj in df['date'].values:
            choice = input('Date already exists- overwrite? (y/n) ').lower()
            if choice not in ('y', 'yes'):
                print('Will not add data for this date.')
                return None
        
        break
    
        
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
    
    
    calories = number_helper('How many calories did you consume yesterday? ')
    productivity = rating_helper('Rate your productivity yesterday 1 to 10: ')
    stress = rating_helper('Rate your stress levels yesterday 1 to 10: ')

    return [date_obj, sleep_hours, sleep_quality, exercise_bool, calories, productivity, stress]


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
            return inp
        except ValueError:
            print('Please enter a valid number.')
    

def read_data():
    csv_data = 'data/data.csv' 

    # load / create csv
    if not os.path.exists(csv_data) or os.path.getsize(csv_data) == 0:
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(columns=columns)
        df.to_csv(csv_data, index=False)
    else:
        df = pd.read_csv(csv_data)

    # convert to datetime
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])

    return df, csv_data


def add_data(df, csv_data):

    # add row for today
    values = get_user_input(df)
    if values is None:
        return df
    date_obj = values[0]

    # if overwritten replace old data
    if date_obj in df['date'].values:
        index = df.index[df['date'] == date_obj][0]
        df.loc[index, ['sleep_hours', 'sleep_quality', 'exercise', 'calories', 'productivity', 'stress']] = values[1:]

    # make and add new row otherwise
    else:
        new_row = [date_obj] + values[1:]
        df.loc[len(df)] = new_row

    # sort by date
    df.sort_values('date', inplace=True)

    # update csv
    df.to_csv(csv_data, index=False)
    return df


# Shows last 7 days of data
def show_week(df, csv_data):

    df_last_week = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]
    print(f'Last weeks averages: \n {df_last_week[numeric_columns].mean().items()}')
    print(df_last_week)

# Show averages for entire dataset
def show_averages(df):
    print(f"Average sleep hours: {df['sleep_hours'].mean():.2f}")
    print(f"Average sleep quality: {df['sleep_quality'].mean():.2f}")
    print(f"Average stress level: {df['stress'].mean():.2f}")
    print(f"Average calories: {df['calories'].mean():.0f}")
    print(f"Average productivity level: {df['productivity'].mean():.2f}")
    


if __name__ == '__main__':
    df, csv_data = main()
    menu(df, csv_data)
    

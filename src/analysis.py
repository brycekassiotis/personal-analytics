import variables
import main

def analysis_menu(df):

    df = main.refresh_data('data/data.csv')

    # loop until the user quits
    while True:
        inp = input("Select: \n"
            "1. Summarize data \n" 
            "2. Get average of data\n"
            "3. Get median of data\n"
            "4. Get standard deviation of data\n"
            "5. Quit\n\n"
            "Number: ")

        if inp == '1':
            print(df.describe())
        elif inp == '2':
            print(get_average(df))
        elif inp == '3':
            print(get_median(df))
        elif inp == '4':
            print(get_std(df))
        elif inp == '5':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')

    return df


def get_average(df):

    col_key = numeric_input_helper('mean')
    if col_key is None:
        return

    return f"The mean of {col_key.replace('_', ' ').title()} is {df[col_key].mean():.2f}"



def get_median(df):

    col_key = numeric_input_helper('median')
    if col_key is None:
        return

    return f"The median of {col_key.replace('_', ' ').title()} is {df[col_key].median():.2f}"


def get_std(df):
    col_key = numeric_input_helper('standard deviation')
    if col_key is None:
        return

    return f"The standard deviation of {col_key.replace('_', ' ').title()} is {df[col_key].std():.2f}"

# takes input for which variable and returns the corresponding column key
def numeric_input_helper(stat):

    numeric_vars = variables.get_numeric_keys()

    print(f'What variable number would you like to find the {stat} of?\n')

    for i, key in numeric_vars.items():
        print(f"{i}. {variables.variables[key]['label']}")

    print(f"{len(numeric_vars) + 1}. Quit")

    inp = input('Number: ')
    
    try:
        ind = int(inp)
        if ind == len(numeric_vars) + 1:
            print('Quitting...')
            return None
        
        if ind not in numeric_vars:
            print('Please enter a valid option.')
            return None
        
        return numeric_vars[ind]
    
    except (ValueError, TypeError):
        print('Please enter a valid option')
        return None
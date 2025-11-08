
import variables
import helpers

def analysis_menu(df, streamlit=False):
    try:
        df = helpers.clean_and_coerce(df)
    except Exception:
        pass

    numeric_df = df.select_dtypes(include=["number"])

    if streamlit:
        import streamlit as st
        option = st.selectbox("Select analysis type:", ["Summary", "Average", "Median", "Standard Deviation"])

        if option == "Summary":
            st.write(numeric_df.describe())
        elif option == "Average":
            st.write(numeric_df.mean().round(2))
        elif option == "Median":
            st.write(numeric_df.median().round(2))
        elif option == "Standard Deviation":
            st.write(numeric_df.std().round(2))
        return df

    # loop until the user quits
    while True:
        inp = input("\nSelect: \n"
            "1. Summarize data \n" 
            "2. Get average of data\n"
            "3. Get median of data\n"
            "4. Get standard deviation of data\n"
            "5. Quit\n\n"
            "Number: ")

        if inp == '1':
            print(numeric_df.describe())
        elif inp == '2':
            result = get_average(df)
            if result is not None:
                print(result)
        elif inp == '3':
            result = get_median(df)
            if result is not None:
                print(result)
        elif inp == '4':
            result = get_std(df)
            if result is not None:
                print(result)
        elif inp == '5':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


def get_average(df):

    col_key = numeric_input_helper('mean')
    if col_key is None:
        return

    return f"The mean of {col_key.replace('_', ' ').title()} is {df[col_key].mean():.2f}\n"



def get_median(df):

    col_key = numeric_input_helper('median')
    if col_key is None:
        return

    return f"The median of {col_key.replace('_', ' ').title()} is {df[col_key].median():.2f}\n"


def get_std(df):
    col_key = numeric_input_helper('standard deviation')
    if col_key is None:
        return

    return f"The standard deviation of {col_key.replace('_', ' ').title()} is {df[col_key].std():.2f}\n"

# takes input for which variable and returns the corresponding column key
def numeric_input_helper(stat):
    # get mapping of numeric variable index->key
    numeric_vars = variables.get_numeric_variables()

    print(f'What variable number would you like to find the {stat} of?\n')

    for i, key in numeric_vars.items():
        print(f"{i}. {variables.variables[key]['label']}")

    print(f"{len(numeric_vars) + 1}. Quit\n")

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
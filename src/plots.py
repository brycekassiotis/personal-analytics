import matplotlib.pyplot as plt

def plot_menu(df):
    while True:
        inp = input('\nSelect: \n'
        '1. Plot variable over time \n'
        '2. Scatterplot between variables \n'
        '3. Quit \n'
        '\nNumber: ')

        if inp == '1':
            plot_variable_over_time(df)
        elif inp == '2':
            scatter_plot(df)
        elif inp == '3':
            exit()
        else:
            print('\nPlease select an option.\n')

# used for plot options
numeric_choices = {'1': 'sleep_hours',
        '2': 'sleep_quality',
        '3': 'calories',
        '4': 'productivity',
        '5': 'stress'}

# Plot inputted variable against date
def plot_variable_over_time(df):

    

    inp = input('What variable number would you like to plot?\n'
        '1. Sleep hours over time. \n'
        '2. Sleep quality over time. \n'
        '3. Calories over time. \n'
        '4. Productivity level over time. \n'
        '5. Stress level over time. \n'
        '6. Quit. \n'

        '\nNumber: ')
    if inp == '6':
        return
    if inp not in numeric_choices:
        print('Please enter a valid option.')
        return
    
    col = numeric_choices[inp]


    plt.plot(df['date'], df[col])
    plt.xlabel('Date')
    plt.ylabel(col.replace('_', ' ').title())
    plt.title(f'{col.replace('_', ' ').title()} Over Time')
    plt.show()

    print('Would you like to save the plot? ')


# scatter plot to compare relationships between variables
def scatter_plot(df):
    inp = input('What should be the X variable?\n'
        '1. Sleep hours \n'
        '2. Sleep quality \n'
        '3. Calories \n'
        '4. Productivity level \n'
        '5. Stress level \n'
        '6. Quit. \n'

        '\nNumber: ')
    if inp == '6':
        return()
    
    if inp not in numeric_choices:
        print('Please enter a valid option.')
        return
    
    x_data = numeric_choices[inp]


    inp = input('What should be the Y variable?\n'
        '1. Sleep hours \n'
        '2. Sleep quality \n'
        '3. Calories \n'
        '4. Productivity level \n'
        '5. Stress level \n'
        '6. Quit. \n'

        '\nNumber: ')
    if inp == '6':
        return
    
    if inp not in numeric_choices:
        print('Please enter a valid option.')
        return
    
    y_data = numeric_choices[inp]

    # avoid plotting variable against itself
    if x_data == y_data:
        print('X and Y must be different variables.')
        return

    # make scatterplot
    plt.xlabel(x_data.replace('_', ' ').title())
    plt.ylabel(y_data.replace('_', ' ').title())
    plt.title(f'{x_data.replace('_', ' ').title()} vs {y_data.replace('_', ' ').title()}')

    plt.scatter(df[x_data], df[y_data])
    plt.show()

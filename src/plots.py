import matplotlib.pyplot as plt
import variables

def plot_menu(df):
    # loop until user quits
    while True:
        inp = input('\nSelect: \n'
        '1. Plot variable over time \n'
        '2. Scatterplot between variables \n'
        '3. Plot correlation between variables'
        '4. Quit \n'
        '\nNumber: ')

        if inp == '1':
            plot_variable_over_time(df)
        elif inp == '2':
            scatter_plot(df)
        elif inp == '3':
            corr_plot(df)
        elif inp == '4':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


# Plot inputted variable against date
def plot_variable_over_time(df):
    numeric_vars = variables.get_numeric_variables()

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
    
    try:
        ind = int(inp)
    except ValueError:
        print('Please enter a valid option.')
        return
    
    if ind not in numeric_vars:
        print('Please enter a valid option.')
        return
    
    col = numeric_vars[ind]

    title = f'{col.replace("_", " ").title()} Over Time'
    plt.plot(df['date'], df[col])
    plt.xlabel('Date')
    plt.ylabel(col.replace('_', ' ').title())
    plt.title(title)
    
    save_plot_helper(title)
    plt.show()


# scatter plot to compare relationships between variables
def scatter_plot(df):
    numeric_vars = variables.get_numeric_variables()

    inp = input('What should be the X variable?\n'
        '1. Sleep hours \n'
        '2. Sleep quality \n'
        '3. Calories \n'
        '4. Productivity level \n'
        '5. Stress level \n'
        '6. Quit. \n'

        '\nNumber: ')
    if inp == '6':
        return
    
    try:
        ind = int(inp)
    except ValueError:
        print('Please enter a valid option.')
        return
    
    if ind not in numeric_vars:
        print('Please enter a valid option.')
        return
    
    x_data = numeric_vars[int(ind)]


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
    
    if int(inp) not in numeric_vars:
        print('Please enter a valid option.')
        return
    
    y_data = numeric_vars[int(inp)]

    # avoid plotting variable against itself
    if x_data == y_data:
        print('X and Y must be different variables.')
        return

    # make scatterplot
    title = f'{x_data.replace("_", " ").title()} vs {y_data.replace("_", " ").title()}'
    plt.xlabel(x_data.replace('_', ' ').title())
    plt.ylabel(y_data.replace('_', ' ').title())
    plt.title(title)

    plt.scatter(df[x_data], df[y_data])

    save_plot_helper(title)
    plt.show()

# helper to check if user wants to save the plot
def save_plot_helper(title):
    
    save_bool = input('Would you like to save the plot? (y/n) ').lower().strip() in ('y', 'yes')

    if save_bool: 
        # save the plot as a PNG file
        filename = f"{title.replace(' ', '_').lower()}.png"
        plt.savefig(filename)
        print(f'Plot saved as {filename}')
    else:
        print('Not saving plot...')


def corr_plot(df):

    numeric_vars = variables.get_numeric_variables()

    inp = input('What should be the X variable?\n'
        '1. Sleep hours \n'
        '2. Sleep quality \n'
        '3. Calories \n'
        '4. Productivity level \n'
        '5. Stress level \n'
        '6. Quit. \n'

        '\nNumber: ')
    if inp == '6':
        return
    
    try:
        ind = int(inp)
    except ValueError:
        print('Please enter a valid option.')
        return
    
    if ind not in numeric_vars:
        print('Please enter a valid option.')
        return
    
    x_data = numeric_vars[int(ind)]


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
    
    if int(inp) not in numeric_vars:
        print('Please enter a valid option.')
        return
    
    y_data = numeric_vars[int(inp)]

    # avoid plotting variable against itself
    if x_data == y_data:
        print('X and Y must be different variables.')
        return

    # make correlation plot
    title = f'{x_data.replace("_", " ").title()} vs {y_data.replace("_", " ").title()}'
    
    plt.title(title)

    corr_val = df[x_data].corr(df[y_data])
    plt.matshow([[corr_val]], cmap='coolwarm', vmin = -1, vmax = 1)
    plt.colorbar(label='Correlation')

    plt.xticks([0], [x_data.replace('_', ' ').title()])
    plt.yticks([0], [y_data.replace('_', ' ').title()])

    save_plot_helper(title)
    plt.show()
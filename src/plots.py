import matplotlib.pyplot as plt
import seaborn as sns
import variables
import main

def plot_menu(df):

    main.refresh_data('data/data.csv')

    # loop until user quits
    while True:
        inp = input('\nSelect: \n'
        '1. Plot variable over time \n'
        '2. Scatterplot between variables \n'
        '3. Plot correlation between variables\n'
        '4. Plot correlation heatmap\n'
        '5. Quit \n'
        '\nNumber: ')

        if inp == '1':
            plot_variable_over_time(df)
        elif inp == '2':
            scatter_plot(df)
        elif inp == '3':
            corr_plot(df)
        elif inp == '4':
            corr_heatmap(df)
        elif inp == '5':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


# Plot inputted variable against date
def plot_variable_over_time(df):
    numeric_vars = variables.get_numeric_keys()

    print(f'What variable would you like to plot over time?\n')

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
    except ValueError:
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


# plot correlation between two variables
def corr_plot(df):

    numeric_vars = variables.get_numeric_variables()

    x_data = pick_var('X')
    if not x_data: return


    y_data = pick_var('Y')
    if not y_data: return

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

    plot_menu(df)


# create visual correlation heatmap
def corr_heatmap(df):
    plt.figure(figsize=(6,6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
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


# helper to pick variables
def pick_var(var_label):
    numeric_vars = variables.get_numeric_variables()

    inp = input(f'What should be the {var_label} variable?\n'
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
        if ind not in numeric_vars:
            print('Please enter a valid option.')
            return None
        
        print(f'\nSelected {numeric_vars[ind].replace("_", " ").title()}')
        return numeric_vars[ind]
    
    except ValueError:
        print('Please enter a valid option.')
        return None
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from helpers import pick_var
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
    col = pick_var('What variable should be plotted against time?')
    if not col: return

    title = f'{col.replace("_", " ").title()} Over Time'
    plt.plot(df['date'], df[col])

    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(8))
    plt.gcf().autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel(col.replace('_', ' ').title())
    plt.title(title)
    
    save_plot_helper(title)
    plt.show()


# scatter plot to compare relationships between variables
def scatter_plot(df):

    x_data = pick_var('What should be the X variable?')
    if not x_data: return

    y_data = pick_var('What should be the Y variable?')
    if not y_data: return

    # avoid plotting variable against itself
    if x_data == y_data:
        print('X and Y must be different variables.')
        return

    # make scatterplot
    title = f'{x_data.replace("_", " ").title()} vs {y_data.replace("_", " ").title()}'
    plt.xlabel(x_data.replace('_', ' ').title())
    plt.ylabel(y_data.replace('_', ' ').title())
    plt.title(title)

    plt.scatter(df[x_data].astype(float), df[y_data].astype(float))

    save_plot_helper(title)
    plt.show()


# plot correlation between two variables
def corr_plot(df):

    x_data = pick_var('What should be the X variable?')
    if not x_data: return

    y_data = pick_var('What should be the Y variable?')
    if not y_data: return

    # avoid plotting variable against itself
    if x_data == y_data:
        print('X and Y must be different variables.')
        return

    # make correlation plot
    title = f'{x_data.replace("_", " ").title()} vs {y_data.replace("_", " ").title()}'

    # clean locally
    df_clean = df.replace('', np.nan).infer_objects(copy=False)

    for col in df_clean.columns:
        try:
            df_clean[col] = pd.to_numeric(df_clean[col])
        except (ValueError, TypeError):
            pass


    corr_val = df_clean[x_data].corr(df_clean[y_data])

    fig, ax = plt.subplots()

    cax = ax.matshow([[corr_val]], cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax, label='Correlation')

    ax.text(0,0, f"{corr_val:.2f}", va='center', ha='center', fontsize=15, fontweight='bold')

    ax.set_xticks([0])
    ax.set_xticklabels([x_data.replace('_', ' ').title()])

    ax.set_yticks([0])
    ax.set_yticklabels([x_data.replace('_', ' ').title()])

    ax.set_title(title, pad=20)

    save_plot_helper(title)
    plt.show()

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
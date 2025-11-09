import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import variables
import helpers
import warnings

# Suppress FutureWarning about downcasting behavior
warnings.filterwarnings('ignore', category=FutureWarning)

def plot_menu(df, streamlit=False):
    if streamlit:
        # Streamlit UI
        option = st.selectbox(
            "Select an analysis type:",
            [
                "Plot variable over time",
                "Scatterplot between variables",
                "Plot correlation between variables",
                "Plot correlation heatmap",
            ],
        )
        if option == "Plot variable over time":
            plot_variable_over_time(df, streamlit=True)
        elif option == "Scatterplot between variables":
            scatter_plot(df, streamlit=True)
        elif option == "Plot correlation between variables":
            corr_plot(df, streamlit=True)
        elif option == "Plot correlation heatmap":
            corr_heatmap(df, streamlit=True)

    else:
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
def plot_variable_over_time(df, streamlit=False):
    # ensure types are clean for plotting
    try:
        df = helpers.clean_and_coerce(df)
    except Exception:
        pass

    if streamlit:
        # Only show numeric variables
        numeric_labels = variables.get_numeric_labels()
        selected_label = st.selectbox("Select variable:", list(numeric_labels.values()))
        col = [k for k, v in numeric_labels.items() if v == selected_label][0]

        # Checkbox for line of best fit
        show_best_fit = st.checkbox("Show line of best fit")

        # Button to generate plot
        if st.button("Generate Plot"):
            # Filter out rows where the selected variable has no data
            df_filtered = df[df[col].notna()].copy()
            
            fig, ax = plt.subplots()
            ax.plot(df_filtered['date'], df_filtered[col], label='Data')
            
            # Add line of best fit if requested
            if show_best_fit and len(df_filtered) > 1:
                x_numeric = np.arange(len(df_filtered))
                y_numeric = df_filtered[col].values
                z = np.polyfit(x_numeric, y_numeric, 1)
                p = np.poly1d(z)
                ax.plot(df_filtered['date'], p(x_numeric), "r--", alpha=0.8, label='Best Fit')
                ax.legend()
            
            ax.set_xlabel('Date')
            ax.set_ylabel(col.replace("_", " ").title())
            ax.set_title(f"{col.replace('_',' ').title()} Over Time")
            # Limit to max 5 x-ticks (dates)
            if len(df_filtered['date']) > 5:
                step = max(1, len(df_filtered['date']) // 5)
                xticks = df_filtered['date'].iloc[::step]
                ax.set_xticks(xticks)
                def _format_date(d):
                    import pandas as pd
                    try:
                        dt = pd.to_datetime(d, errors='coerce')
                        if pd.isnull(dt):
                            return str(d)
                        return dt.strftime('%Y-%m-%d')
                    except Exception:
                        return str(d)
                ax.set_xticklabels([_format_date(d) for d in xticks], rotation=45)
            else:
                plt.xticks(rotation=45)
            st.pyplot(fig)
        return

    else:
        from helpers import pick_var
        col = pick_var('What variable should be plotted against time?', numeric_only=True)
        if not col:
            return
        
        # Ask if user wants line of best fit
        best_fit_input = input('Add line of best fit? (y/n): ').lower().strip()
        show_best_fit = best_fit_input in ['y', 'yes']

    # Filter out rows where the selected variable has no data
    df_filtered = df[df[col].notna()].copy()
    
    title = f'{col.replace("_", " ").title()} Over Time'
    plt.plot(df_filtered['date'], df_filtered[col], label='Data')
    
    # Add line of best fit if requested
    if show_best_fit and len(df_filtered) > 1:
        x_numeric = np.arange(len(df_filtered))
        y_numeric = df_filtered[col].values
        z = np.polyfit(x_numeric, y_numeric, 1)
        p = np.poly1d(z)
        plt.plot(df_filtered['date'], p(x_numeric), "r--", alpha=0.8, label='Best Fit')
        plt.legend()
    
    # Limit to max 5 x-ticks (dates)
    if len(df_filtered['date']) > 5:
        step = max(1, len(df_filtered['date']) // 5)
        xticks = df_filtered['date'].iloc[::step]
        def _format_date(d):
            import pandas as pd
            try:
                dt = pd.to_datetime(d, errors='coerce')
                if pd.isnull(dt):
                    return str(d)
                return dt.strftime('%Y-%m-%d')
            except Exception:
                return str(d)
        plt.xticks(xticks, [_format_date(d) for d in xticks], rotation=45)
    else:
        plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel(col.replace('_', ' ').title())
    plt.title(title)
    plt.show()


# scatter plot to compare relationships between variables
def scatter_plot(df, streamlit=False):
    # ensure types are clean for plotting
    try:
        df = helpers.clean_and_coerce(df)
    except Exception:
        pass

    if streamlit:
        labels = variables.get_numeric_labels()
        x_label = st.selectbox("Select X variable:", list(labels.values()))
        y_label = st.selectbox("Select Y variable:", list(labels.values()))
        x_data = [k for k, v in labels.items() if v == x_label][0]
        y_data = [k for k, v in labels.items() if v == y_label][0]

        
        if st.button("Generate Scatter Plot"):
            if x_data == y_data:
                st.warning("X and Y must be different variables.")
            else:
                # Filter out rows where either variable has no data
                df_filtered = df[df[x_data].notna() & df[y_data].notna()].copy()
                
                fig, ax = plt.subplots()
                ax.scatter(df_filtered[x_data].astype(float), df_filtered[y_data].astype(float))
                ax.set_xlabel(x_data.replace("_"," ").title())
                ax.set_ylabel(y_data.replace("_"," ").title())
                ax.set_title(f"{x_data.replace('_',' ').title()} vs {y_data.replace('_',' ').title()}")
                st.pyplot(fig)
        return
    else:
        from helpers import pick_var
        x_data = pick_var('What should be the X variable?', numeric_only=True)
        if not x_data: return
        y_data = pick_var('What should be the Y variable?', numeric_only=True)
        if not y_data: return

    # avoid plotting variable against itself
    if x_data == y_data:
        print('X and Y must be different variables.')
        return

    # Filter out rows where either variable has no data
    df_filtered = df[df[x_data].notna() & df[y_data].notna()].copy()
    
    # make scatterplot
    title = f'{x_data.replace("_", " ").title()} vs {y_data.replace("_", " ").title()}'
    plt.xlabel(x_data.replace('_', ' ').title())
    plt.ylabel(y_data.replace('_', ' ').title())
    plt.title(title)

    plt.scatter(df_filtered[x_data].astype(float), df_filtered[y_data].astype(float))

    plt.show()


# plot correlation between two variables
def corr_plot(df, streamlit=False):
    # ensure types are clean for plotting
    try:
        df = helpers.clean_and_coerce(df)
    except Exception:
        pass

    if streamlit:
        x_data = st.selectbox("Select X variable:", df.columns[1:], key="corr_x")
        y_data = st.selectbox("Select Y variable:", df.columns[1:], key="corr_y")
        
        if st.button("Generate Correlation Plot"):
            if x_data == y_data:
                st.warning("X and Y must be different variables.")
            else:
                df_clean = df.replace('', np.nan).infer_objects(copy=False)
                for col in df_clean.columns:
                    try: df_clean[col] = pd.to_numeric(df_clean[col])
                    except: pass
                corr_val = df_clean[x_data].corr(df_clean[y_data])

                fig, ax = plt.subplots()
                cax = ax.matshow([[corr_val]], cmap='coolwarm', vmin=-1, vmax=1)
                fig.colorbar(cax, label='Correlation')
                ax.text(0,0,f"{corr_val:.2f}",va='center',ha='center',fontsize=15,fontweight='bold')
                ax.set_xticks([0])
                ax.set_xticklabels([x_data.replace('_',' ').title()])
                ax.set_yticks([0])
                ax.set_yticklabels([y_data.replace('_',' ').title()])
                ax.set_title(f"{x_data.replace('_',' ').title()} vs {y_data.replace('_',' ').title()}", pad=20)
                st.pyplot(fig)
        return
    else:
        from helpers import pick_var
        x_data = pick_var('What should be the X variable?', numeric_only=True)
        if not x_data: return
        y_data = pick_var('What should be the Y variable?', numeric_only=True)
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
    ax.set_yticklabels([y_data.replace('_', ' ').title()])

    ax.set_title(title, pad=20)

    if streamlit:
        st.pyplot(fig)
    else:
        plt.show()


# create visual correlation heatmap
def corr_heatmap(df, streamlit=False):
    # ensure types are clean for plotting
    try:
        df = helpers.clean_and_coerce(df)
    except Exception:
        pass

    # get rid of non-numeric columns
    corr_df = df.select_dtypes(include=np.number).corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_df,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        annot_kws={"size": 8}
    )

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    ax.set_title("Correlation Matrix")

    if streamlit:
        st.pyplot(fig)
    else:
        plt.tight_layout()
        plt.show()



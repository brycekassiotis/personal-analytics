import helpers
import shutil
import streamlit as st

variables = {
    "sleep_hours": {"label": "Sleep Hours", "type": "numeric"},
    "sleep_quality": {"label": "Sleep Quality", "type": "numeric"},
    "steps": {"label": "Steps", "type": "numeric"},
    "exercise": {"label": "Exercise", "type": "text"},
    "calories": {"label": "Calories", "type": "numeric"},
    "productivity": {"label": "Productivity", "type": "numeric"},
    "stress": {"label": "Stress", "type": "numeric"},
    "day_rating": {"label": "Day Rating", "type": "numeric"},
    "mood": {"label": "Mood", "type": "numeric"},
    "screen_time": {"label": "Screen Time", "type": "numeric"},
    "min_temp": {"label": "Minimum Temperature", "type": "numeric"},
    "max_temp": {"label": "Maximum Temperature", "type": "numeric"},
    "weather": {"label": "Weather", "type": "text"},
    "day_of_week": {"label": "Day of Week", "type": "text"},
    "social": {"label": "Socialness", "type": "numeric"},
    "notes": {"label": "Notes", "type": "text"},
    "creatine": {"label": "Creatine", "type": "boolean"},
    "vitamin_d": {"label": "Vitamin D", "type": "boolean"},
    "magnesium": {"label": "Magnesium", "type": "boolean"}
}


def variables_menu(df, csv_data, streamlit=False):
    sync_variables_with_df(df)

    if streamlit:
        st.header("⚙️ Variable Settings")
        sync_variables_with_df(df)

        # Store selected variable persistently
        if "selected_var_key" not in st.session_state:
            st.session_state.selected_var_key = None

        # === View Variables ===
        st.subheader("Current Variables")
        for key, val in variables.items():
            st.write(f"**{val['label']}** — *{val['type']}*")

        st.markdown("---")

        # === Add Variable ===
        st.subheader("Add New Variable")
        with st.form("add_var_form", clear_on_submit=True):
            new_key = st.text_input("Variable Key")
            new_label = st.text_input("Display Label")
            new_type = st.selectbox("Type", ["numeric", "text", "boolean"])
            add_submit = st.form_submit_button("Add Variable")

            if add_submit:
                if new_key in variables:
                    st.error("This variable key already exists.")
                elif new_key.strip() == "":
                    st.error("Variable key cannot be empty.")
                else:
                    variables[new_key] = {"label": new_label, "type": new_type}
                    df[new_key] = '' if new_type != "boolean" else False
                    df.to_csv(csv_data, index=False)
                    helpers.push_to_sheet(df)
                    st.success(f"✅ Variable '{new_label}' added successfully!")

        st.markdown("---")

        # === Edit / Delete Variable ===
        st.subheader("Edit or Delete Variable")

        var_keys = list(variables.keys())
        selected = st.selectbox(
            "Select a variable", 
            ["None"] + var_keys,
            index=(var_keys.index(st.session_state.selected_var_key) + 1) if st.session_state.selected_var_key in var_keys else 0,
            key="var_select"
        )

        if selected != "None":
            st.session_state.selected_var_key = selected
            selected_var = variables[selected]
            st.write(f"**Current Label:** {selected_var['label']}")
            st.write(f"**Current Type:** {selected_var['type']}")

            new_label = st.text_input("New Label", value=selected_var["label"], key=f"label_{selected}")
            new_type = st.selectbox(
                "New Type",
                ["numeric", "text", "boolean"],
                index=["numeric", "text", "boolean"].index(selected_var["type"]),
                key=f"type_{selected}"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes", key=f"save_{selected}"):
                    variables[selected]["label"] = new_label
                    variables[selected]["type"] = new_type
                    df.to_csv(csv_data, index=False)
                    helpers.push_to_sheet(df)
                    st.success(f"Saved changes to '{new_label}'.")

            with col2:
                if st.button("Delete Variable", key=f"delete_{selected}"):
                    st.session_state.confirm_delete = selected

            if "confirm_delete" in st.session_state and st.session_state.confirm_delete == selected:
                confirm = st.text_input("Type DELETE to confirm deletion", key=f"confirm_{selected}")
                if confirm == "DELETE":
                    shutil.copy(csv_data, csv_data.replace(".csv", "_backup.csv"))
                    if selected in df.columns:
                        df.drop(columns=[selected], inplace=True)
                    del variables[selected]
                    df.to_csv(csv_data, index=False)
                    helpers.push_to_sheet(df)
                    st.warning(f"Deleted variable '{selected_var['label']}'.")
                    st.session_state.selected_var_key = None
                    del st.session_state.confirm_delete
                    st.rerun()

            st.markdown("---")
            st.subheader("Numeric Variables (for plotting)")
            numeric_vars = [v["label"] for v in variables.values() if v["type"] == "numeric"]
            st.write(numeric_vars)

            return


    # loop until user quits
    while True:
        inp = input('\nSelect: \n'
        '1. View variables \n'
        '2. Add new variable \n'
        '3. Edit variable\n'
        '4. Quit \n'
        '\nNumber: ')

        if inp == '1':
            print("\nCurrent Variables in DataFrame:\n")
            for col in df.columns:
                label = variables.get(col, {}).get('label', col)
                print(f"- {label}")

        elif inp == '2':
            add_variable(df)
        elif inp == '3':
            edit_variable(df, csv_data)
        elif inp == '4':
            print('Exiting menu...')
            break
        else:
            print('\nPlease select an option.\n')


# to add new variable
def add_variable(df, csv_data):
    global variables

    key = input("Enter the variable key: ").strip()
    if key in variables:
        print("This variable key already exists.")
        return df
    
    label = input("Enter the display label for the variable: ").strip()
    var_type = input("Enter the variable type (numeric, text, boolean): ").lower().strip()
    if var_type not in ["numeric", "text", "boolean"]:
        print("Invalid type.")
        return df

    # add var to dict
    variables[key] = {"label": label, "type": var_type}
    
    # add col to df
    df[key] = ''

    df.to_csv(csv_data, index=False)
    helpers.push_to_sheet(df)

    print(f"Variable '{label}' added successfully!")
    return df


def edit_variable(df, csv_data):
    global variables

    selected_key = helpers.pick_var("Select variable number to edit:", numeric_only=False)

    if selected_key is None: return df

    selected_var = variables[selected_key]

    print(f"\nEditing '{selected_var['label']}' ({selected_var['type']})")
    print("Options:\n1. Edit label\n2. Edit type\n3. Delete variable\n4. Cancel")
    action = input("Select option: ").strip()

    if action == "1":
        new_label = input("Enter new label: ").strip()
        variables[selected_key]['label'] = new_label
        print("Label updated.")

    elif action == "2":
        new_type = input("Enter new type (numeric, text, boolean): ").strip().lower()
        if new_type in ["numeric", "text", "boolean"]:
            variables[selected_key]['type'] = new_type
            print("Type updated.")
        else:
            print("Invalid type!")
            return df

    elif action == "3":
        confirm = input(f"Are you sure you want to delete '{selected_var['label']}'? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            confirm_final = input("Type DELETE to confirm: ").strip()
            if confirm_final == "DELETE":
                # Backup CSV just in case
                shutil.copy(csv_data, csv_data.replace(".csv", "_backup.csv"))

                if selected_key in df.columns:
                    df.drop(columns=[selected_key], inplace=True)

                del variables[selected_key]
                print("Variable deleted.")
            else:
                print("Delete cancelled.")
                return df
        else:
            print("Delete cancelled.")
            return df

    elif action == "4":
        print("Cancelled.")
        return df
    else:
        print("Invalid option.")
        return df

    # Save CSV and push changes to Google Sheet
    df.to_csv(csv_data, index=False)
    helpers.push_to_sheet(df)
    return df


# ==============================
# Support Functions
# ==============================

def get_numeric_variables():
    return {i + 1: key for i, (key, val) in enumerate(variables.items()) if val['type'] == 'numeric'}


def get_numeric_keys():
    return [key for key, val in variables.items() if val['type'] == 'numeric']


def sync_variables_with_df(df):
    global variables

    # keep only columns that exist in df
    current_keys = list(df.columns)
    new_variables = {}

    for col in current_keys:
        if col in variables:
            new_variables[col] = variables[col]
        else:
            if df[col].dtype in ['float64', 'int64']:
                var_type = 'numeric'
            elif df[col].dtype == 'bool':
                var_type = 'boolean'
            else:
                var_type = 'text'

            new_variables[col] = {
                "label": col.replace("_", " ").title(),
                "type": var_type
            }

    variables = new_variables


def get_all_variables():
    return list(variables.keys())

def get_variable_labels():
    return {k: v["label"] for k, v in variables.items()}

def get_numeric_labels():
    return {k: v["label"] for k, v in variables.items() if v["type"] == "numeric"}

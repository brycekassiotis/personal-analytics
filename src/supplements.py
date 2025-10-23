import json
import os
import pandas as pd

supplement_file = "data/supplements.json"

def supplements_menu():
    while True:
        print('\nSupplements Menu\n')

        inp = input('Select:\n'
            '1. View supplements\n'
            '2. Add supplements\n'
            '3. Delete supplements\n'
            '4. Quit\n\n'
            'Number: ').strip()
        
        if inp == '1':
            sups = load_supplements()
            if not sups:
                print('No supplements found.')
            else:
                for name, info in sups.items():
                    print(f"\n{info['label']} ({info['type']})")
            
        elif inp == '2':
            add_supplement()
        
        elif inp == '3':
            sups = load_supplements()
            name = input('Enter supplement name to delete: ').strip().lower()

            if name in sups:
                del sups[name]
                save_supplements(sups)
                check_supplement_columns('data/data.csv')
                print(f"Deleted supplement '{name}'")
            
            else:
                print('Supplement not found')
        
        elif inp == '4':
            print('Exiting...\n')
            break

        else:
            print('Invalid selection.')


def load_supplements():
    if not os.path.exists(supplement_file):
        return {}
    
    with open(supplement_file, 'r') as f:
        return json.load(f)
    

def save_supplements(sups):
    with open(supplement_file, 'w') as f:
        json.dump(sups, f, indent=5)


def add_supplement():
    sups = load_supplements()

    name = input('Enter supplement name: ').strip().lower()

    if name in sups:
        print('Supplement already exists.')
        return
    
    sup_type = input('Enter variable type (b for boolean, n for numeric): ').lower().strip()

    if sup_type not in ['b', 'boolean', 'n', 'numeric']:
        print('Invalid type.')
        return
    else:
        if sup_type in ['b', 'boolean']: sup_type = 'boolean'
        else: sup_type = 'numeric'
    
    label = input("Label to display (such as 'Took Creatine' or 'Caffeine (mg)'): ").strip()

    sups[name] = {
        'label': label,
        'type': sup_type
    }

    save_supplements(sups)
    check_supplement_columns('data/data.csv')

    print(f"Added supplement '{label}' ({sups[name]['type']}).")
    

# Helper to check supplement columns in csv
def check_supplement_columns(csv_path):

    sups = load_supplements()
    if not sups: return

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        print('Creating data file...')
        df = pd.DataFrame()
    
    for name in sups.keys():
        if name not in df.columns:
            df[name] = None
    
    df.to_csv(csv_path, index=False)
import variables


# helper to pick variables
def pick_var(var_question):
    numeric_vars = variables.get_numeric_keys()

    print(f'{var_question}\n')

    for i, key in numeric_vars.items():
        print(f"{i}. {variables.variables[key]['label']}")

    print(f"{len(numeric_vars) + 1}. Quit\n")

    inp = input('Number: ').strip()
    
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
        
    print(f'\nSelected {numeric_vars[ind].replace("_", " ").title()}')
    return numeric_vars[ind]
    
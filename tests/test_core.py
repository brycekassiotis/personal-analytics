import os
import sys
from pathlib import Path
import pandas as pd


# Ensure src is importable
ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import helpers
import main
import variables


def test_clean_and_coerce_basic():
    # create a small dataframe with strings that should be coerced
    df = pd.DataFrame({
        'date': ['2025-01-01', 'not-a-date', None],
        'sleep_hours': ['7', '8.5', 'not-a-number'],
        'creatine': ['y', 'n', None]
    })

    out = helpers.clean_and_coerce(df)

    # date coerced: first row valid, others NaT
    assert pd.api.types.is_datetime64_any_dtype(out['date'])
    assert out['sleep_hours'].dtype.kind in ('f', 'i')
    # numeric coercion: invalid becomes NaN
    assert pd.isna(out.loc[2, 'sleep_hours'])
    # boolean coercion (allow numpy boolean types)
    assert out.loc[0, 'creatine'] == True
    assert out.loc[1, 'creatine'] == False


def test_add_data_writes_csv(tmp_path, monkeypatch):
    # prepare an empty dataframe with the expected columns
    variable_keys = [k for k in variables.variables.keys()]
    columns = ['date'] + variable_keys

    df = pd.DataFrame(columns=columns)

    # create a temporary csv path
    csv_path = tmp_path / 'data.csv'

    # construct manual_values matching columns length
    values = [
        '2025-11-07',  # date
    ]
    # fill the remaining with simple defaults
    for k in variable_keys:
        vtype = variables.variables[k]['type']
        if vtype == 'numeric':
            values.append(1)
        elif vtype == 'boolean':
            values.append(True)
        else:
            values.append('x')

    # ensure offline to avoid external push
    monkeypatch.setenv('PERSONAL_ANALYTICS_OFFLINE', '1')

    # call add_data with manual_values and the tmp csv path
    out_df = main.add_data(df, str(csv_path), manual_values=values)

    # file should be created and contain our row
    assert csv_path.exists()
    read = pd.read_csv(csv_path)
    assert len(read) == 1
    # date column should match
    assert str(read.loc[0, 'date']).startswith('2025')


def test_push_to_sheet_offline_no_error(monkeypatch):
    # When offline flag is set, push_to_sheet should return early and not raise
    monkeypatch.setenv('PERSONAL_ANALYTICS_OFFLINE', '1')
    df = pd.DataFrame({'date': ['2025-01-01'], 'sleep_hours': [7]})

    # Should not raise
    helpers.push_to_sheet(df, sheet_name='TestSheet', creds_file='credentials.json')

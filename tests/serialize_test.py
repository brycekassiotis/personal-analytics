import pandas as pd
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import helpers

# Create sample df with pandas Timestamp, numpy int, and NaN
df = pd.DataFrame({
    'date': [pd.Timestamp('2025-11-07'), pd.NaT],
    'val': [np.int64(5), np.float64(3.2)],
    'note': [np.nan, 'ok']
})

# Re-run serialization logic similar to helpers.push_to_sheet

def _serialize_cell(cell):
    try:
        if pd.isna(cell):
            return ''
    except Exception:
        pass

    if isinstance(cell, pd.Timestamp):
        try:
            return cell.strftime('%Y-%m-%d')
        except Exception:
            return str(cell)

    try:
        import numpy as _np
        if isinstance(cell, _np.generic):
            return cell.item()
    except Exception:
        pass

    if cell is pd.NaT:
        return ''

    return cell

rows = []
rows.append(df.columns.values.tolist())
for row in df.values.tolist():
    rows.append([_serialize_cell(c) for c in row])

print('Serialized rows:')
for r in rows:
    print(r)

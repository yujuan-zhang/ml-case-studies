"""Small shared helpers for the standalone learning exercises."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent


def read_table(path, columns, **kwargs):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f'Input not found: {path}. See README.md for the synthetic example command.')
    table = pd.read_excel(path, **kwargs) if path.suffix.lower() == '.xlsx' else pd.read_csv(path, **kwargs)
    missing = sorted(set(columns) - set(table.columns))
    if missing:
        raise ValueError(f'{path.name} is missing columns: {", ".join(missing)}')
    if table.empty:
        raise ValueError(f'{path.name} has no rows.')
    return table


def write_json(result, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    path.write_text(text)
    print(text, end='')
    print(f'Saved {path}')

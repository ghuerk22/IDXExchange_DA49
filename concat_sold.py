import pandas as pd
from datetime import date, timedelta

data_dir = '/Users/alainshi/Desktop/IDX Monthly/Raw CSV Files'
output_dir = '/Users/alainshi/Desktop/IDX Monthly/Concat Listings'

through = date.today().replace(day=1) - timedelta(days=1)

tables = []
rows_read = 0

for yr in range(2024, through.year + 1):
    last_month = through.month if yr == through.year else 12

    for mo in range(1, last_month + 1):
        path = f'{data_dir}/CRMLSSold{yr}{mo:02d}.csv'
        try:
            table = pd.read_csv(path)
        except FileNotFoundError:
            table = pd.read_csv(path.replace('.csv', '_filled.csv')).iloc[:, :-2]

        tables.append(table)
        rows_read += len(table)

combined = pd.concat(tables)

print(f'Sold rows before concatenation: {rows_read}')
print(f'Sold rows after concatenation: {len(combined)}')

rows_before_filter = len(combined)
combined = combined[combined['PropertyType'] == 'Residential']

print(f'Sold rows before filtering: {rows_before_filter}')
print(f'Sold rows after filtering: {len(combined)}')

combined.to_csv(f'{output_dir}/CRMLSSoldFinal.csv', index=False)

# Sold rows before concatenation: 639878
# Sold rows after concatenation: 639878

# Sold rows before filtering: 639878
# Sold rows after filtering: 430437

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
        path = f'{data_dir}/CRMLSListing{yr}{mo:02d}.csv'
        table = pd.read_csv(path)
        tables.append(table)
        rows_read += len(table)

combined = pd.concat(tables)

print(f'Listing rows before concatenation: {rows_read}')
print(f'Listing rows after concatenation: {len(combined)}')

rows_before_filter = len(combined)
combined = combined[combined['PropertyType'] == 'Residential']

print(f'Listing rows before filtering: {rows_before_filter}')
print(f'Listing rows after filtering: {len(combined)}')

combined.to_csv(f'{output_dir}/CRMLSListingFinal.csv', index=False)

# Listing rows before concatenation: 930311
# Listing rows after concatenation: 930311

# Listing rows before filtering: 930311
# Listing rows after filtering: 591980

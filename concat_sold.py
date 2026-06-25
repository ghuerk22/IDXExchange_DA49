import pandas as pd
from datetime import date, timedelta

csv_dir = '/Users/alainshi/Desktop/IDX Monthly'
output_dir = f'{csv_dir}/Concat Listings'

last_completed = date.today().replace(day=1) - timedelta(days=1)
end_year = last_completed.year
end_month = last_completed.month

year = 2024
month = 1

sold_df = []
sold_row_count = 0

while (year < end_year) or (year == end_year and month <= end_month):
    base = f'{csv_dir}/CRMLSSold{year}{month:02d}'

    # some sold months only exist as _filled exports (two extra columns at the end)
    try:
        sold = pd.read_csv(f'{base}.csv')
    except FileNotFoundError:
        sold = pd.read_csv(f'{base}_filled.csv')
        sold = sold.iloc[:, :-2]

    sold_df.append(sold)
    sold_row_count += len(sold)

    month += 1
    if month > 12:
        month = 1
        year += 1

sold_final = pd.concat(sold_df)

print(f'Sold rows before concatenation: {sold_row_count}')
print(f'Sold rows after concatenation: {len(sold_final)}')

before_filter = len(sold_final)
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']
after_filter = len(sold_final)

print(f'Sold rows before filtering: {before_filter}')
print(f'Sold rows after filtering: {after_filter}')

sold_final.to_csv(f'{output_dir}/CRMLSSoldFinal.csv', index=False)

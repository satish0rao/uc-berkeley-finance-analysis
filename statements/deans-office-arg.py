import pandas as pd
import sys

filename = 'expenditures.csv'

if (len(sys.argv) > 1):
    filename = sys.argv[1]

a = pd.read_csv(filename)

a.columns
a['Unnamed: 1']
print a[a['Unnamed: 0'].notnull & a['Unnamed: 0'].str.lower().str.contains('dean')].fillna('0')['Unnamed: 1'].str.replace(',','').str.replace('-','0').str.replace('(','-').str.replace(')','').astype(int).sum()

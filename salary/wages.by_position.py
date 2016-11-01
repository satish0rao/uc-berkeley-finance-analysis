import pandas as pd
import os

a = pd.read_csv("data/2015_UniversityOfCalifornia.csv")
b = a[a['Department / Subdivision']== 'UC - Berkeley']
c = b.groupby('Position')
c['Total Wages'].sum().to_csv("wages2015.csv")
c['Total Wages'].count().to_csv("count2015.csv")
os.system('echo \'Position,Wages\' | cat > junk')
os.system('cat junk wages2015.csv > hwages2015.csv')
os.system('echo \'Position,Count\' | cat > junk')
os.system('cat junk count2015.csv > hcount2015.csv')
d = pd.read_csv("hwages2015.csv")
d = pd.merge(d,pd.read_csv("hcount2015.csv"))
e = d.sort_values('Wages')
e.to_csv("wages.by_position.2015.csv")

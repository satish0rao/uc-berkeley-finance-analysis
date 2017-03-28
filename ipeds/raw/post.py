import pandas as pd
import copy
import sys
import math 

inst_char = pd.read_csv("hd2015.csv")

a = pd.read_csv('outfile.2014.csv')

c = a.merge(inst_char,left_on='Unnamed: 0',right_on='INSTNM')
d = c
phd = d[(d['HLOFFER']==9) & (d['Ovhd'] < 3) & (d['Ovhd'] > 0)]
phdpub = phd[phd['CONTROL']==1]

for x in [(phd,'phd.csv'),(phdpub,'phdpub.csv')]:
    a=x[0]
    num = (a['Bus/Fin']+a['Comp/Eng/Sci']+a['Mgnt']+a['Admin/Off'])*1.0
    denom = a['Inst']*1.0

    foo = num/denom
    a.insert(0,'Alt_Ovhd', foo)

    a = a.sort_values(by='Ovhd')
    a[['Unnamed: 0','Ovhd','Alt_Ovhd','CONTROL']].to_csv(x[1],index=False)

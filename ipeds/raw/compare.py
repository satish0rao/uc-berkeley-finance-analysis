import pandas as pd

uc_schools = pd.read_csv("../uc_inst_ids.csv")


def clean(fname):
    result = pd.read_csv(fname)
    return pd.merge(uc_schools,result, left_on='id',right_on='UNITID')

finance = clean("f1314_f1a.csv")
instructional = clean("sal2014_is.csv")
non_instructional = clean("sal2014_nis.csv")
enrollment = clean("ef2014c.csv")


def compare(finance,pair,enrollment,threshold=lambda(x,y) ):
    

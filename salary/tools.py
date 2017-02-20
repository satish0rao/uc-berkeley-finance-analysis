import pandas as pd
import sys

def get_positions(a, place = 'UC Berkeley', contains = '', without = 'profl',case_insensitive=False,place_tag = 'Department / Subdivision'):
    if case_insensitive:
        return a[(a[place_tag] == place) & 
                 (a['Position'].notnull()) & a['Position'].str.contains(contains) & 
                 ( ~a['Position'].str.contains(without))]
    else:
        return a[(a[place_tag] == place) & 
                 (a['Position'].notnull()) & a['Position'].str.lower().str.contains(contains) & 
                 ( ~a['Position'].str.lower().str.contains(without))]


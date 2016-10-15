import pandas as pd


#a = pd.read_csv("ucpay2005.csv")

#a[a['title'].notnull() & a['title'].str.lower().str.contains('vice chan')].describe()

#b = pd.read_csv("2014_UniversityOfCalifornia.csv")

#b[b['Department / Subdivision'] == 'UC \x96 Berkeley'].describe()


def recent_csv(a,place,title="",pay_lb = 0.0):
    return a[(a['Department / Subdivision'] == place)  &
             (a['Regular Pay'] > pay_lb) &
             (a['Position'].str.lower().str.contains(title))]

def old_csv(a,place,title="",pay_lb = 0.0):
    return a[(a['campus'] == place)  &
             a['base'].notnull() &
             (a['base'] > pay_lb) &
             a['title'].str.lower().str.contains(title)]
    

xlator = {'UC - Berkeley': 'BERKELEY', 
          'UC - Santa Barbara': 'SANTA BARBARA', 
          'UC - Santa Cruz':'SANTA CRUZ', 
          'UC - Riverside':'RIVERSIDE',
          'UC - Los Angeles': 'LOS ANGELES',
          'UC - San Diego': 'SAN DIEGO',
          'UC - Irvine':'IRVINE',
          'UC - Davis': 'DAVIS'
      }

def id(places):
    return places


def xlate_places(places):
    result = []
    for p in places:
        result.append(xlator[p])
    return result

def table(a,places=['UC - Berkeley'],titles = [''],old=False, lb=0.0):
    result = []
    for place in places:
        totals = {'Place': place }
        for title in titles:
            if title == '':
                column_title = 'all'
            else:
                column_title = title
            if old:
                res = old_csv(a,place,title,lb)['base']
            else:
                res = recent_csv(a,place,title,lb)['Total Wages'] + recent_csv(a,place,title,lb)['Total Retirement and Health Cost'] 
                
                
            totals[column_title + '_pay'] = res.sum()
            totals[column_title + '_count'] =res.count()
        if len(titles)>= 2:
            pay_denom = 0.0
            cnt_denom = 0.0
            pay_num = 0.0
            cnt_num = 0.0
            for title in titles:
                if title == '':
                    column_title = 'all'
                    pay_denom = totals[column_title + '_pay']
                    cnt_denom = totals[column_title + '_count']
                else:
                    column_title = title
                    pay_num += totals[column_title + '_pay']
                    cnt_num += totals[column_title + '_count']
            if pay_denom > 0:
                for title in titles:
                    if not title == '':
                        totals[title + "_pay_frac"] = totals[title + '_pay']*1.0/pay_denom
                        totals[title + "_count_frac"] = totals[title + '_count']*1.0/cnt_denom
            # if pay_denom == 0:
            #     pay_denom = -1.0
            # if cnt_denom == 0:
            #     cnt_denom = -1.0
            totals['pay frac'] = pay_num/pay_denom
            totals['cnt frac'] = cnt_num/cnt_denom
        result.append(totals)
    return pd.DataFrame(result)


#p.table(a,places=['SANTA BARBARA', 'BERKELEY', 'DAVIS','RIVERSIDE','LOS ANGELES','SAN DIEGO','DAVIS','IRVINE','MERCED'], titles=['prof',''],old=True, lb = 37500)

#p.table(b,places=['UC - Santa Barbara', 'UC - Santa Cruz', 'UC \x96 Berkeley','UC - Riverside'], titles=['prof',''],lb = 50000)

csvs = {}

for x in ["2013","2014","2015"]:
    csvs[x] = pd.read_csv('data/' + x+ '_UniversityOfCalifornia.csv')

old_csvs = {}

for x in ['2011']:
    old_csvs[x] = pd.read_csv('data/ucpay'+x + '.csv',sep='\t')

print "Exploring Jobtitles..."
print "Most Common Titles..."
for place in ['UC - Berkeley', 'UC - Santa Barbara']:
    a = csvs['2014']
    print "....for ", place
    print a[(a['Department / Subdivision']== place)]['Position'].value_counts().head(n=30)

print "Types of Profs 2014"
for place in ['UC - Berkeley', 'UC - Santa Barbara']:
    a = csvs['2014']
    print
    print "...for ", place
    print a[(a['Department / Subdivision']== place) & a['Position'].str.contains('Prof') & ( ~a['Position'].str.contains('Profl'))]['Position'].unique()

print
print "Types of Teaching Assts"
for place in ['UC - Berkeley', 'UC - Santa Barbara']:
    a = csvs['2014']
    print
    print "...for ", place
    print a[(a['Department / Subdivision']==place) & a['Position'].str.contains('Teachg Asst') & ( ~a['Position'].str.contains('Profl'))]['Position'].unique()


print
print "Types of Teaching Assts"
for place in ['UC - Berkeley', 'UC - Santa Barbara']:
    a = csvs['2014']
    print
    print "...for ", place
    print a[(a['Department / Subdivision']==place) & a['Position'].str.contains('Teachg Asst') & ( ~a['Position'].str.contains('Profl'))]['Position'].unique()


tables_cutoff = {}

for (x,y) in [('2013',45000),('2014',47500),('2015',50000)]:
    #print x
    print 
    print "Prof/Lect Pay Fraction Table for %s above pay %d " %(x,y)
    tables_cutoff[x] = table(csvs[x],places=['UC - Santa Barbara', 'UC - Santa Cruz', 'UC - Berkeley','UC - Riverside'], titles=['lect', 'prof',''],lb = y)
    print tables_cutoff[x]
    name = "output/prof_lect.%s.thresh.%d.csv" % (x,y)
    tables_cutoff[x].to_csv(name,index=False)


def compute_summary(tables,key_column,data_column,keys,file_name):
    data = []
    data_names = []
    for x in keys:
        data.append(tables[x][[key_column,data_column]].set_index('Place'))
    result = pd.concat(data,axis=1)
    new_col_names = []
    for x in keys:
        new_col_names.append(data_column + "_" + x)
    result.columns = new_col_names
    result.to_csv(file_name)
    print result
    

print "Professor Lecturer Threshold Summary..."
compute_summary(tables_cutoff,"Place","pay frac",['2013','2014','2015'],"output/prof_lect.thresh.summary.csv")

tables_all = {}

for x in ['2013','2014','2015']:
    #print x
    print
    print "Prof/Lect Pay Fraction Table for %s all pay" % x
    tables_all[x] = table(csvs[x],places=['UC - Santa Barbara', 'UC - Santa Cruz', 'UC - Berkeley','UC - Riverside'], titles=['lect', 'prof',''])
    print "Prof/Lect Pay Fraction Table for ", x
    print tables_all[x]
    name = "output/prof_lect.%s.all.csv" % x
    tables_all[x].to_csv(name,index=False)

print "Professor Lecturer All Summary..."
compute_summary(tables_all,"Place","pay frac",['2013','2014','2015'],"output/prof_lect.all.summary.csv")

ta_tables_all = {}

for x in ['2013','2014','2015']:
    #print x
    print
    print "Teaching Pay Fraction Table for %s all pay" % x
    ta_tables_all[x] = table(csvs[x],places=['UC - Santa Barbara', 'UC - Santa Cruz', 'UC - Berkeley','UC - Riverside'], titles=['teachg asst',''])
    print "Teaching Asst Pay Fraction Table for ", x
    print ta_tables_all[x]
    name = "output/teach_asst.%s.all.csv" % x
    ta_tables_all[x].to_csv(name,index=False)


print "Professor Lecturer All Summary..."
compute_summary(ta_tables_all,"Place","pay frac",['2013','2014','2015'],"output/ta.summary.csv")



def get_positions(a, place = 'UC Berkeley', contains = '', without = 'profl'):
    return a[(a['Department / Subdivision'] == place) & (a['Position'].notnull()) & a['Position'].str.lower().str.contains(contains) & ( ~a['Position'].str.lower().str.contains(without))]

def old_get_positions(a,place,title="",without='XXXXX', pay_lb = 0.0):
    return a[(a['campus'] == place)  &
             a['base'].notnull() &
             (a['base'] > pay_lb) &
             a['title'].str.lower().str.contains(title) &
             ~a['title'].str.lower().str.contains(without)]

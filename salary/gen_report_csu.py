import pandas as pd
import sys

place = 'State Polytech University, San Luis Obispo'

place_tag = 'Entity Name'
datafile = "data/2015_CaliforniaStateUniversity.csv"

if len(sys.argv) > 1:
    place = sys.argv[1]

print "Generating report for ", place

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

def get_positions(a, place = 'UC Berkeley', contains = '', without = 'XXXXX',case_insensitive=False):
    if case_insensitive:
        return a[(a[place_tag] == place) & 
                 (a['Position'].notnull()) & a['Position'].str.contains(contains) & 
                 ( ~a['Position'].str.contains(without))]
    else:
        return a[(a[place_tag] == place) & 
                 (a['Position'].notnull()) & a['Position'].str.lower().str.contains(contains) & 
                 ( ~a['Position'].str.lower().str.contains(without))]


def excluder(a,exclude_list=[],column_name='Position'):
    for x in xrange(0,len(exclude_list)):
        a = a[~a[column_name].str.lower().str.contains(exclude_list[x])]
    return a

def old_excluder(a,exclude_list=[],column_name='Position'):
    return excluder(a,exclude_list,column_name='title')

def basic_report_pay(a,title_name='',match_list=[],exclude_list=[],place=place,old=False,case_insensitive=False,category='Total Wages'):
    amount = category
    if old:
        getter = old_get_positions
        excluding = old_excluder
        title = 'title'
        if category == 'Total Wages':
            amount = 'gross'
        elif category == 'Regular Pay':
            amount = 'base'
    else:
        getter = get_positions
        excluding = excluder
        title = 'Position'
        amount = category

    got_this = getter(a,place,match_list[0],case_insensitive=case_insensitive)
    for i in xrange(1,len(match_list)):
        got_this = pd.concat([got_this,
                              getter(a,place,match_list[i],case_insensitive=case_insensitive)])

    got_this = excluding(got_this,exclude_list)

    print
    print "%s Position titles: all\n" % title_name, got_this[title].value_counts()
    #print "Professor Position titles: lease common\n", profs2011['title'].value_counts().tail()
    print "%s Count: " % title_name , got_this[title].count()
    print "%s %s: " % (title_name, category), got_this[amount].sum()
    print
    return got_this[amount].sum()


print "**************"
print "***%s 2015***" % place
print "**************"

a2015 = pd.read_csv(datafile)


teaching = basic_report_pay(a2015,title_name='Professors',match_list=['faculty','chair'],exclude_list=[])
teaching += basic_report_pay(a2015,title_name='Lecturer',match_list=['lect'], exclude_list=['ellect','elect','collect'])
teaching += basic_report_pay(a2015,title_name='Teaching Assistant',match_list=['teachg'], exclude_list=[])
teaching += basic_report_pay(a2015,title_name='Teacher',match_list=['teacher'], exclude_list=[])
research =basic_report_pay(a2015,title_name='GSR',match_list=['gsr'], exclude_list=[])
research += basic_report_pay(a2015,title_name='PostDoc',match_list=['postdoc'], exclude_list=[])
research += basic_report_pay(a2015,title_name='Research Associates',match_list=['res'], exclude_list=['prof','survey','computer','stores'])
research += basic_report_pay(a2015,title_name='Scientist ',match_list=['scientist'], exclude_list=['prof','survey','computer','stores'])



athletics = basic_report_pay(a2015,title_name='Coaches',match_list=['coach'],exclude_list=[])
athletics += basic_report_pay(a2015,title_name='Athletics',match_list=['ath'],exclude_list=['coach'])
athletics += basic_report_pay(a2015,title_name='Trainers', match_list=['train'],exclude_list=['coach','ath'])

deans = basic_report_pay(a2015,title_name='Deans',match_list=['dean'],exclude_list=[])
vcs = basic_report_pay(a2015,title_name='VC',match_list=['VC'],exclude_list=[],case_insensitive=True)

svc = basic_report_pay(a2015,title_name='Food SVC',match_list=['food'],exclude_list=[])


print "Teachers    : ", teaching
print "Researchers : ", research
print "Athletics   : ", athletics
print "Total Wages : ", a2015[a2015[place_tag] == place]['Total Wages'].sum()

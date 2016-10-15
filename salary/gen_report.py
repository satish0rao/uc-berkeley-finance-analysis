import pandas as pd
import sys

place = 'UC - Berkeley'

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

def get_positions(a, place = 'UC Berkeley', contains = '', without = 'profl',case_insensitive=False):
    if case_insensitive:
        return a[(a['Department / Subdivision'] == place) & 
                 (a['Position'].notnull()) & a['Position'].str.contains(contains) & 
                 ( ~a['Position'].str.contains(without))]
    else:
        return a[(a['Department / Subdivision'] == place) & 
                 (a['Position'].notnull()) & a['Position'].str.lower().str.contains(contains) & 
                 ( ~a['Position'].str.lower().str.contains(without))]

old_place = xlator[place]

def old_get_positions(a,place,title="",without='XXXXX', pay_lb = 0.0,case_insensitive=False):
    if case_insensitive:
        return a[(a['campus'] == place)  &
                 a['gross'].notnull() &
                 (a['gross'] > pay_lb) &
                 a['title'].str.contains(title) &
                 ~a['title'].str.contains(without)]
    else:
        return a[(a['campus'] == place)  &
                 a['gross'].notnull() &
                 (a['gross'] > pay_lb) &
                 a['title'].str.lower().str.contains(title) &
                 ~a['title'].str.lower().str.contains(without)]


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
        got_this = pd.concat(got_this,
                             getter(a,place,match_list[i]))

    got_this = excluding(got_this,exclude_list)

    print
    print "%s Position titles: all\n" % title_name, got_this[title].value_counts()
    #print "Professor Position titles: lease common\n", profs2011['title'].value_counts().tail()
    print "%s Count: " % title_name , got_this[title].count()
    print "%s %s: " % (title_name, category), got_this[amount].sum()
    print
    return got_this[amount].sum()


a2011 = pd.read_csv("data/ucpay2011.csv",sep='\t')

profs2011_pre = old_get_positions(a2011,old_place,'prof','professional')
profs2011 = old_get_positions(profs2011_pre,old_place,'prof','prof\'l')


lect2011 = old_get_positions(a2011,old_place,'lect','intellectual')
lect2011 = old_get_positions(lect2011,old_place,'lect','elect')
lect2011 = old_get_positions(lect2011,old_place,'lect','collect')

print "**************"
print "***%s 2011***" % place
print "**************"

basic_report_pay(a2011,title_name='Professors', match_list=['prof'], exclude_list=['prof\'l','professional'],place=old_place, old=True)


basic_report_pay(a2011,title_name='lect', match_list=['lect'],exclude_list=['ellect','elect','collect'],place=old_place, old=True)


print "**************"
print "***%s 2015***" % place
print "**************"

a2015 = pd.read_csv("data/2015_UniversityOfCalifornia.csv")


teaching = basic_report_pay(a2015,title_name='Professors',match_list=['prof'],exclude_list=['profl'])
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
print "Total Wages : ", a2015[a2015['Department / Subdivision'] == place]['Total Wages'].sum()

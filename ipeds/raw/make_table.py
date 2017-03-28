
import pandas as pd
import copy
import sys
import math 

test_schools = pd.read_csv("uc_inst_ids.csv")
test_schools = pd.read_csv("all_colleges.csv")

outfile = 'outfile.csv'
if len(sys.argv) > 2:
    outfile = sys.argv[2]

sub = True
sub_aux = True
sub_num_res_ovhd = True

finance_year = '1415'
sal_year = '2015'
if (len(sys.argv) > 1):
    if sys.argv[1] == '2015':
        finance_year = '1415'
        sal_year = '2015'
    elif sys.argv[1] == '2014':
        finance_year = '1314'
        sal_year = '2014'
    elif sys.argv[1] == '2013':
        finance_year = '1213'
        sal_year = '2013'
    elif sys.argv[1] == '2012':
        finance_year = '1112'
        sal_year = '2012'
    else:
        pass




def clean(fname):
    result = pd.read_csv(fname)
    return pd.merge(test_schools,result, left_on='id',right_on='UNITID')

finance_private = "f%s_f2.csv" % finance_year
priv_finance = clean(finance_private)
priv_finance_varlist = pd.read_csv("f1415_f2_varlist.csv")
priv_finance_clean_columns = pd.read_csv("fields.fin.priv.csv")['field']

finance_public = "f%s_f1a.csv" % finance_year
finance = clean(finance_public)
finance_varlist = pd.read_csv("f1314_f1a_varlist.csv")
#finance_varlist = pd.read_csv("f1112_f1a_varlist.csv")
# finance_clean_columns = [x for x in finance.columns 
#                          if not x in ['UNITID','id','name']]
finance_clean_columns = pd.read_csv("fields.fin.csv")['field']

is_file = "sal%s_is.csv" % sal_year
instructional = clean(is_file)
instructional_varlist = pd.read_csv("sal2014_is_varlist.csv")

#instructional_varlist = pd.read_csv("sal2012_is_varlist.csv")
# instructional_clean_columns = [x for x in instructional.columns 
#                                if not x in ['UNITID','id','name']]
instructional_clean_columns = pd.read_csv("fields.is.csv")['field']

nis_file = 'sal%s_nis.csv' % sal_year
non_instructional = clean(nis_file)
non_instructional_varlist = pd.read_csv("sal2014_nis_varlist.csv")
#non_instructional_varlist = pd.read_csv("sal2012_nis_varlist.csv")
# non_instructional_clean_columns = [x for x in non_instructional.columns 
#                                    if not x in ['UNITID','id','name']]
non_instructional_clean_columns = pd.read_csv("fields.nis.csv")['field']

#enrollment = clean("ef2014c.csv")


def value_ats_of(a,ats,values,item):
    # print "ats_of", ats,values
    result = a[a[ats[0]]==values[0]]
    for x in xrange(1,len(ats)):
        result = result[result[ats[x]] == values[x]]
    lst = result[item].tolist()
    if len(lst)<1:
        return 0
    else:
        return lst[len(lst)-1]

def value_at_of(a,at,value,item):
    result = a[a[at]==value]
    lst = result[item].tolist()
    if len(lst)<1:
        return 0
    else:
        return lst[len(lst)-1]
    
def name_to_value(a,name,item):
    return value_ats_of(a,['name'],[name],item)


pairs = []
for x in test_schools['name']:
    pairs.append([['name'],[x]])
#pairs = pairs[0:100]

table = {}

for tup in [["Finance",pairs,finance,finance_clean_columns,finance_varlist],
            ["Private Finance",pairs,priv_finance,priv_finance_clean_columns,priv_finance_varlist],
            ["Instruction",map(lambda(x): [x[0]+ ['ARANK'], x[1] + [7]],copy.deepcopy(pairs)),
             instructional,instructional_clean_columns,instructional_varlist],
            ["Non_instruction",pairs,
             non_instructional,non_instructional_clean_columns,
             non_instructional_varlist]]:
    for pair in tup[1]:
        institution = pair[1][0]
        #print institution
        if not (institution in table.keys()):
            table[institution] = {}
        for x in tup[3]:
            table[institution][x] = name_to_value(tup[2],institution,x)

#print table

a = pd.DataFrame.from_dict(table,orient='index')

print a.columns 
#([u'F1C062', u'F1C112', u'SAOUTLT', u'SANIT02', u'SANIT06', u'F2E072', u'SANIT01', u'F2E052', u'SANIT07', u'SANIT05', u'SANIT12'],
a.columns = ['Stdt','Aux','Inst','Res','Bus/Fin','Prv/Aux','Non-inst','Prv/Stdt','Comp/Eng/Sci','Mgnt','Admin/Off']

def millions(val):
    return int(val/1000000)

a = a.dropna()

b = a.applymap(lambda x: int(x/1000))

#print b

denom = b['Inst']

#print denom

num = 1.0*(b['Non-inst'] - b['Res'])

if sub:
    if sub_num_res_ovhd:
        num = num-.57*b['Res']
    if sub_aux:
        num = num - b['Aux']-b['Prv/Aux']
else:
    num = b['Bus/Fin']+b['Comp/Eng/Sci']+b['Mgnt']+b['Admin/Off']

#a.columns = ['Stdt','Aux','Inst','Res','Bus/Fin','Prv/Aux','Non-inst','Prv/Stdt','Comp/Eng/Sci','Mgnt','Admin/Off']

#print num

c = num/denom
#print c

b['Ovhd'] = c.apply(lambda x: -10 if (math.isnan(x)) else int(max(min(x,100),-100)*100)/100.0)

d = b.reindex_axis(['Ovhd','Inst','Res','Non-inst','Bus/Fin','Comp/Eng/Sci','Mgnt','Admin/Off','Stdt','Aux','Prv/Stdt','Prv/Aux'],axis=1).sort_values(by='Ovhd')
#print d


#sanjay_file = "for_sanjay.%s.csv" % sal_year
d.to_csv(outfile)

def compute_effective_overhead(table):
    names = []
    acads = []
    researchs = []
    nises = []
    ovhds = []
    mngts = []
    for x in table.keys():
        acad = table[x]['SAOUTLT']
        res = table[x]['SANIT02']
        nis = table[x]['SANIT01']
        mngt = table[x]['SANIT05']
        mngt_ovhd = ((mngt)*1.0)/acad
        ovhd = ((nis-res)*1.0)/acad
        print x, ovhd, acad,res,nis
        names.append(x)
        acads.append(int(acad/1000))
        researchs.append(int(res/1000))
        nises.append(int(nis/1000))
        ovhds.append(int((ovhd*100)))
        mngts.append(int(mngt/1000))
        
    result = pd.DataFrame({'Name': names,'Ovhd':ovhds,'Inst':acads,'Rsch':researchs,'NIS': nises,'MGT':mngts})
    a = result.sort_values(by = 'Ovhd',axis=0)
    b = a.reindex_axis(['Name','Ovhd','MGT','Inst','Rsch','NIS'],axis=1)
    print b

#compute_effective_overhead(table)

exit(0) 



# pairs=[[['name'],['University of California-Berkeley']],
#        [['name'],['University of California-San Diego']],
#        [['name'],['University of California-Davis']],
#        [['name'],['University of California-Los Angeles']],
#        [['name'],['University of California-Santa Barbara']],
#        [['name'],['University of California-Santa Cruz']],
#        [['name'],['University of California-Irvine']],
#        [['name'],['University of California-Riverside']],
#        [['name'],['University of Illinois at Urbana-Champaign']],
#        [['name'],['University of Michigan-Ann Arbor']],
#        [['name'],['University of Virginia-Main Campus']],
#        [['name'],['Princeton University']],
#        [['name'],['Harvard University']],
#        [['name'],['Williams College']],
#        [['name'],['Stanford University']],
#        [['name'],['Massachusetts Institute of Technology']],
#        [['name'],['Carnegie Mellon University']]]
       
#       [['name'],['University of California-Merced']]]

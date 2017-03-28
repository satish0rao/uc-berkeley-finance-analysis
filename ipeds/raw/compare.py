import pandas as pd
import copy

uc_schools = pd.read_csv("../uc_inst_ids.csv")


def clean(fname):
    result = pd.read_csv(fname)
    return pd.merge(uc_schools,result, left_on='id',right_on='UNITID')

finance = clean("f1314_f1a.csv")
finance_varlist = pd.read_csv("f1314_f1a_varlist.csv")
finance_clean_columns = [x for x in finance.columns 
                         if not x in ['UNITID','id','name']]

instructional = clean("sal2014_is.csv")
instructional_varlist = pd.read_csv("sal2014_is_varlist.csv")
instructional_clean_columns = [x for x in instructional.columns 
                               if not x in ['UNITID','id','name']]

non_instructional = clean("sal2014_nis.csv")
non_instructional_varlist = pd.read_csv("sal2014_nis_varlist.csv")
non_instructional_clean_columns = [x for x in non_instructional.columns 
                                   if not x in ['UNITID','id','name']]


enrollment = clean("ef2014c.csv")


def value_ats_of(a,ats,values,item):
    # print "ats_of", ats,values
    result = a[a[ats[0]]==values[0]]
    for x in xrange(1,len(ats)):
        result = result[result[ats[x]] == values[x]]
    lst = result[item].tolist()
    if len(lst)<1:
        return -1
    else:
        return lst[len(lst)-1]

def value_at_of(a,at,value,item):
    result = a[a[at]==value]
    lst = result[item].tolist()
    if len(lst)<1:
        return -1
    else:
        return lst[len(lst)-1]
    
def name_to_value(a,name,item):
    return value_ats_of(a,['name'],[name],item)

def compare(finance,pairs,items,items_desc,enrollment,threshold= lambda x,y: x > y):
    result = []
    # print "Pairs",pairs
    for x in items:
        a = value_ats_of(finance,pairs[0][0],pairs[0][1],x)
        b = value_ats_of(finance,pairs[1][0],pairs[1][1],x)
        if threshold(a,b):
            result.append([x,a,b,
                           value_at_of(items_desc,'varname',x,'varTitle')])
    return result

def compare1(finance,pairs,items,items_desc,enrollment,threshold= lambda x,y: x > y):
    # print "Pairs",pairs
    result = []
    for x in items:
        lst = []
        for i in range(0,len(pairs)):
            lst.append(value_ats_of(finance,pairs[i][0],pairs[i][1],x))
        result.append([x, value_at_of(items_desc,'varname',x,'varTitle'), lst])
    return result


def report_diffs(data,pairs,items,items_desc,enrollment,threshold=lambda x,y: x > y):
    differences = compare(data,
                          pairs,
                          items,
                          items_desc,
                          enrollment,
                          threshold=threshold)
    print "Dude, Really?"
    for x in differences:
        if True or ('alaries' in x[3]) or ("ther" in x[3]):
            print x[3]
            if x[1] > 1000000:
                print "%d%s" % ((x[1]+500000)/1000000,"M"),"%d%s" % ((x[2]+500000)/1000000,"M")
            else:
                print x[1],x[2]

def report_diffs1(data,pairs,items,items_desc,enrollment,threshold=lambda x,y: x > y):
    differences = compare1(data,
                          pairs,
                          items,
                          items_desc,
                          enrollment,
                          threshold=threshold)
    print "Dude, Really?"
    for x in differences:
        if True or ('alaries' in x[1]) or ("ther" in x[1]):
            if ((isinstance(x[2][0],int)) or (isinstance(x[2][0],float))) and (x[2][0] > 0):
                print x[1],x[0],"hello"
                for i in xrange(0,len(x[2])):
                    if x[2][i] > 1000000:
                        print "%d%s" % ((x[2][i]+500000)/1000000,"M"), 
                    else:
                        print "%d%s" % ((x[2][i]),""), 
                print



pairs=[[['name'],['University of California-Berkeley']],
       [['name'],['University of California-San Diego']],
       [['name'],['University of California-Davis']],
       [['name'],['University of California-Los Angeles']],
       [['name'],['University of California-Santa Barbara']],
       [['name'],['University of California-Santa Cruz']],
       [['name'],['University of California-Irvine']],
       [['name'],['University of California-Riverside']],
       [['name'],['University of Illinois at Urbana-Champaign']],
       [['name'],['University of Michigan-Ann Arbor']],
       [['name'],['University of Virginia-Main Campus']],
       [['name'],['Princeton University']],
       [['name'],['Harvard University']],
       [['name'],['Williams College']],
       [['name'],['Stanford University']],
       [['name'],['Massachusetts Institute of Technology']],
       [['name'],['Carnegie Mellon University']]]
       

#       [['name'],['University of California-Merced']]]



for tup in [["Finance",pairs,finance,finance_clean_columns,finance_varlist],
            ["Instruction",map(lambda(x): [x[0]+ ['ARANK'], x[1] + [7]],copy.deepcopy(pairs)),
             instructional,instructional_clean_columns,instructional_varlist],
            ["Non_instruction",pairs,
             non_instructional,non_instructional_clean_columns,
             non_instructional_varlist]]:
    print
    print "table ", tup[0]
    pairs = tup[1]
    data = tup[2]
    items = tup[3]
    desc = tup[4]
    report_diffs1(data,
                  pairs,
                  items,
                  desc,
                  enrollment,
                  threshold=lambda x,y: (isinstance(x,(int,float)) and (True or x > y)))

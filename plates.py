import numpy as np
import pandas as pd
from collections import OrderedDict
from itertools import product
from os import path


def read_plate(fname,start=3,end=-3):

    if fname[-4:] != '.txt':
        fname = fname+'.txt'
    with open(fname) as f:
        agg = []
        for i,t in enumerate(f.readlines()[start:end]):
            if i == 0:
                try:
                    agg.append(np.asarray([float(s.replace('\x00','')) for s in t.split()][1:]))
                except: print [s.replace('\x00','') for s in t.split()][3:-3]
            else:
                agg.append(np.asarray([float(s.replace('\x00','')) for s in t.split()]))

    agg = pd.DataFrame(np.vstack(agg))
    agg.index = ['A','B','C','D','E','F','G','H']
    agg.columns = range(1,13)
    return agg

def collapse_plate(df,name='Value'):
    temp = df.unstack().reset_index()
    temp.columns = ['Col','Row',name]
    temp['Well']=temp.apply(lambda row: row['Row']+str(row['Col']),axis=1)
    return temp[['Well',name]]

def tuple_to_name(t):
    ''' Construct a filename from a tuple of values '''
    return path.join('_'.join(t)+'.txt')

def construct_names(base_path,properties,tuple_to_name_fun):
    ''' Take the product of all the dictionarys' values in d, and convert to filenames.
    Inputs:
        - base_path, the base path
        - properties, a collections.OrderedDict
    Returns:
        - the order of Properties in tuples
        - a list of tuples (values, filename)
            - values: the values of each property in order
            - filename: the corresponding filename
    '''
    filenames = [path.join(base_path,tuple_to_name_fun(t)) for t in product(*[p.values() for p in properties.values()])]
    values = [t for t in product(*[p.keys() for p in properties.values()])]
    return properties.keys(),zip(values,filenames)

def aggregate_plates(base_path,properties,start=3,end=-3,tuple_to_name_fun=tuple_to_name):
    columns, values_and_filenames = construct_names(base_path,properties,tuple_to_name_fun)

    agg = []
    for values,filename in values_and_filenames:
        agg.append(collapse_plate(read_plate(filename,start=start,end=end)).assign(**dict(zip(columns,values))))

    agg = pd.concat(agg).reset_index(drop=True)
    return agg

# EXAMPLE
# properties = OrderedDict()
#
# properties['Bug'] = {
#     'control':'iso',
#     'PAE':'PAE',
#     'PAG':'PAG',
#     'PC':'PC',
#     'PF':'PF',
#     'PP':'PP',
#     'PS':'PS'
# }
#
# properties['Site'] = {
#     'Middlesex Fells':'MF',
#     'MIT Killian':'KC'
# }
#
# properties['Rep'] = {
#     1:'1',
#     2:'2'
# }
#
# properties['Channel'] = {
#     'GFP':'GFP',
#     'OD':'OD'
# }
#
# properties['Timepoint'] = {
#     0:'t0',
#     1:'t1',
#     2:'t2',
#     3:'t3'
# }
#
# data = aggregate_plates(base_path, properties)

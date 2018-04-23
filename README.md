# plateprocess

Python library for processing output of the Beta SpectraMax Plate Reader. 

* This plate reader appears to output different formats at random, I'm not sure why. The function `read_plate` will stay updated with `try` flow control to read new formats as they appear. 

*  This library also contains a function `aggregate_plates` that will automatically read and annotate data across plates. 

EXAMPLE  

```
properties = OrderedDict()

properties['Bug'] = {
    'control':'iso',
    'PAE':'PAE',
    'PAG':'PAG',
    'PC':'PC',
    'PF':'PF',
    'PP':'PP',
    'PS':'PS'
}

properties['Site'] = {
    'Middlesex Fells':'MF',
    'MIT Killian':'KC'
}

properties['Rep'] = {
    1:'1',
    2:'2'
}

properties['Channel'] = {
    'GFP':'GFP',
    'OD':'OD'
}

properties['Timepoint'] = {
    0:'t0',
    1:'t1',
    2:'t2',
    3:'t3'
}

data = aggregate_plates(base_path, properties)
```

#!/usr/bin/env python3
#--Ayan Chakrabarti <ayan@wustl.edu>

import sbplot as sb
import numpy as np
import sys
import re


# Parse command line args
if len(sys.argv) == 1:
    sys.exit("USAGE: log2sb.py ID:/path/to/log/file [ID2:/path/to/log/file/2] ...")
v = sys.argv[1:]
files = [f.split(':')[-1] for f in v]
exps = [v[i].split(':')[0] if len(v[i].split(":")) == 2 else str(i) for i in range(len(v))]


# Parse log files
plots, tags = [], {}
for j in range(len(files)):
    lines = re.sub('[\ ]+',' ',re.sub('[,=]',' ',open(files[j]).read()))
    lines = [[q[0]]+q[1].split(' ') for q in re.findall(r'\[(\d+)\] ([^\n]*)\n',lines)]

    data = {}
    for l in lines:
        it = int(l[0])
        for k in range(1,len(l)-1,2):
            tag = l[k]
            if tag not in data.keys():
                data[tag] = [[],[]]

            data[tag][0].append(it)
            data[tag][1].append(float(l[k+1]))
            
    for tag in data.keys():
        tags[tag] = 1
        its = np.float32(data[tag][0])
        vals = np.float32(data[tag][1])
        nm = tag + '@' + exps[j]
        plots.append([its,vals,nm])

# Write        
sb.write_data(sys.stdout,exps,sorted(list(tags.keys())),plots)

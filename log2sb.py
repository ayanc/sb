#!/usr/bin/env python3
#--Ayan Chakrabarti <ayan@wustl.edu>

import sbplot as sb
import numpy as np
import sys
import re
import numpy as np
from scipy.signal import convolve2d as conv2
import json

HOSTURL='https://ayanc.github.io/sb/assets/'

########################## Code to output json
html_pfx='''
<html><head><link rel="stylesheet" type="text/css" href="HOSTURLsb.css">
<script src="https://cdn.plot.ly/plotly-1.31.2.min.js"></script>
<script src="HOSTURLsb.js"></script>
<script type="text/javascript">
'''.replace('HOSTURL',HOSTURL).strip('\n')

html_sfx='''
</script></head><body></body></html>
'''.strip('\n')

def smooth(x,y,xmax):
    LIM=5e2

    x2 = np.linspace(0.,xmax,LIM)
    x2 = x2[x2 <= np.max(x)]
    ln = int(np.round(3*len(x)/len(x2)))

    filt = np.linspace(-3,3,2*ln+1)
    filt = np.exp(-filt*filt/2)
    filt = filt/np.sum(filt)
    filt = filt.reshape([1,2*ln+1])
    
    y = np.pad(y,((ln,ln)),'edge')
    y = conv2(y.reshape((1,len(y))),filt,'valid').flatten()
    y = np.interp(x2,x,y)

    return list(x2),list(y)

def write_data(out,exps,tags,data):
    dstr = []
    xmax = 0
    for i in range(len(data)):
        xmax = np.max([xmax,np.max(data[i][0])])
    for i in range(len(data)):
        steps,vals = smooth(data[i][0],data[i][1],xmax)
        steps = ','.join([str(int(i)) for i in steps])
        vals = ','.join(['%.5f' % float(i) for i in vals])
        dstr.append("'" + data[i][2] + "': { x: [" + steps + "], y: [" + vals + "]}");

    out.write(html_pfx)
    out.write('exps=' + json.dumps(exps) + ';')
    out.write('tags=' + json.dumps(tags) + ';')
    out.write("data= {" + ",".join(dstr) + "};");
    out.write(html_sfx)
##########################

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
write_data(sys.stdout,exps,sorted(list(tags.keys())),plots)

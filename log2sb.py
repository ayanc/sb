#!/usr/bin/env python3
# - Ayan Chakrabarti <ayan.chakrabarti@gmail.com>
"""Convert log files to html."""

import json
import sys
import re
import numpy as np

HOSTURL = 'https://ayanc.github.io/sb/assets/'

# Code to output json
html_pfx='''
<html><head><link rel="stylesheet" type="text/css" href="HOSTURLsb.css">
<script src="https://cdn.plot.ly/plotly-1.31.2.min.js"></script>
<script src="HOSTURLsb.js"></script>
<script type="text/javascript">
'''.replace('HOSTURL', HOSTURL).strip('\n')

html_sfx='''
</script></head><body></body></html>
'''.strip('\n')


def smooth(x, y, xmax):
    """Simple fast smoother."""
    LIM=int(5e2)
    xmax = len(x)*xmax/x[-1]
    if xmax <= 2*LIM:
        return list(x), list(y)

    fac = int(np.floor(xmax/LIM))
    pad = (-len(x)) % fac
    x = np.pad(x, [[pad, 0]], 'edge')
    y = np.pad(y, [[pad, 0]], 'edge')
    x = np.mean(np.reshape(x, (-1, fac)),1)
    y = np.mean(np.reshape(y, (-1, fac)),1)

    if len(y) < 3:
        return list(x), list(y)
    return list(x), [y[0]] + list(
        0.5*y[1:-1] + 0.25*y[:-2] + 0.25*y[2:]
    ) + [y[-1]]


def write_data(out,exps,tags,data):
    dstr = []
    xmax = 0
    for i in range(len(data)):
        xmax = xmax if data[i][0][-1] < xmax else data[i][0][-1]
    for i in range(len(data)):
        steps, vals = smooth(data[i][0], data[i][1], xmax)
        steps = ','.join(['%.4e' % float(i) for i in steps])
        vals = ','.join(['%.4e' % float(i) for i in vals])
        dstr.append("'" + data[i][2]
                    + "': { x: [" + steps + "], y: ["
                    + vals + "]}")

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
    try:
        lines = re.sub('[\ ]+',' ',re.sub('[,=]',' ',open(files[j]).read()))
    except:
        continue
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

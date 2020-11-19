#!/usr/bin/env python3
# - Ayan Chakrabarti <ayan.chakrabarti@gmail.com>
"""Convert log files to interactive html plot."""

import json
import sys
import re
import numpy as np

HOSTURL = 'https://ayanc.github.io/sb/assets/'
HTML_DATA = [
    '''
<html><head>
<link rel="stylesheet" type="text/css" href="HOSTURLsb.css">
<script src="https://cdn.plot.ly/plotly-1.31.2.min.js"></script>
<script src="HOSTURLsb.js"></script>
<script type="text/javascript">
'''.replace('HOSTURL', HOSTURL).strip('\n'),
    '</script></head><body></body></html>']


def smooth(xdata, ydata, xmax, _limit=int(5e2)):
    """Simple fast smoother."""
    xmax = len(xdata)*xmax/xdata[-1]
    if xmax <= 2*_limit:
        return xdata, ydata

    fac = int(np.floor(xmax/_limit))
    pad = (-len(xdata)) % fac
    xdata = np.pad(xdata, [[pad, 0]], 'edge')
    ydata = np.pad(ydata, [[pad, 0]], 'edge')
    xdata = np.mean(np.reshape(xdata, (-1, fac)), 1)
    ydata = np.mean(np.reshape(ydata, (-1, fac)), 1)

    if len(ydata) >= 3:
        ydata[1:-1] = 0.5*ydata[1:-1] + 0.25*ydata[:-2] + 0.25*ydata[2:]
    return xdata, ydata


def write_data(out, exps, tags, data):
    """Write data to out."""
    fmtr = {'float_kind': lambda x: '%.4e' % x}
    dstr = []
    xmax = 0
    for _d in data:
        xmax = xmax if _d[0][-1] < xmax else _d[0][-1]

    for _d in data:
        steps, vals = smooth(_d[0], _d[1], xmax)
        # steps = ','.join(['%.4e' % float(j) for j in steps])
        # vals = ','.join(['%.4e' % float(j) for j in vals])
        steps = np.array2string(steps, separator=',', formatter=fmtr)
        vals = np.array2string(vals, separator=',', formatter=fmtr)
        dstr.append("\n'" + _d[2] + "': {\n x: " + steps
                    + ",\n y: " + vals + "}")

    out.write(HTML_DATA[0])
    out.write('exps=' + json.dumps(exps) + ';\n')
    out.write('tags=' + json.dumps(tags) + ';\n')
    out.write("data= {" + ",".join(dstr) + "};")
    out.write(HTML_DATA[1])


def parseargs():
    """Parse command line arguments"""
    if len(sys.argv) == 1:
        sys.exit("USAGE: log2sb.py ID:/path/to/log/file " +
                 "[ID2:/path/to/log/file/2] ...")
    args = sys.argv[1:]
    files = [f.split(':')[-1] for f in args]
    exps = [f.split(':')[0] if len(f.split(":")) == 2
            else str(i) for i, f in enumerate(args)]
    return files, exps


def getdata(files, exps):
    """Parse log files"""
    plots, tags = [], set()
    for fnm, exp in zip(files, exps):
        try:
            lines = re.sub(r'[\ ,=]+', ' ', open(fnm).read())
        except:
            continue

        data = {}
        for line in re.finditer(r'\[(\d+)\] ([^\n]*)\n', lines):
            itrs = line[1]
            _l = line[2].split(' ')
            for k in range(0, len(_l)-1, 2):
                tag, val = _l[k], _l[k+1]
                if tag not in data:
                    data[tag] = [[itrs], [val]]
                else:
                    data[tag][0].append(itrs)
                    data[tag][1].append(val)

        tags |= set(data.keys())
        for tag in data:
            its = np.float32(data[tag][0])
            vals = np.float32(data[tag][1])
            name = tag + '@' + exp
            plots.append([its, vals, name])
    return plots, sorted(list(tags))


def main():
    """Main function"""
    files, exps = parseargs()
    plots, tags = getdata(files, exps)
    write_data(sys.stdout, exps, tags, plots)


if __name__ == "__main__":
    main()

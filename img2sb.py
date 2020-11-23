#!/usr/bin/env python
"""Convert YAML to html."""

import sys
import os
import re
import itertools
import json
from glob import glob
import yaml


HOSTURL = 'https://ayanc.github.io/sb/assets/'
HTML_DATA = [
    '''
<html><head>
<link rel="stylesheet" type="text/css" href="HOSTURLsbi.css">
<script src="HOSTURLsbi.js"></script>
<script type="text/javascript">
'''.replace('HOSTURL', HOSTURL).strip('\n'),
    '</script></head><body></body></html>']


def parse(fname):
    """Convert from YAML + glob to json."""
    flist = glob('**', recursive=True)

    config = yaml.load(open(fname).read(), Loader=yaml.CLoader)
    outs = []

    # Handle each block
    for exp in config:

        # Parse block description, match files
        ename, econfig = exp.popitem()
        keys = econfig[0].split('+')
        kvals = {k: None for k in keys}
        cnames, cfiles, ckeys = [], [], []
        for idx in range(1, len(econfig)):
            cname, creg_ = econfig[idx].popitem()
            creg_ = creg_.replace('(', '(?P<').replace(')', r'>[^/\\]*)')
            creg = re.compile(creg_)
            cfile_ = [(p[0], p.groupdict()) for p in map(creg.match, flist)
                      if p is not None]
            if len(cfile_) == 0:
                sys.stderr.write("Could not find match to: %s\n" % creg_)
                sys.exit(128)
            ckey = list(cfile_[0][1].keys())
            ckvals = {k: set() for k in ckey}
            cfile = {}
            for _f in cfile_:
                cfile[':'.join(_f[1].values())] = _f[0]
                for _k in ckey:
                    ckvals[_k].add(_f[1][_k])

            for _k in ckey:
                if kvals[_k] is None:
                    kvals[_k] = ckvals[_k]
                else:
                    kvals[_k] = kvals[_k].intersection(ckvals[_k])

            cnames.append(cname)
            cfiles.append(cfile)
            ckeys.append(ckey)

        # Convert to lists of arrays
        labels = [sorted(list(kvals[k])) for k in keys]
        subexps = list(itertools.product(*labels[:-1]))
        sublist = []
        for sub in subexps:
            sdict = {keys[k]: sub[k] for k in range(len(sub))}
            jname = ', '.join(['%s=%s' % (k, sdict[k]) for k in sdict])
            rows = []
            for lastkey in labels[-1]:
                sdict[keys[-1]] = lastkey
                row = []
                for _j, ckey in enumerate(ckeys):
                    col = cfiles[_j][':'.join([sdict[k] for k in ckey])]
                    coltxt = col.split('.')
                    coltxt = '.'.join(coltxt[:-1]) + '.txt'
                    if os.path.isfile(coltxt):
                        col = [col, open(coltxt, 'r').read()]
                    row.append(col)
                rows.append(row)
            sublist.append([jname, rows])

        group = [ename, cnames, labels[-1], sublist]
        outs.append(group)

    return 'data='+json.dumps(outs)+';'


def getargs():
    """Get yaml file name or print usage."""
    if len(sys.argv) < 2:
        sys.exit("USAGE: img2sb.py yaml-file-name")
    return sys.argv[1]


def main():
    """Main function"""
    data = parse(getargs())
    sys.stdout.write(HTML_DATA[0] + data + HTML_DATA[1])


if __name__ == "__main__":
    main()

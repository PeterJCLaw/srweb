#!/usr/bin/env python

import pandocfilters as pf

def latex(s):
    return pf.RawBlock('latex', s)

def debug(string):
    print >> _f, string

def mk_columns(key, val, format_, meta):
    if key == "Para":
        value = pf.stringify(val)
        if value.startswith('//'):
            return []
    if key == "Header":
        value = pf.stringify(val)
        return pf.Header(val[0], val[1], [pf.Str(value)])

_f = None
if __name__ == "__main__":
    _f = open('/tmp/bees', 'w+')
    pf.toJSONFilter(mk_columns)

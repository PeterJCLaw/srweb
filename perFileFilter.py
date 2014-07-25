#!/usr/bin/env python

# Run on each file as we convert from markdown to html

import pandocfilters as pf

def Para(string):
    return pf.Para([pf.Str(string)])

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
    if key == "CodeBlock":
        val[0][1] = list(set(val[0][1] + ['python']))
        return pf.CodeBlock(*val)
    if key == "Div":
        attrs, children = val
        _, classes, others = attrs
        if 'warning' in classes:
            return [Para('@_@WARNING_START@_@'), pf.Div(*val), Para('@_@WARNING_END@_@')]
        if 'info' in classes:
            return [Para('@_@INFO_START@_@'), pf.Div(*val), Para('@_@INFO_END@_@')]

_f = None
if __name__ == "__main__":
    _f = open('/tmp/bees', 'w+')
    pf.toJSONFilter(mk_columns)

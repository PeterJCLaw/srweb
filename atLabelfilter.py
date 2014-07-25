#!/usr/bin/env python

import pandocfilters as pf

def latex(s):
    return pf.RawBlock('latex', s)

def debug(string):
    print >> _f, string

def mk_columns(key, val, format_, meta):
    if key == "Para":
        value = pf.stringify(val)
        if value.startswith('@@'):
            anchor = value[2:]
            return latex(r'\label{%s}' % anchor)
        if value.startswith('@_@'):
            content = value[3:-3]
            if content == 'WARNING_START':
                return latex(r"""
% .warning box
\medskip
\noindent\fcolorbox[rgb]{1,0,0}{1,0.75,0.79296875}{%
    \minipage[t]{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
""")
            if content == 'INFO_START':
                return latex(r"""
% .info box
\medskip
\noindent\fcolorbox[rgb]{0,0,1}{0.5,1,0.828125}{%
    \minipage[t]{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
""")

            if content == 'WARNING_END' or content == 'INFO_END':
                return latex(r"""
    \endminipage}
\medskip
""")

_f = None
if __name__ == "__main__":
    _f = open('/tmp/bees', 'w+')
    pf.toJSONFilter(mk_columns)

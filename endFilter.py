#!/usr/bin/env python

# Run on the all.html as we convert to latex for PDF generation

import pandocfilters as pf

def latex(s):
    return pf.RawBlock('latex', s)

def box_start(border_rgb, background_rgb):
    def colour_str(rgb):
        colours = [c/255.0 for c in rgb]
        return ",".join(str(c) for c in colours)

    border = colour_str(border_rgb)
    background = colour_str(background_rgb)

    return latex(r"""
% warning or info box
\medskip
\noindent\fcolorbox[rgb]{""" + border + "}{" + background + r"""}{%
    \minipage[t]{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
""")

def box_end():
    return latex(r"""
    \endminipage}
\medskip
""")

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
                # red, pink
                return box_start( (255, 0, 0), (255, 192, 203) )

            if content == 'INFO_START':
                # blue, aquamarine
                return box_start( (0, 0, 255), (127, 255, 212) )

            if content == 'WARNING_END' or content == 'INFO_END':
                return box_end()

_f = None
if __name__ == "__main__":
    _f = open('/tmp/bees', 'w+')
    pf.toJSONFilter(mk_columns)

#!/usr/bin/env python

DOCS_ROOT = 'content/en/docs'

files = ["index"
        ,"kit/motor_board"
        ,"kit/jointio_board"
        ,"kit/power_board"
        ,"kit/token_ring"
        ,"kit/batteries"
        ,"kit/servo_board"
        ,"programming/index"
        ,"programming/sr/servos/index"
        ,"programming/sr/index"
        ,"programming/sr/vision/index"
        ,"programming/sr/vision/markers"
        ,"programming/sr/io/index"
        ,"programming/sr/io/wait_for"
        ,"programming/sr/power/index"
        ,"programming/sr/motors/index"
        ,"troubleshooting/index"
        ,"troubleshooting/python"
        ,"troubleshooting/hardware"
        ,"tutorials/python"
        ,"tutorials/basic_motor_control"
]

import os
import os.path
import re
import subprocess

def pandoc(*args):
    args = list(args)
    args.insert(0, 'pandoc')
    subprocess.check_call(args)

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def fn_to_anchor(fn):
    return "smallpiece-internal-" + fn.replace('/', '-')

def fix_links_helper(match):
    before = match.group(1)
    orig_uri = uri = match.group(2)
    after = match.group(3)
    message = match.group(4)

    if not uri.startswith('/'):
        # External link -- leave alone
        return match.group(0)

    # Ignore anchors
    anchor_idx = uri.rfind('#')
    anchor = ''
    if anchor_idx >= 0:
        anchor = uri[anchor_idx+1:]
        uri = uri[:anchor_idx]

    #print dict(uri=uri, anchor=anchor)

    if uri.endswith('/'):
        uri += 'index'

    docs = '/docs/'
    if uri.startswith(docs):
        short = uri[len(docs):]
        #print 'short:', short
        if short in files:
            # we can do something with these
            if anchor:
                new_uri = anchor
            else:
                new_uri = '#' + fn_to_anchor(short)
            return '<a{before}href="{uri}"{after}>{msg}</a>'.format(
                        before = before,
                        uri = new_uri,
                        after = after,
                        msg = message
                    )

    # Doesn't go anywhere, just remove it
    print "removing: " + orig_uri
    return message

def fix_links(html):
    html = html.replace('"/resources/', '"https://www.studentrobotics.org/resources/')
    html = html.replace('"/images/', '"./images/')

    linkish = re.compile('<a([^>]+)href="([^"]+)"([^>]*)>((<code>)?[^<]+(</code>)?)</a>')
    html = linkish.sub(fix_links_helper, html)

    return html

if __name__ == '__main__':
    blddir = '.bld'

    html_files = []
    for fn in files:
        html_fn = os.path.join(blddir, fn + ".html")
        ensure_dir(os.path.dirname(html_fn))
        fp = os.path.join(DOCS_ROOT, fn)
        pandoc(fp, '-o', html_fn \
              ,'--filter', './noCommentFilter.py' \
               ,'-f', 'markdown+pipe_tables+raw_html+fenced_code_blocks+header_attributes' \
              )
        html_files.append((fn, html_fn))

    all_html = ''
    for fn, html_fn in html_files:
        all_html += "\n@@{0}\n".format(fn_to_anchor(fn))
        with open(html_fn, 'r') as f:
            all_html += f.read()

    all_html = fix_links(all_html)

    all_fn = os.path.join(blddir, 'all.html')
    with open(all_fn, 'w') as f:
        f.write(all_html)

    pandoc(all_fn, '-o', 'smallpiece_docs.pdf' \
          ,'-V', 'geometry:margin=1.3in' \
          ,'--filter', './atLabelfilter.py' \
          ,'--latex-engine=xelatex' \
          ,'--toc', '--toc-depth=2' \
          )

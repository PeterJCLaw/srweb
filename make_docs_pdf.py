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
import subprocess

def pandoc(*args):
    args = list(args)
    args.insert(0, 'pandoc')
    subprocess.check_call(args)

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

if __name__ == '__main__':
    blddir = '.bld'

    html_files = []
    for fn in files:
        html_fn = os.path.join(blddir, fn + ".html")
        ensure_dir(os.path.dirname(html_fn))
        fn = os.path.join(DOCS_ROOT, fn)
        pandoc(fn, '-o', html_fn \
              ,'--filter', './noCommentFilter.py' \
               ,'-f', 'markdown+pipe_tables+raw_html+fenced_code_blocks+header_attributes' \
              )
        html_files.append(html_fn)

    all_html = ''
    for fn in html_files:
        with open(fn, 'r') as f:
            all_html += f.read()

    all_html = all_html.replace('/images/', '/home/peter/public_html/sr/srweb/images/')

    all_fn = os.path.join(blddir, 'all.html')
    with open(all_fn, 'w') as f:
        f.write(all_html)

    pandoc(all_fn, '-o', 'smallpiece_docs.pdf' \
          ,'-V', 'geometry:margin=1.3in' \
          ,'--latex-engine=xelatex' \
          ,'--toc', '--toc-depth=2' \
          )

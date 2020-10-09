#!/usr/bin/env python3

import sys
import re
import os

import json

def split_externals(work_dir, line) :
    url = ''
    rev = ''
    ext_dir = ''

    pattern = '({0})([^\s]+?)(@(\d+))?\s+([^\s]+)'.format(work_dir)
    m = re.search(pattern, line)
    if m :
        url = m.group(2)
        rev = m.group(4)
        ext_dir = m.group(5)
        #print('{0}, {1}, {2}'.format(url, rev, ext_dir))

    return url, rev, ext_dir

def main() :
    work_dir = ''

    items = []

    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        
        line = re.sub(r'\r?\n?$', '', line)

        if line == '' :
            continue

        m = re.search(r'^# (.*/)$', line)
        if m :
            work_dir = m.group(1)
            continue

        url, rev, ext_dir = split_externals(work_dir, line)

        if url != '' and ext_dir != '':
            ext_dir = '.' + work_dir + ext_dir
            ext_dir = re.sub(r'^\./', '', ext_dir)

            tmp = "." + work_dir
            tmp = re.sub(r'/$', '', tmp)

            item = {
                'cwd' : tmp,
                'url' : url,
                'rev' : rev,
                'ext_dir' : ext_dir
            }

            items.append(item)

    records = {
        "externals" : items
    }

    print(
        json.dumps(
            records,
            sort_keys=True,
            ensure_ascii=False,
            indent='\t'
        )
    )

if __name__ == "__main__" :
    main()


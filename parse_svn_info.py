#!/usr/bin/env python3

import sys
import re
import os

import json

def main() :
    items = {}

    while 1:
        line = sys.stdin.readline()
        if not line:
            break

        m = re.search(r'^([^:]+): (.+)', line)
        if m :
            key = m.group(1)
            val = m.group(2)
            key = key.replace(' ', '_')
            items[key] = val

    records = {
        "svn_info" : items
    }

    print(
        json.dumps(
            records,
            ensure_ascii=False,
            sort_keys=True,
            indent='\t'
        )
    )
if __name__ == "__main__" :
    main()


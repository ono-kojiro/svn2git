#!/usr/bin/env python3

import re

import subprocess

def get_command_output(cmd) :
    proc = subprocess.Popen(
        cmd,
        shell=True,
        encoding='utf-8',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    while True:
        line = proc.stdout.readline()
        if line :
            line = re.sub(r'\r?\n?', '', line)
            yield line

        if not line and proc.poll() is not None:
            break

def main() :
    cmd = 'git svn show-externals'

    for line in get_command_output(cmd):
        print("'" + line + "'")

if __name__ == "__main__" :
    main()


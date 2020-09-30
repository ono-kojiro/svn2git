#!/usr/bin/env python3

import re
import sys
import os

import getopt

import subprocess

def get_command_output(cmd) :
    count = 0

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

        if proc.poll() is not None:
            count += 1

        if not line and (count > 5) :
            break


def git_svn_show_revision(ext_dir) :
    rev = -1

    cmd = 'git -C {0} log -z -1'.format(ext_dir)

    #print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        #print('OUT : {0}'.format(line))
        m = re.search(r'\s*git-svn-id: ([^\s]+?)(@(\d+))?\s+(.+)$', line)
        if m :
            url = m.group(1)
            rev = int(m.group(3))
            id  = m.group(4)
    
    return rev
    
def main() :
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    output = None
    
    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"
    
    #if output == None :
    #    print "no output option"
    #    ret += 1
    
    if ret != 0:
        sys.exit(1)

    # fp = open(output, mode='w', encoding='utf-8')

    for arg in args :
        rev = git_svn_show_revision(arg)
        if rev < 0 :
            print("git_svn_show_revision failed")
        else :
            print("  {0} : revision {1}".format(arg, rev))
    
    #fp.close()

if __name__ == "__main__" :
    main()


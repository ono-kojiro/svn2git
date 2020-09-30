#!/usr/bin/env python3

import re

import sys
import os
import pathlib

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
            count = 0
            yield line

        if proc.poll() is not None :
            count += 1

        if not line and count > 5 :
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
    
def split_externals(work_dir, line) :
    url = ''
    rev = ''
    ext_dir = ''

    pattern = '({0})([^\s]+?)(@(\d+))?\s+([^\s]+)'.format(work_dir)
    m = re.search(pattern, line)
    if m :
        url = m.group(2)
        rev = int(m.group(4))
        ext_dir = m.group(5)
        print('{0}, {1}, {2}'.format(url, rev, ext_dir))

    return url, rev, ext_dir

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

    #fp = open(output, mode='w', encoding='utf-8')

    for target_dir in args :
        cwd = os.getcwd()

        os.chdir(target_dir)

        cmd = 'git svn show-externals'

        for line in get_command_output(cmd):
            #print("LINE : '{0}'".format(line))
        
            if line == '' :
                continue

            m = re.search(r'^# (.*/)$', line)
            if m :
                work_dir = m.group(1)
                continue

            url, rev, ext_dir = split_externals(work_dir, line)
        
            if url != '' and ext_dir != '':
                ext_dir = '.' + work_dir + ext_dir
                #print('{0}, {1}, {2}'.format(url, rev, ext_dir))

                got_rev = git_svn_show_revision(ext_dir)
                #print('type of got_rev : {0}'.format(type(got_rev)))
                #print('type of rev     : {0}'.format(type(rev)))

                if rev == got_rev :
                    print('revision OK')
                else :
                    print('revision NOT MATCH')
                    print("  expected : '{0}'".format(rev))
                    print("  got      : '{0}'".format(got_rev))
        
        os.chdir(cwd)


    
    #fp.close()

if __name__ == "__main__" :
    main()


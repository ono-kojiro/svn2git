#!/usr/bin/env python3

import re

import os
import pathlib

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

def init_git_svn(url, ext_dir) :
    cmd = 'git -C {0} init'.format(ext_dir, url)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)

    cmd = 'git -C {0} svn init --prefix=svn/ {1}'.format(ext_dir, url)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)
    
    cmd = 'git -C {0} svn fetch'.format(ext_dir)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)

def checkout_git(url, ext_dir) :
    print('{0}, {1}'.format(url, ext_dir))
    if not os.path.isdir(ext_dir) :
        print("INFO : no such working directory, '{0}'".format(ext_dir))
        if ext_dir != '.' and not os.path.isdir(ext_dir) :
            print("'make ext_dir, {0}'".format(ext_dir))
            os.makedirs(ext_dir)

        init_git_svn(url, ext_dir)

    else :
        print('directory exists, {0}'.format(ext_dir))

    pass

def main() :
    cmd = 'git svn show-externals'

    for line in get_command_output(cmd):
        if line == '' :
            continue

        m = re.search(r'^# (.*/)$', line)
        if m :
            continue

        m = re.search(r'([^\s]+)\s+(.+)', line)
        if m :
            ext_dir = '.' + m.group(1)
            url = m.group(2)
            
            cmd = 'git -C {0} svn rebase'.format(ext_dir)
            print('{0}'.format(cmd))
            subprocess.run(cmd, shell=True, encoding='utf-8')
        
if __name__ == "__main__" :
    main()


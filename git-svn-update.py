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

def init_git_svn(url, rev, ext_dir) :
    cmd = 'git -C {0} init'.format(ext_dir, url)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)

    cmd = 'git -C {0} svn init --prefix=svn/ {1}'.format(ext_dir, url)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)
    
    #cmd = 'git -C {0} svn fetch --revision {1}'.format(ext_dir, rev)
    #print('CMD : {0}'.format(cmd))
    #for line in get_command_output(cmd) :
    #    print(line)

def checkout_git(url, rev, ext_dir) :
    print('CHECKOUT_GIT : {0}, {1}'.format(url, ext_dir))
    if not os.path.isdir(ext_dir) :
        if ext_dir != '.' and not os.path.isdir(ext_dir) :
            os.makedirs(ext_dir)
        print('INFO : initialize git repository, {0}, {1}'.format(ext_dir, url))
        init_git_svn(url, rev, ext_dir)

    else :
        print('directory exists, {0}'.format(ext_dir))

    pass

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
        print('{0}, {1}, {2}'.format(url, rev, ext_dir))

    return url, rev, ext_dir

def main() :
    git_exclude = '.git/info/exclude'
    fp = open(git_exclude, mode='a', encoding='utf-8')

    work_dir = ''

    cmd = 'git svn show-externals'

    items = []

    for line in get_command_output(cmd):
        print("LINE : '{0}'".format(line))
        if line == '' :
            continue

        m = re.search(r'^# (.*/)$', line)
        if m :
            work_dir = m.group(1)
            continue

        url, rev, ext_dir = split_externals(work_dir, line)

        
        if url != '' and ext_dir != '':
            ext_dir = '.' + work_dir + ext_dir
            
            fp.write('{0}\n'.format(ext_dir))

            item = {
                'url' : url,
                'rev' : rev,
                'ext_dir' : ext_dir
            }

            items.append(item)

    for item in items :
        url = item['url']
        rev = item['rev']
        ext_dir = item['ext_dir']

        checkout_git(url, rev, ext_dir)

        #cmd = 'git -C {0} svn rebase'.format(ext_dir)
        #print('{0}'.format(cmd))
        #subprocess.run(cmd, shell=True, encoding='utf-8')
    
    fp.close()

if __name__ == "__main__" :
    main()


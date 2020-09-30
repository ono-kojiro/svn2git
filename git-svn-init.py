#!/usr/bin/env python3

import re

import os
import pathlib

import subprocess

#import pygit2

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

def git_init(ext_dir) :

    cmd = 'git -C {0} init'.format(ext_dir)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)

def git_svn_init(url, ext_dir) :
    
    cmd = 'git -C {0} svn init --prefix=svn/ {1}'.format(ext_dir, url)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)

def git_svn_fetch(rev, ext_dir) :
    
    cmd = 'git -C {0} svn fetch --revision {1}'.format(ext_dir, rev)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)


def init_git_svn(url, rev, ext_dir) :

    git_init(ext_dir)

    git_svn_init(url, ext_dir)

    git_svn_fetch(rev, ext_dir)

def git_config_get_regex(ext_dir) :
    cmd = 'git -C {0} config --get-regex svn-remote'.format(ext_dir)
    print('CMD : {0}'.format(cmd))

    configs = {}
    for line in get_command_output(cmd) :
        print(line)
        tokens = re.split(r'[\s+]', line)
        if len(tokens) == 2 :
            key = tokens[0]
            val = tokens[1]
            configs[key] = val

    return configs
    
def checkout_git(url, rev, ext_dir) :
    print('CHECKOUT_GIT : {0}, {1}'.format(url, ext_dir))
    if not os.path.isdir(ext_dir) :
        if ext_dir != '.' and not os.path.isdir(ext_dir) :
            os.makedirs(ext_dir)
        print('INFO : initialize git repository, {0}, {1}'.format(ext_dir, url))
        init_git_svn(url, rev, ext_dir)

    else :
        print("directory '{0}' already exists".format(ext_dir))
        configs = git_config_get_regex(ext_dir)
        for key in configs :
            val = configs[key]
            print('  {0} => {1}'.format(key, val))

        svn_remote_svn_url = configs['svn-remote.svn.url']
        if url == svn_remote_svn_url :
            print('  url OK')
        else :
            print('  url NG')
            print('  expected : {0}'.format(url))
            print('  got      : {0}'.format(svn_remote_svn_url))

            print('INFO : git svn init, {0}, {1}'.format(ext_dir, url))
            git_svn_init(url, ext_dir)
            git_svn_fetch(rev, ext_dir)
            init_git_svn(url, rev, ext_dir)
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


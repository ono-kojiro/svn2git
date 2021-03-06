#!/usr/bin/env python3

import sys

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

    cmd = 'git -C {0} commit '.format(ext_dir) + \
        '--allow-empty ' \
        '-m "first commit"'.format(ext_dir)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)

def git_svn_info(target_dir) :
    items = {}

    cmd = 'git -C {0} svn info'.format(target_dir)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)
        m = re.search(r'^([^:]+): (.+)', line)
        if m :
            key = m.group(1)
            val = m.group(2)
            key = key.replace(' ', '_')
            items[key] = val

    return items

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

def get_repos_root_url(url) :
    cmd = 'LANG=C svn info --show-item ' \
        'repos-root-url {0'.format(url)

    res = ''

    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        res = line

    return res

def get_relative_url(url) :
    cmd = 'LANG=C svn info --show-item ' \
        'relative-url {0'.format(url)

    res = ''

    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        res = re.sub(r'^\^/', '', line)

    return res
    
def git_svn_info(url) :
    url = ''
    repos_root_url = ''

    cmd = 'LANG=C svn git -C {0} svn info'.format(ext_dir)
    print('CMD : {0}'.format(cmd))
    for line in get_command_output(cmd) :
        print(line)
        m = re.search(r'^URL : (.+)', line)
        if m :
            url = m.group(1)

        m = re.search(r'^Repository Root: (.+)', line)
        if m :
            repos_root_url = m.group(1)

    relative_url = url.replace(repos_root_url, '')
    relative_url = re.sub(r'/$', '', relative_url)

    return repos_root_url, relative_url

def update_git_svn_config(repos_root_url, relative_url) :
    cmd = \
        'git config svn-remote.svn.url {0}'.format(repos_root_url)
    for line in get_command_output(cmd) :
        print(line)

    cmd = \
        'git config svn-remote.svn.fetch ' \
        '{0}:refs/remotes/svn/trunk'.format(relative_url)
    for line in get_command_output(cmd) :
        print(line)

def init_git_svn(url, rev, ext_dir) :

    git_init(ext_dir)
    
    relative_url = get_relative_url(url)
    repos_root_url = get_repos_root_url(url)

    git_svn_init(url, ext_dir)


    update_git_svn_config(repos_root_url, relative_url)

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

def extract_schema(url) :
    schema = ''

    m = re.search(r'^([^:]+:)//', url)
    if m :
        schema = m.group(1)

    return schema

def extract_schema_and_hostname(url) :
    schema_host = ''
    
    m = re.search(r'^([^:]+:///?([^/]+))/', url)
    if m :
        schema_host = m.group(1)

    return schema_host

def update_url(url, infos) :
    repository_root = infos['Repository_Root']

    while 1:
        m = re.search(r'^//', url)
        if m :
            # copy schema from repository root
            schema = extract_schema(url)
            url = schema + url
            break

        m = re.search(r'^\^/', url)
        if m :
            # relative path to repository root
            url = re.sub(r'^\^', '', url)
            url = infos['URL'] + url
            break

        m = re.search(r'^/[^/]', url)
        if m :
            # copy schema and hostname
            schema_host = extract_schema_and_hostname(infos['URL'])
            url = schema_host + url
            break
        
        m = re.search(r'^\.\./', url)
        if m :
            # relative path to parent directory
            url = infos['URL'] + '/' + url
            #print('not supported yet')
            #sys.exit(1)


        print('invalid external url, "{0}"'.format(url))
        sys.exit(1)
        
    return url
        

def main() :
    git_exclude = '.git/info/exclude'
    fp = open(git_exclude, mode='a', encoding='utf-8')

    target_dir = '.'

    infos = {}


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

    
        infos = git_svn_info(work_dir)

        url, rev, ext_dir = split_externals(work_dir, line)

        url = update_url(url, infos)

        
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


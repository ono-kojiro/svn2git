#!/usr/bin/env python3

import sys
import getopt
import re

import os
import pathlib
import json

import subprocess

#import pygit2

def git_init(ext_dir) :

    cmd = 'git -C {0} init'.format(ext_dir)
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

def update_url(url, cwd, infos) :
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
            url = infos['URL'] + '/' + cwd + '/' + url

            # remove /./
            url = re.sub(r'/./', '/', url)

            # remove /xxx/../
            url = re.sub(r'/[^/]+/\.\./', '/', url)
            
            break

        print('invalid external url, "{0}"'.format(url))
        sys.exit(1)
        
    return url

def read_json(filepath) :
    with open(filepath, mode='r', encoding='utf-8') as fp :
        data = json.load(fp)

    return data

def main() :
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
    
    ret = 0
    
    if output == None :
        print("no output option")
        ret += 1
    
    if ret != 0:
        sys.exit(1)

    externals = []
    svn_info = {}

    for arg in args :
        data = read_json(arg)

        if 'externals' in data :
            externals = data['externals']
        elif 'svn_info' in data :
            svn_info = data['svn_info']

    if not 'URL' in svn_info :
        print('no URL information')
        ret += 1

    if len(externals) == 0 :
        print('no externals')
        ret += 1

    if ret :
        sys.exit(1)
    
    with open(output, mode='w', encoding='utf-8') as fp :
        for item in externals :
            cwd = item['cwd']
            ext_dir = item['ext_dir']
            rev = item['rev']
            url = item['url']

            print('update url, "{0}"'.format(url))
            url = update_url(url, cwd, svn_info)
            print('new url, "{0}"'.format(url)) 
            item['url'] = url

        fp.write(
            json.dumps(
                externals,
                ensure_ascii=False,
                sort_keys=True,
                indent='\t'
            )
        )

if __name__ == "__main__" :
    main()


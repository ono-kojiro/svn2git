#!/bin/sh

cwd=`pwd`
url=file://$cwd/svnrepo

cd git_work

git svn init --trunk=trunk --tags=tags --branches=branches $url
git svn fetch

cd ..


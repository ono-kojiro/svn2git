#!/bin/sh

cwd=`pwd`
url=file://$cwd/svnrepo

cd git_work

git checkout trunk
git svn info

git branch -a


cd ..


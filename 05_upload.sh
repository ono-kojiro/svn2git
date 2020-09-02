#!/bin/sh

cwd=`pwd`
url=file://$cwd/svnrepo

cd git_work

echo foo > foo.txt
git add foo.txt
git commit -m 'add foo.txt'
cd ..


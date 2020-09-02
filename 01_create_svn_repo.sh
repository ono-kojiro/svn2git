#!/bin/sh

cwd=`pwd`
url=file://$cwd/svnrepo

rm -rf svnrepo

svnadmin create svnrepo

svn mkdir $url/trunk $url/tags $url/branches -m "create standard layout" --parents

svn ls $url

rm -rf svn_work

svn co $url/trunk svn_work

cd svn_work
echo hello > test.txt
svn add test.txt
svn commit -m "add test.txt"

echo hoge > hoge.txt
svn add hoge.txt
svn commit -m "add hoge.txt"

cd ..





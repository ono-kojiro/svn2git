#!/bin/sh

cwd=`pwd`
url=file://$cwd/svnrepo

cd svn_work
svn update
cd ..


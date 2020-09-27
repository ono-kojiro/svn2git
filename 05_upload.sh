#!/bin/sh

set -e

source ./config.bashrc

pushd svn2git

git checkout svn/trunk

cat - << 'EOS' >> main.c

int git_func()
{
	return 0;
}

EOS

git add main.c
git commit -m '[git] add git_func'

git push origin svn/trunk
git svn dcommit
popd

pushd svn_work
svn update
popd



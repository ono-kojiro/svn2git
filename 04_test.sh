#!/bin/sh

set -e

echo $0

source ./config.bashrc

### update svn
echo update svn and commit
pushd svn_work

echo "#include <stdio.h>" > main.c
svn commit -m "[svn] add include in main.c"

popd

echo git svn rebase
pushd svn2git
git svn rebase
popd


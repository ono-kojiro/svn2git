#!/bin/sh

set -e

source ./config.bashrc

pushd svn2git

git checkout svn/trunk

echo "int main()" >> main.c
echo "{" >> main.c
echo "}" >> main.c

git add main.c
git commit -m '[git] add main function'

git push origin svn/trunk
git svn dcommit
popd

pushd svn_work
svn update
popd



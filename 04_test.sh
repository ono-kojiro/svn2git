#!/bin/sh

set -e

source ./config.bashrc

cd git_work

git checkout svn/trunk
# git switch -c svn/trunk

git svn info
git branch -a

cd ..


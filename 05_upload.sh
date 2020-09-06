#!/bin/sh

set -e

source ./config.bashrc

cd git_work

git checkout svn/trunk

echo "This is commit from git" > foo.txt
git add foo.txt
git commit -m 'add foo.txt in git_work'

git push origin svn/trunk
git svn dcommit

cd ..


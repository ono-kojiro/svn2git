#!/bin/sh

set -e

source ./config.bashrc

rm -rf gitrepo.git

git init --bare --shared gitrepo.git

rm -rf git_work
git clone $git_url git_work

cd git_work
echo hello > hello.txt
git add hello.txt
git commit -m "add hello.txt in git_work"
git push origin master
cd ..


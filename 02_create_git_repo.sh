#!/bin/sh

cwd=`pwd`
url=file://$cwd/gitrepo.git

rm -rf gitrepo.git

git init --bare --shared gitrepo.git

rm -rf git_work
git clone $url git_work

cd git_work
echo hello > hello.txt
git add hello.txt
git commit -m test
git push origin master
cd ..


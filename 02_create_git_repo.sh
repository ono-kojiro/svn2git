#!/bin/sh

set -e

source ./config.bashrc

rm -rf $repo_git

git init --bare --shared $repo_git

rm -rf git_work
git clone $git_url git_work

cd git_work
echo hello > hello.txt
git add hello.txt
git commit -m "add hello.txt in git_work"
git push origin master

mkdir app
touch app/main.c
git add app/main.c
git commit -m "[git] add app/main.c"
git push origin master

cd ..


### svn2git
rm -rf $repo_svn2git
rm -rf svn2git

git init --bare --shared $repo_svn2git
git clone $svn2git_url svn2git

pushd svn2git
echo This is README > README.txt
git add README.txt
git commit -m "[git] add README.txt"
git push origin master

git branch develop
git checkout develop
mkdir app
touch app/main.c
git add app/main.c
git commit -m "[git] add app/main.c"
git push origin develop

git checkout master

popd



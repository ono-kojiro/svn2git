#!/bin/sh

pushd svn2git
git checkout develop

git branch tmp
git checkout tmp

git filter-branch --subdirectory-filter app HEAD

git commit -m '[git] subdirectory-filter of develop branch'

git checkout svn-trunk
git clean -fdx
git merge -X theirs \
	--allow-unrelated-histories -m 'merge develop branch' tmp

git branch -D tmp

popd

pushd svn_work
svn update
popd




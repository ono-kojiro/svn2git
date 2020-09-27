#!/bin/sh

source ./config.bashrc

pushd svn2git

#git remote add svn2git $svn2git_url
#git fetch svn2git

#git branch develop
git checkout develop

git merge \
	-X subtree=app \
	--allow-unrelated-histories \
	-m 'merge svn2git/svn/trunk' \
	svn/trunk

git push origin develop

popd


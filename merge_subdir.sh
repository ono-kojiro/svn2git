#!/bin/sh

src_branch=develop
src_dir=app

dst_branch=svn/trunk
dst_dir=.

tmp_branch=${src_branch}-${src_dir}

git checkout $src_branch

git branch $tmp_branch
git checkout $tmp_branch

git filter-branch --subdirectory-filter $src_dir HEAD
git commit -m 'subdirectory-filter $src_dir in $src_branch branch'

git checkout $dst_branch
git merge -X theirs \
	--allow-unrelated-histories -m 'merge $src_branch branch' $tmp_branch
git branch -D $tmp_branch


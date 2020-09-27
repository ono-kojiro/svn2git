#!/bin/sh

set -e

source ./config.bashrc


cd svn2git

git svn init \
	--trunk=common/workspace/build \
	--tags=tags \
	--branches=branches \
	--prefix=svn/ \
	$svn_url

git svn fetch

git checkout svn/trunk
git checkout -b svn-trunk

git gc --aggressive

git log

cd ..


#!/bin/sh

set -e

source ./config.bashrc


cd git_work

git svn init \
	--trunk=common/workspace \
	--tags=tags \
	--branches=branches \
	--prefix=svn/ \
	$svn_url

git svn fetch

cd ..


#!/bin/sh

set -e

rm -rf test

mkdir test

pushd test
git init

git svn init \
	--trunk=trunk \
	--tags=tags \
	--branches=branches \
	--prefix=svn/ \
	https://localhost/svn/svnparent

git svn fetch

popd


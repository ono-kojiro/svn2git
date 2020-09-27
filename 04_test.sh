#!/bin/sh

set -e

echo $0

source ./config.bashrc

### update svn
echo update svn and commit
pushd svn_work

cat - << 'EOS' >> main.c
int hoge()
{
	printf("hoge\n");
	return 0;
}

EOS

svn commit -m "[svn] add function hoge() in main.c"

popd

echo git svn rebase
pushd svn2git
git svn rebase
popd


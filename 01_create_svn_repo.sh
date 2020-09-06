#!/bin/sh

set -e

source ./config.bashrc

rm -rf svnrepo

echo create repository
svnadmin create svnrepo

echo create standard layout in repository
svn mkdir \
	$svn_url/trunk \
	$svn_url/tags \
	$svn_url/branches \
	-m "create standard layout" --parents

echo create common directory
svn mkdir $svn_url/common -m "create common directory" --parents

svn ls $svn_url

echo checkout trunk as 'svn_work'
rm -rf svn_work
svn co $svn_url/trunk svn_work

cd svn_work

echo add main.c in svn trunk
cat - << 'EOS' > main.c
#include <stdio.h>

int main(int argc, char **argv)
{
	printf("Hello World\n");
	return 0;
}

EOS

svn add main.c
svn commit -m "add main.c in svn_work"

cat - << 'EOS' > test.c
#include <stdio.h>

int test(void)
{
	printf("This is test\n");
	return 0;
}
EOS

echo add test.c in svn trunk
svn add test.c
svn commit -m "add test.c in svn_work"

svn copy -m "copy from trunk to branches/v0.0.1" . $svn_url/branches/v0.0.1
svn switch $svn_url/branches/v0.0.1
svn update

cat - << 'EOS' > version.h
#define VERSION 0.0.1
EOS

svn add version.h
svn commit -m "add version.h in branch v0.0.1"
svn update

svn switch $svn_url/trunk
svn update

svn copy -m "copy from trunk to common/workspace" . $svn_url/common/workspace

svn switch $svn_url/common/workspace
echo workspace > workspace.txt
svn add workspace.txt
svn commit -m "add workspace.txt in svn_work"

cd ..





#!/bin/sh

set -e

source ./config.bashrc

cd svn_work
svn update
grep "This is commit from git" foo.txt
if [ "$?" = "0" ]; then
	echo commit of git found in svn		
else
	echo commit of git NOT found in svn
fi

cd ..


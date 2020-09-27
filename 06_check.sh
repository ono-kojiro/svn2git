#!/bin/sh

#set -e

source ./config.bashrc

echo start

pushd svn_work
echo svn update
svn update

echo svn log
svn log | grep '\[git\] add main function'

if [ "$?" = "0" ]; then
	echo OK : commit of git found in svn		
else
	echo NG : commit of git NOT found in svn
fi

popd


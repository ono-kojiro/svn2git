#!/bin/sh

echo This is $0

pushd svn2git

git checkout -f develop

echo update comment

sed -i.bak \
	's|COMMENT 1 |[git] update comment in app/main.c |' \
	app/main.c > app/main.c
git add -u
git commit -m '[git] add comment in app dir'
git push origin develop

popd


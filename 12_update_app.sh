#!/bin/sh

echo This is $0

pushd svn2git

git checkout -f develop

echo update comment


cat app/main.c | \
	sed 's/comment 1 /comment A /' \
	> tmp.c
cp -f tmp.c app/main.c
git add -u
git commit -m '[git] update comment in app dir'
git push origin develop

popd



all :

init :
	sh 00-prepare.sh

test :
	#cd test && python3 ../git-svn-get-externals.py
	cd test && python3 ../git-svn-init.py

clean :
	rm -rf test

.PHONY : \
	all clean init test


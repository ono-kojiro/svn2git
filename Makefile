
all :
	sh 00-prepare.sh
	cd test && python3 ../git-svn-get-externals.py

clean :
	rm -rf test


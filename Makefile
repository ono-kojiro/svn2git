
all :
	$(MAKE) clean init
	cd test && python3 ../git-svn-get-externals.py

init :
	sh 00-prepare.sh

clean :
	rm -rf test


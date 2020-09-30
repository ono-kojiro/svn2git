all :

init :
	sh 00-prepare.sh

ext : git-svn-init

git-svn-init :
	#cd test && python3 ../git-svn-get-externals.py
	cd test && python3 ../git-svn-init.py

config :
	cd test && autoreconf -vi && sh configure 

build :
	cd test && $(MAKE)

check :
	cd test && $(MAKE) check

git-svn-fetch :
	python3 git-svn-fetch.py test/

check-revision :
	python3 git-svn-check-revision.py test/

clean :
	rm -rf test

.PHONY : \
	all clean init test


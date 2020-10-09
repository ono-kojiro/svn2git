GIT_WORK = test

all :

init :
	sh 00-prepare.sh

ext :
	#cd test && python3 ../git-svn-get-externals.py
	git -C $(GIT_WORK) svn show-externals > externals.txt
	cat externals.txt

	git -C $(GIT_WORK) svn info > svn_info.txt
	cat svn_info.txt

	cat svn_info.txt  | python3 parse_svn_info.py  > svn_info.json
	cat svn_info.json

	cat externals.txt | python3 parse_externals.py > externals.json
	cat externals.json

test :
	python3 update_externals.py -o new_externals.json externals.json svn_info.json

	#cd test && python3 ../git-svn-init.py

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


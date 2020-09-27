

all :
	sh 01_create_svn_repo.sh
	sh 02_create_git_repo.sh
	sh 03_sync.sh
	sh 04_test.sh
	sh 05_upload.sh
	sh 06_check.sh

clean :
	rm -rf $repo_git
	rm -rf $svnrepo
	rm -rf git_work
	rm -rf svn_work


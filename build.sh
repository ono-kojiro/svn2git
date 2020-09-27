#!/bin/sh

source ./config.bashrc

usage()
{
	echo "usage : $0 [options] target1 target2 ..."
	exit 0
}

all()
{
	sh 01_create_svn_repo.sh
	sh 02_create_git_repo.sh
	sh 03_sync.sh
	sh 04_test.sh
	sh 05_upload.sh
	sh 06_check.sh

	sh 11_merge_to_dir.sh
	#sh 12_update_app.sh
	#sh 13_merge_app_to_top.sh

}

clean()
{
	rm -rf $repo_svn
	rm -rf $repo_git
	rm -rf $repo_svn2git

	rm -rf svn_work
	rm -rf git_work
	rm -rf svn2git
}


logfile=""

while getopts hvl: option
do
	case "$option" in
		h)
			usage;;
		v)
			verbose=1;;
		l)
			logfile=$OPTARG;;
		*)
			echo unknown option "$option";;
	esac
done

shift $(($OPTIND-1))

if [ "x$logfile" != "x" ]; then
	echo logfile is $logfile
fi

for target in "$@" ; do
	echo target is "$target"
	type -t $target
	res=`type -t $target | grep function`
	if [ "$res" = "function" ]; then
		echo $target is function
		$target
	else
		echo $target is not function
	fi
done


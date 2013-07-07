#!/bin/bash

if [ ! "$#" -eq 2 ] || [ "$#" -eq 3 ] && [ "$1" != "-f" ]
then
	echo "usage: $0 [-f] \"url\" \"title\""
	echo "e: i nazisti farebbero meglio a non codare in bash"
	exit 0
fi


curdir=`basename $(pwd)`
if [ "$curdir" != "mi.perpli.me" ]
then
    pushd mi.perpli.me > /dev/null
fi

source bin/activate
if [ $1 == "-f" ]
then
    python perplime.py -u "$2" -t "$3" -f
    ret=$?
else
    python perplime.py -u "$1" -t "$2"
    ret=$?
fi

if [ $ret -eq 0 ]
then
    make html
fi 
deactivate

# let's build a list of this shit for backup reasons
echo $@ >> $HOME/.images_backup

popd > /dev/null 2>&1

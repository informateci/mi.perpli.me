#!/bin/bash

DIALOGS="dialog xdialog gdialog zenity"
DIAG_OPTS="--backtitle \"mi.perpli.me Poor Admin Tool\""
TMP=/tmp

VIEWSCR=$TMP/viewscr
ITEMSCR=$TMP/itemscr

for diag in $DIALOGS; do
    DIALOG=$(which $diag)
    [ "$DIALOG" != "" ] && break
done

[ "$DIALOG" == "" ] && echo "You need some sort of dialog to use this program." && exit 0

echo "Collecting data on Articles..."

sorted=$(
    for i in $(find content -iname '*md' ); do 
        echo  "$i \"$(egrep "^Date" $i | sed -e 's/^[^:]*: //') $(egrep "^Title" $i | sed -e 's/^[^:]*: //')\" "; 
    done  | sort -r -k 2
    )

[ "$sorted" == "" ] && "No articles found. Wtf." && exit 0

mainret=0
edit=0

while [ $mainret = 0 ]; do
    echo $DIALOG $DIAG_OPTS --cancel-label "Exit" --ok-label "Edit" --no-tags --menu \"Select an Article\" 25 80 30  $sorted 2\> $TMP/result > $VIEWSCR
    
    . $VIEWSCR
    
    mainret=$?
    if [ $mainret = 0 ]; then
        item=`cat $TMP/result`
        echo $DIALOG $DIAG_OPTS --menu $item 25 80 30 \
            rename \"New title for the article\" \
            edit \"Modify the source\" \
            delete \"Erase the Article \(wow much pain\)\" \
            2\> $TMP/result > $ITEMSCR
        . $ITEMSCR
        case `cat $TMP/result` in
            "rename")
                oldtitle="$(egrep '^Title: ' $item | sed -e 's/^[^:]*: //')"
                $DIALOG --inputbox "Rename the Article $item"  25 80 "$oldtitle" 2> $TMP/result
                if [ $? = 0 ]; then
                    newtitle=`cat $TMP/result | tr '[:lower:]' '[:upper:]'`
                    sed -i -e "s/^Title: .*/Title: $newtitle/" $item
                    edit=1
                fi
                ;;
            "edit")
                $DIALOG --editbox $item 25 80 2> $TMP/newfile
                if [ $? = 0 ]; then
                    $DIALOG --yesno "Write your edits for $item?" 5 80 && cp $TMP/newfile $item && edit=1
                fi
                ;;
            "delete")
                $DIALOG --yesno "DELETE $item?\nTHE ENTRY AND ALL RELATED RESOURCES WILL BE DELETED" 10 80
                if [ $? = 0 ]; then
                    hsh=$( echo $item | sed -e 's/.*\///; s/.md//' )
                    find content -name "$hsh*" -delete
                    edit=1
                fi
                ;;
        esac
    fi
done

if [ $edit = 1 ]; then
    $DIALOG --yesno "Regenerate the site after all this mess?" 5 80
    
    if [ $? = 0 ]; then
        source bin/activate
        make html
        deactivate
    fi
fi

rm $VIEWSCR
rm $ITEMSCR
rm $TMP/result

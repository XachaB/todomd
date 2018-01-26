#!/bin/bash
source todoconfig.py
OUTPUT=$(zenity --forms  --text "Add to TODO list" --add-list "List" --list-values "$(find $todofolder*.md ! -name TODO.md -printf "%f|" | sed "s/|$//g")" --add-entry "Item:" --separator="")

if [[ $OUTPUT ]]; then
    DATE_INPUT=$(zenity --calendar --text "Select the due date (cancel to add no date)")
    if [[ $DATE_INPUT ]]; then
       DATE=" @date($DATE_INPUT)"
    else
       DATE=""
    fi


    FILE=$(awk -F, '{print $1}' <<<$OUTPUT)
    TEXT=$(awk -F, '{print $2}' <<<$OUTPUT)
    ITEM="# [TODO] $TEXT$DATE"

    echo -e "$ITEM\n$(cat $todofolder$FILE)" > $todofolder$FILE

    python3 gather_todo.py

    notify-send  -i checkbox "Added to $FILE" "$ITEM"
fi
#zenity --notification --text="Added  --window-icon=/usr/share/icons/elementary-xfce/apps/128/checkbox.png

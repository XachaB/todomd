#!/bin/bash
source todoconfig.py
python3 gather_todo.py
zenity --notification --text="$(head -n 10 $todolist | sed s/^*//g | sed s/[*#]//g)"

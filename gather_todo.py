from glob import glob
from os.path import basename, getmtime
import re
import datetime
import todoconfig

todo = re.compile(r"\[TODO\](.+)")
item_format = "* {}"
dated_item_format = "* [{}] [{}] {}"
dated_item_format_urgent = "* **[{}] [{}] {}**"
later_item_format = "* [{}] {}"
date = re.compile(r"(.+) @date\((.+)\)")

def to_date(string):
    if string is None:
        return ""
    else:
        return datetime.datetime.strptime(string, '%d/%m/%Y').date()

def parse_date(todo_item):
    match = date.search(todo_item)
    if match:
        return match.groups()
    else:
        return todo_item, None

def find_items(filename):
    with open(filename, "r", encoding="utf-8") as flow:
        for line in flow:
            match = todo.search(line.strip("\n"))
            if match:
                yield match.groups()[0]
dated_todo_list = []
later_todo_list = []
todo_list = []
today = datetime.datetime.today().date()
for filename in sorted(glob(todoconfig.todofolder+"*.md"), key=getmtime, reverse=True):
    try:
        items = list(find_items(filename))
        if items:
            title_added = False
            title = basename(filename)[:-3].replace("_"," ")
            for todo_item in items:
                todo_item, due_date_str = parse_date(todo_item.strip())
                if "[later]" in todo_item:
                    todo_item = re.sub("\[later\]","",todo_item).strip()
                    later_todo_list.append(later_item_format.format(title,todo_item))
                elif due_date_str is not None:
                    due_date = to_date(due_date_str)
                    item =  dated_item_format.format(due_date_str,title,todo_item)
                    if due_date <= today:
                        item = dated_item_format_urgent.format(due_date_str,title,todo_item)
                    dated_todo_list.append((due_date, item))
                else:
                    if not title_added:
                        todo_list.append("\n# "+title.capitalize())
                        title_added = True
                    todo_list.append(item_format.format(todo_item))
    except Exception as e:
        print("Exception Occured in file {}".format(filename))
        raise

dated_todo_list.sort(key=lambda x:x[0])
if dated_todo_list:
    todo_list = ["# With due date"] + [y for x,y in dated_todo_list] + todo_list

if later_todo_list:
    todo_list = todo_list + ["","# Tasks for later"] + later_todo_list


with open(todoconfig.todolist, "w", encoding="utf-8") as flow:
    flow.write("\n".join(todo_list))

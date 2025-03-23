import subprocess
import os
import sys
import funcs
import signal

def add():
    name = ''
    while name == '':
        name = input("Enter the name of script or 'r': ")
        if name == '':
            print("Please, enter the name or 'r'!")
        if name == 'r':
            print("return")
            return

    path = ''
    while path == '':
        path = input("Enter the path: ")
        if path == '':
            print("Please, enter the path!")
        else:
            if path[0] == '"':
                path = path[1:-1]
    
    question = ''
    while question != "Y" and question != "n":
        question = input("Do you need a venv?(Y/n): ")
        if question == "Y":
            start_by = ''
            while start_by == '':
                start_by = input("Enter the venv path: ")
                if start_by == '':
                    print("Please, enter the venv path!")
                else:
                    if start_by[0] == '"':
                        start_by = start_by[1:-1]
                        start_by = os.path.join(start_by, 'Scripts', 'python.exe')
        elif question == "n":
            start_by = funcs.get_start_by(path)
        else:
            print("Invalid syntax, please try again")
    funcs.add(name, path, start_by)
    print(f"{name} created successfully ")

def delete():
    name = input("Enter the name or 'r': ")
    if name == 'r':
            print("return")
            return
    if not name in funcs.get_scripts():
        print("There is no such name")
        return
    q = ''
    while q != 'Y' and q != 'n':
        q = input(f"are you sure to delete {name}?(Y/n): ")
        if q == 'Y':
            funcs.delete(name)
            print(f"{name} deleted successfully")
        elif q == 'n':
            return
        else:
            print("Invalid syntax, please try again")

def launch():
    name = input("Enter name or 'r': ")
    if name == 'r':
            print("return")
            return
    if not name in funcs.get_scripts():
        print("There is no such name")
        return

    script = funcs.get_script(name)
    activate = script[2] 
    script_path = script[1]

    subprocess.Popen([activate, script_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("opening..")

def close():
    name = input("Enter the name or 'r': ")
    if name == 'r':
            print("return")
            return
    if not name in funcs.get_scripts():
        print("There is no such name")
        return
    
    script = funcs.get_script(name)
    if script[2] == None:
        activate = 'python'
    else:
        activate = os.path.join(script[2], 'Scripts', 'python.exe')

    script_path = script[1]
    pid = funcs.get_pid_by_process_path(f"{activate} {script_path}")

    if pid == None:
        print(f"{name} is already closed")
        return
    
    os.kill(pid, signal.SIGINT)
    print(f"{name} closed successfilly")


info = """
list of commands:
add new proccess: add
delete procces from list: del
get list: get
launch procces: l
close procces: c
quit: q
return: r
"""

while True:
    to_do = input("What to do?: ")

    if to_do == 'a':
        add()
    elif to_do == 'd':
        delete()
    elif to_do == 'l':
        launch()
    elif to_do == 'g':
        for name in funcs.get_scripts():
            print(name)
    elif to_do == 'c':
        close()
    elif to_do == 'help':
        print(info)
    elif to_do == 'q':
        sys.exit()
    else:
        print("Invalid syntax, please try again (to get a list of commands: help)")
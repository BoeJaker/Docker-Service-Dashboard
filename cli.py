# Package Imports
import os
import subprocess
from simple_term_menu import TerminalMenu

# File Imports
from tmux_operations import *
from git_operations import *
from file_operations import *

# Globals
menu_entry_index = 0
exit = False


def file_routine():
    global exit
    exit = False
    list_files(root_dir)
    i = file_list
    while exit == False:
        i = file_menu_handler(i)

def github_routine():
    global exit
    exit = False
    git_projects = list_git_projects(root_dir)
    git_project = main_menu([g["directory"] for g in git_projects])
    github_menu_handler(git_project)
     

def osint_routine():
    pass

def ports_routine():
    pass

def backup_routine():
    pass

def capture_network():
    pass

def network_outage():
    pass

def wpa2_crack():
    pass

def clone_drive():
    pass

# Generic Menu Function
def main_menu(options=["entry 1", "entry 2", "entry 3"],operations=[]):
    os.system("clear")
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!\n")
    print()
    if len(operations) >= 1 :
        command = operations[menu_entry_index][0]
        args = operations[menu_entry_index][1]
        if len(args) > 0:
            return command(args)
        else:
            return command()
    return options[menu_entry_index]

# A Placholder Function
def do_nothing():
    pass

# Udates the exit status
def exit_menu():
    global exit
    exit = True

# File Menu    
def file_menu_handler(path):
    global file_list, menu_entry_index, exit
    if isinstance(path, list):
        menu_entry_index = main_menu(options=file_list)
    elif os.path.isfile(path):
        menu_entry_index = main_menu(
            options=[
                "Edit", 
                "Run", 
                "Back", 
                "Exit"
            ],
            operations=[
                [file_edit,[path]],
                [file_run,[path]],
                [list_files,[root_dir]],
                [exit_menu,[]]
            ]
        )            
    elif os.path.isdir(path):
        file_list = list_files(path)
        menu_entry_index = main_menu(file_list)
    return menu_entry_index

def github_menu_handler(directory):
    global exit
    menu_opt = main_menu(
        options=[
            "Pull", 
            "Add",
            "Commit",
            "Push", 
            "Rebase", 
            "Gist Create",
            "Gist Update",
            "Exit"
        ],
        operations=[
            git_pull,
            git_add,
            git_commit,
            git_push,
            do_nothing,
            gist_create,
            gist_update,
            exit_menu
        ]
    )

# Main Menu
def cli_menu():
    global exit
    while True:
        menu_opt = main_menu(
            options=[
                "Files", 
                "Github",
                "Ports", 
                "Backup", 
                "Monitor", 
                "OSINT", 
                "Exploit", 
                "Network Outage", 
                "Capture Mode", 
                "WPA2 Crack",
                "Clone Drive"
            ],
            operations=[
                [file_routine,[]],
                [github_routine,[]],
                [ports_routine,[]],
                [backup_routine,[]],
                [monitor,[]],
                [osint_routine,[]],
                [exploit,[]],
                [do_nothing,[]],
                [do_nothing,[]],
                [do_nothing,[]],
                [do_nothing,[]]
            ]
        )
        print(menu_opt)
        
if __name__ == "__main__":
    cli_menu()
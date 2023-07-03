import os
from vars import *
# File/Directory Enumerator
def list_files(directory=root_dir):
    global file_list
    print("loading...")
    for item in os.listdir(directory):
        file_list.append(os.path.join(directory, item))
    return(file_list)

def file_edit(path):
    os.system(f"nano '{str(path)}'")

def file_run(path):
    os.system(f"screen -S runner -dm bash -c '{str(path)}'")

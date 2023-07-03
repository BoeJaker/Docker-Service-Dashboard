import os, subprocess

def list_git_projects(directory):
    git_projects = []

    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            project_name = os.path.basename(root)
            git_projects.append({'name': project_name, 'directory': root})
            # Exclude subdirectories from further search
            dirs.remove('.git')

    return git_projects

def git_check_auth():
    try:
        # Execute 'git config user.name' to check if the user is logged in
        subprocess.check_output(['git', 'config', 'user.name'], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def git_auth():
    if git_check_auth():
        os.system("git credential fill")

def git_add(files="."):
    git_auth()
    os.system(f"git add {files}")

def git_commit(message):
    if not message:
        message = input("Enter the commit message")
    git_auth()
    os.system(f"git commit -m {message}")

def git_pull(url, folder=""):
    git_auth()
    os.system("git pull  {url} {folder}")

def git_push():
    git_auth()
    os.system("git push")

def git_first_push():
    git_auth()
    os.system("git push origin main")

def gist_check_auth():
    try:
        output = subprocess.check_output(['gh', 'auth', 'status']).decode('utf-8')
        return 'Logged in' in output
    except subprocess.CalledProcessError:
        return False

def gist_auth():
    if not gist_check_auth():
        os.system("gh auth login")

def gist_create(files=[]):
    gist_auth()
    os.system(f"gh gist create --public --files {files}")

def gist_update(gistid, files=[]):
    gist_auth()
    os.system(f"gh gist edit {gistid} --files {files}")
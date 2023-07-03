import os

def tmux_four_pane(operations=[]):
    # Split the terminal into four panes
    os.system("tmux new-session -d")
    os.system("tmux split-window -v")
    os.system("tmux split-window -h")
    os.system("tmux select-pane -t 0")
    os.system("tmux split-window -h")
    if len(operations):
        for index in range(0,3):
            os.system('tmux send-keys -t '+str(index)+' "'+operations[index]+'" Enter')
    # Switch focus to the fourth pane
    os.system("tmux select-pane -t 3")
    # Attach to the session
    os.system("tmux attach-session")

def monitor():
    tmux_four_pane(
        operations=[
            "htop",
            "iftop",
            "docker stats",
            "# Ctrl+B Arrow Key (Left, Right, Up, Down) — Move between panes. Ctrl+B X — Close pane. Ctrl+B C — Create a new window. Ctrl+B N or P — Move to the next or previous window"
        ]
    )

def exploit():
    tmux_four_pane(
        operations=[
            "msfconsole",
            "searchsploit",
            "python3 '/home/boejaker/BACKUPS/Legacy/MEGA T470s/Programming - Docker/Service_Dashboard_2/cli.py'",
            "# Ctrl+B Arrow Key (Left, Right, Up, Down) — Move between panes. Ctrl+B X — Close pane. Ctrl+B C — Create a new window. Ctrl+B N or P — Move to the next or previous window"
        ]
    )

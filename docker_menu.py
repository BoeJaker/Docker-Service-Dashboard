import os
import subprocess
from simple_term_menu import TerminalMenu
import libtmux

from docker_operations import *
from tmux_operations import *

# Init termux
server = libtmux.Server()
session = server.new_session()
window = session.attached_window


def display_menu(services):
    # Display the menu with available services
    menu_items = [service for service in services] + ["View Logs", "Exit"]
    menu = TerminalMenu(menu_entries=menu_items, title="Docker Compose Services")
    selected_index = menu.show()

    # Get the user's selection
    selection = menu_items[selected_index]
    return selection

def view_logs():
    # View logs of a container using tmux
    container_name = input("Enter the container name to view logs: ")
    session_name = f"{container_name}-logs"
    command = f"tmux new-session -A -s {session_name} ;\
                tmux split-window -v \
                'docker logs -f {container_name}' ;"
    tmux_generator([command,  "python3 '/home/boejaker/BACKUPS/Legacy/MEGA T470s/Programming - Docker/Service_Dashboard_2/docker_menu.py'",])


def docker_menu_loop():
    services = get_docker_compose_services()
    # services = get_container_list()
   
    # Display the initial menu
    selection = display_menu(services)
    while selection != "Exit":
        if selection == "View Logs":
            view_logs()
        else:
            if selection in subprocess.check_output("docker-compose ps --services", shell=True).decode("utf-8").split():
                print(f"The '{selection}' service is already running.")
                attached = input("Do you want to attach to it? (y/n): ").lower() == "y"
                if attached:
                    tmux_generator([attach_to_service(selection),  "python3 '/home/boejaker/BACKUPS/Legacy/MEGA T470s/Programming - Docker/Service_Dashboard_2/docker_menu.py'",])
            else:
                print(f"The '{selection}' service is not running.")
                run_detached = input("Do you want to run it in detached mode? (y/n): ").lower() == "y"
                run_service(selection, attached=not run_detached)

        # Display the menu again
        selection = display_menu(services)
    
    server.kill_server()

if __name__ == "__main__":
    docker_menu_loop()
import os
import subprocess
from simple_term_menu import TerminalMenu
from pathlib import Path
import yaml

def get_script_directory():
    # Get the directory where the script is being run from
    return os.getcwd()

def get_docker_compose_services():
    # Get the list of services from the Docker Compose file
    docker_compose_file = os.path.join(get_script_directory(), "docker-compose.yml")
    services = []
    with open(docker_compose_file, "r") as f:
        data = yaml.safe_load(f)
        if "services" in data:
            services = list(data["services"].keys())
    return services

def display_menu(services):
    # Display the menu with available services
    menu_items = [service for service in services] + ["View Logs", "Exit"]
    menu = TerminalMenu(menu_entries=menu_items, title="Docker Compose Services")
    selected_index = menu.show()

    # Get the user's selection
    selection = menu_items[selected_index]
    return selection

def run_service(service, attached=True):
    # Run the Docker Compose service
    if attached:
        command = f"docker-compose up {service}"
    else:
        command = f"docker-compose up -d {service}"
    subprocess.run(command, shell=True)

def stop_service(service):
    # Stop the Docker Compose service
    command = f"docker-compose stop {service}"
    subprocess.run(command, shell=True)

def attach_to_service(service):
    # Attach to the running Docker Compose service using tmux
    session_name = f"{service}-session"
    command = f"tmux new-session -A -s {session_name} docker-compose exec {service} bash"
    subprocess.run(command, shell=True)

def view_logs():
    # View logs of a container using tmux
    container_name = input("Enter the container name to view logs: ")
    session_name = f"{container_name}-logs"
    command = f"tmux new-session -A -s {session_name} 'docker logs -f {container_name}'"
    subprocess.run(command, shell=True)

def main():
    # Start the terminal interface within a tmux window
    tmux_session = "docker-menu"
    # subprocess.run(["tmux", "new-session", "-d", "-s", tmux_session])

    # Get the list of services from the Docker Compose file
    services = get_docker_compose_services()

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
                    attach_to_service(selection)
            else:
                print(f"The '{selection}' service is not running.")
                run_detached = input("Do you want to run it in detached mode? (y/n): ").lower() == "y"
                run_service(selection, attached=not run_detached)

        # Display the menu again
        selection = display_menu(services)

    # Stop the tmux session when the user selects "Exit"
    # subprocess.run(["tmux", "kill-session", "-t", tmux_session])

if __name__ == "__main__":
    main()
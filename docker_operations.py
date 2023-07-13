import docker
import subprocess
import yaml
import os

client = docker.from_env()

def get_docker_compose_services():
    # Get the list of services from the Docker Compose file
    docker_compose_file = os.path.join(os.getcwd(), "docker-compose.yml")
    services = []
    with open(docker_compose_file, "r") as f:
        data = yaml.safe_load(f)
        if "services" in data:
            services = list(data["services"].keys())
    return services

def get_container_list():
    containers = client.containers.list(all=True)
    return containers

def get_container(container_id):
    container = client.containers.get(container_id)
    return container

# Container Details
def get_container_details(container):
    cpu_total_usage = container.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']
    cpu_system_usage = container.stats(stream=False)['cpu_stats']['system_cpu_usage']
    cpu_percent = cpu_total_usage / cpu_system_usage * 100

    memory_usage = container.stats(stream=False)['memory_stats']['usage']
    memory_limit = container.stats(stream=False)['memory_stats']['limit']
    memory_percent = memory_usage / memory_limit * 100
    details = {
        'ID': container.id,
        'Name': container.name,
        'Stack Name': container.labels.get('com.docker.compose.project'),
        'Status': container.status,
        'Uptime': container.attrs['State']['StartedAt'],
        'CPU Usage': cpu_percent,
        'Memory Usage': memory_percent,
        'Ports': container.attrs['NetworkSettings']['Ports'],
        'Logs': container.logs().decode('utf-8'),
        'Volumes': container.attrs['Mounts'],
        'Configuration': container.attrs['Config'],
    }
    return details

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
    command = f"docker-compose exec {service} bash"
    return(command)

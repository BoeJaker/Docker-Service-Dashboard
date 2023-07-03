import docker

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

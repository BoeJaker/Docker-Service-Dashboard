import requests, json, time, nmap
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
# from simple_term_menu import TerminalMenu
from threading import Thread

# File Imports
from main_menu import *
from docker_operations import *
from docker_menu import *

app = Flask(__name__)

DEVICE_NAMES_FILE = "device_names.json"
device_names = {}

# Get host IP address dynamically
def get_host_ip():
    return request.host.split(':')[0]

# Home page
@app.route('/')
def home():
    containers = get_container_list()
    print(containers)
    host_ports = [container.attrs['HostConfig']['PortBindings'] for container in containers]
    print(host_ports)
    bookmarks = request.cookies.get('bookmarks', '').split(';')
    return render_template('index.html', containers=containers, host_ports=host_ports, bookmarks=bookmarks)

# Reverse Proxy
@app.route('/proxy/<port>')
def proxy(port):
    host_ip = "192.168.3.135"
    url = f'http://{host_ip}:{port}'
    response = requests.get(url, allow_redirects=True)
    headers = response.headers.items()
    return Response(response.content, content_type=response.headers['content-type'], headers=headers)

# Container details page
@app.route('/container/<container_id>')
def container_details(container_id):
    container = get_container(container_id)
    details = get_container_details(container)
    return render_template('container_details.html', details=details)

# Start container
@app.route('/container/<container_id>/start', methods=['POST'])
def start_container(container_id):
    container = get_container(container_id)
    container.start()
    return redirect('/', 302)

# Stop container
@app.route('/container/<container_id>/stop', methods=['POST'])
def stop_container(container_id):
    container = get_container(container_id)
    container.stop()
    return redirect('/', 302)

# Remove container
@app.route('/container/<container_id>/remove', methods=['POST'])
def remove_container(container_id):
    container = get_container(container_id)
    container.remove()
    return redirect('/', 302)

# Build container
@app.route('/container/build', methods=['POST'])
def build_container():
    build_path = request.form['build_path']
    tag = request.form['tag']
    client.images.build(path=build_path, tag=tag)
    return redirect('/', 302)

# Save container state
@app.route('/container/<container_id>/save', methods=['POST'])
def save_container_state(container_id):
    container = get_container(container_id)
    container.commit()
    return redirect('/', 302)

# Add bookmark
@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    url = request.form['url']
    bookmarks = request.cookies.get('bookmarks', '')
    bookmarks += f'{url};'
    response = make_response(redirect('/'))
    response.set_cookie('bookmarks', bookmarks)
    return response

# Remove bookmark
@app.route('/remove_bookmark', methods=['POST'])
def remove_bookmark():
    url = request.form['url']
    bookmarks = request.cookies.get('bookmarks', '').split(';')
    bookmarks.remove(url)
    updated_bookmarks = ';'.join(bookmarks)
    response = make_response(redirect('/'))
    response.set_cookie('bookmarks', updated_bookmarks)
    return response


# Load device names from file if it exists
try:
    with open(DEVICE_NAMES_FILE, "r") as f:
        device_names = json.load(f)
except FileNotFoundError:
    pass

def scan_network(range):
    previous_devices = []
    while True:
        devices = get_connected_devices(range + "/24")
        if devices != previous_devices:
            send_notification(devices)
        previous_devices = devices
        with app.app_context():
            app.devices = devices
        time.sleep(120)  # Perform scan every 2 minutes

def get_connected_devices(range):
    nm = nmap.PortScanner()
    nm.scan(hosts=range, arguments='-sn')
    devices = []
    for host in nm.all_hosts():
        print(host)
        if 'mac' in nm[host]['addresses']:
            ip = nm[host]['addresses']['ipv4']
            mac = nm[host]['addresses']['mac']
            hostname = nm[host].hostname() if 'hostname' in nm[host] else ''
            # Load device names from file if it exists
            try:
                with open(DEVICE_NAMES_FILE, "r") as f:
                    device_names = json.load(f)
            except FileNotFoundError:
                pass
            device_name = device_names.get(mac, '')  # Get the assigned name for the device
            devices.append({'ip': ip, 'mac': mac, 'hostname': hostname, 'name': device_name})
    return devices

def send_notification(devices):
    # Implement your notification logic here
    pass

@app.route('/nmap/<range>', methods=['GET', 'POST'])
def index(range):
    if request.method == 'POST':
        mac = request.form['mac']
        name = request.form['name']
        device_names[mac] = name
        with open(DEVICE_NAMES_FILE, "w") as f:
            json.dump(device_names, f)
            print("name change sucsessful")
        return render_template('devices.html', range=range)
    else:
        return render_template('devices.html', range=range)

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            devices = getattr(app, 'devices', [])
            yield 'data: {}\n\n'.format(json.dumps(devices))
            time.sleep(60)  # Update every 60 seconds

    return Response(event_stream(), mimetype="text/event-stream")




menu_entry_index = 0
file_list = []
exit = False


def list_files(directory="/home/boejaker"):
    print("loading...")
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
            

if __name__ == '__main__':
    web_thread = Thread(target=app.run, kwargs={"threaded":True, "host":"0.0.0.0", "port":"5005"})
    web_thread.start()
    main_menu_loop()
    docker_menu_loop()

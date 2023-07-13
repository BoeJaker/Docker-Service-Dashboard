import libtmux

server = libtmux.Server()

session_name="Docker"

menu_logic = "sudo python3 /home/boejaker/BACKUPS/Legacy/MEGA T470s/Programming - Docker/Service_Dashboard_2/ServiceDashboard.py"
print(server)
session = server.new_session(session_name=session_name, 
                            kill_session=True, 
                            attach=True, 
                            start_directory=None, 
                            window_name=None, 
                            window_command=menu_logic, 
                            x=None, 
                            y=None
                            )

# window = session.new_window(window_name=None, 
#                             start_directory=None, 
#                             attach=True, window_index='', 
#                             window_shell=None, 
#                             environment=None
#                             )
window = session.windows[0]
session.attach_session()

while True:
    pass
   

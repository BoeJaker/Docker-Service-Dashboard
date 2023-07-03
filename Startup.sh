# Start Docker Services
docker-compose --build up .docker-compose.yml

# Start Docker Dashboard
python3 "/home/boejaker/MEGA/Programming - Docker/Service_Dashboard_2/app.py" &

# # Set compose file locations
# compose_files=[./Workbench,./Docker-MediaServer,]

# # Check Running Containers
# running_containers=$(docker ps)

# for cont in running_containers
# do
#     echo $cont
# done

# # Crtoss Refrence Docker Compose
# for file in compose_files
# do
#     cd $file
#     docker-compose up $containers
# done

#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to bring up the services
start_services() {
    echo "Bringing up Docker Compose services..."
    sudo docker-compose up --build -d
    sudo docker-compose ps
}

# Function to bring down the services
stop_services() {
    echo "Bringing down Docker Compose services..."
    sudo docker-compose down
    sudo docker-compose ps
}

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "No arguments provided. Use 'start' or 'stop'."
    exit 1
fi

# Check the argument value
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    *)
        echo "Invalid argument. Use 'start' or 'stop'."
        exit 1
        ;;
esac

# #USING BASE IMAGE FROM DOCKER HUB
FROM python:3.10

RUN apt-get -y update

# UPGRADING PIP 
RUN pip install --upgrade pip

# Install system dependencies
RUN apt-get update && apt-get install -y 
RUN apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev

# Set the working directory in the container
WORKDIR /app/

# COPY SOURCE CODE INTO APP FOLDER
COPY . .

# Install the project dependencies
RUN pip install -r requirements.txt

# Run Gunicorn
ENTRYPOINT [ "sh", "-c", "./entrypoint.sh" ]

# LinkedU
# Project Setup Guie.
## step-1 Step 1: Clone the Project Repository
Clone the project repository to your local machine using the following command::
Example: git clone "repo url"


## Step 2: Configure the Environment
Navigate to the project directory and create a .env file where manage.py exists. Update the .env file with your system’s IP address for the POSTGRES_HOST variable. Here’s an example of how to set it:
  - Navigate to the project directory:
      - cd LinkedU
  - Create and edit the .env file: 
      - nano .env
  - Add or update the POSTGRES_HOST variable with your system’s IP address:
      - POSTGRES_HOST=your_system_ip


## Step 3: Start and Stop the Project
The project includes a setup.sh script to simplify starting and stopping the Docker Compose services. Execute the following commands from the project directory:

To Start the Project
Run the following command to start the Docker Compose services:

- ./setup.sh start

To Stop the Project
Run the following command to stop the Docker Compose services:
- ./setup.sh stop

**Note**: Ensure that the setup.sh script is executable. You can make it executable with the following command:
chmod +x setup.sh




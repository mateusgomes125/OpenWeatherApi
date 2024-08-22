# Weather API

This application is a service API built in Python using Flask. It collects weather data from various cities using the OpenWeather API and stores this information in a MongoDB database. The application is configured to run in a Docker container, ensuring easy portability and environment consistency.

## Features

- **POST `/weather`**: Receives a `user_id`, collects weather data from specific cities, and stores it in the database.
- **GET `/weather/<user_id>`**: Returns the progress of weather data collection for the given `user_id`.
- **GET `/city/<user_id>`**: Returns the cities associated with the provided `user_id`.

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [MongoDB](https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.12-signed.msi)

## Setup and Execution

1. **Clone the Repository**

   Clone this repository to your local environment:

  `git clone https://github.com/mateusgomes125/OpenWeatherApi.git`
  
   `cd weather-api`

# Starting the Service
`docker-compose up`

# API Testing Tool (Postman, etc.)
  
  ## To Start the API Process

  Method: POST
  Endpoint: http://127.0.0.1:5000/weather

  JSON body
  {
    "user_id": "12345"
  }

  ## To Monitor the Progress of the POST Operation
  Method: GET
  Endpoint: http://127.0.0.1:5000/weather/<user_id>


  ## To Check the Cities Retrieved by User
  Method: GET
  Endpoint: http://127.0.0.1:5000/city/<user_id>


# Checking the Records Inserted into the Database

  - Open another terminal

  - Execute the following commands:

    `docker ps`

    `docker exec -it <container_id> mongosh`

    `show dbs`

    `use weather_db`

    `show collections`

    `db.cities.find().pretty()`

# Stopping the Service
`docker-compose down`


# Running Tests
 
To run the tests, you need to run the API locally. Here are the necessary steps:

  Install Python, version 3.10 - (https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz)

  Install the dependency manager `pip install pip`
  
  Install MongoDB - (https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.12-signed.msi)

  # Creating the Virtual Environment
  `python3 -m venv venv`

  # Activating the Virtual Environment
  ## LINUX
  `source venv/bin/activate`

  ## WINDOWS
  `venv\Scripts\activate`

  # Installing Packages in the Virtual Environment
  `pip install -r requirements.txt`



  # Running the Tests
    Assign 'test' to the FLASK_ENV environment variable in the .env file at the project root:

  `pytest -s test/test_app.py`







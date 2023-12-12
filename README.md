# Train Station API Service

## Description

Welcome to the Train Station API Service, where travellers can seamlessly book tickets for upcoming train journeys. 
This API provides comprehensive information about trains, crews, stations, and journeys, enhancing your travel experience. 
Additionally, JWT authentication ensures secure access to the service, requiring a personal Access Token obtained during registration.


### DB Diagram

## Features

### Train Information
* Retrieve detailed information about trains, including cargo capacity, passenger capacity, and associated train types.

### Crew Details
* Access information about crew members, including their first and last names.

### Station Insights
* Obtain details about train stations, such as names and geographical coordinates.

### Journey Data
* Retrieve information about journeys, including routes, associated trains, crews, departure, and arrival times.

### Order Creation
* Create orders with tickets to book your upcoming train trips seamlessly.

### JWT Authentication
* Securely access the API using JWT authentication.
* Obtain a personal Access Token and Refresh Token after registering to authenticate API requests.

### Admin Privileges
* As an administrator (staff member), you have elevated privileges, allowing you to perform operations such as creating, deleting, and updating records within the API. 
Admins can manage trains, crews, stations, journeys, and orders.

## API Endpoints

### USE this ip address: http://127.0.0.1:8000

#### Access to Data Endpoints
* /api/train_station/stations/
* /api/train_station/routes/
* /api/train_station/trains/
* /api/train_station/crews/
* /api/train_station/journeys/
* /api/train_station/orders/

#### User Authentication and Registration Endpoints
* api/user/register/
* api/user/token/
* api/user/token/refresh/
* api/user/token/verify/
* api/user/me/

### Also, you can test API through *Swagger*
* Explore the API using Swagger, a user-friendly interface for testing and understanding available endpoints.
* http://127.0.0.1:8000/api/doc/swagger/

### To get access for API

1) Clone the repository `git clone https://github.com/Shatrovskyi/train-station-api-service.git`
2) Create .env file using .env.sample as an example
3) Use `docker-compose up --build`
4) Login into the Docker `docker login`
5) Pull the docker repository `docker pull shatrovskyivladyslav/train_station_api_service-app:latest`
6) Run the docker-compose.yml file `docker-compose up`
7) Follow the Endpoints

### API web pages examples


##### License
This Train Station API is licensed under the MIT License. Travel safely and enjoy your journeys!

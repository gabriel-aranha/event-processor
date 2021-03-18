[![Build](https://github.com/gabriel-aranha/event-processor/actions/workflows/python-app.yml/badge.svg)](https://github.com/gabriel-aranha/event-processor/actions/workflows/python-app.yml)
# RabbitMQ Event Processor
Project written in Python to consume RabbitMQ messages, validate them, and persist in a MongoDB instance.
# Overview
1. The code consumes mock messages from the RabbitMQ events queue produced by the project in the following repository: https://github.com/gabriel-aranha/event-producer  
2. The messages consumed are then validated according to its JSON schema and necessary values types, depending on the event-type key.
3. If a validation is successful, the message is persisted on MongoDB and the message ID is sent to a new RabbitMQ queue named validation-success for further processing.
4. If a validation is not successful, the message is persisted on MongoDB and the message ID along with the validation error is sent to a new RabbitMQ queue named validation-error for further processing.
# Quickstart with Docker Compose
## Setup
1. Clone this repository:
    ```
    $ git clone git@github.com:gabriel-aranha/event-processor.git
    ```
2. Enter the folder:
    ```
    $ cd event-processor
    ```
3. Send the docker compose command:
    ```
    $ docker-compose up --build
4. Wait for the event-processor, MongoDB, and RabbitMQ to startup.  
4.1 RabbitMQ Management can be accessed on the following address and credentials:  
    ```
    http://localhost:15672

    Username: guest
    Password: guest
    ```  
<<<<<<< HEAD
    4.2 MongoDB can be accessed on the following address and credentials:
    ```
    http://localhost:27017

    Username: mongo
    Password: password1234
    ```
=======
    4.2 Redis can be accessed on Port 6379.
>>>>>>> a6addd730491bd3144da4f5b842feda3544f279a

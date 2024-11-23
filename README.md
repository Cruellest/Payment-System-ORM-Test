# Payment System

This repository is an recreational implementation of an connection system using SQLAlchemy and Flask

First, got to the `env_model` file and set up your own variables. Then, to run the app, in the root of your project run:
````sh
docker compose -f payment_system.yml up
````
- if you want to follow the logs, or
````sh
docker compose -f payment_system.yml up -d
````
- if you don't.

To stop the application, run:
````sh
docker compose -f payment_system.yml stop
````



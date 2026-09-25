# AWS Docker Web Application

A hands-on DevOps project demonstrating a containerized web application running behind an Nginx reverse proxy.

## Architecture

Client
  |
  v
Nginx :80
  |
  v
Gunicorn :5000
  |
  v
Flask Application

The application container is not exposed directly to the host. Nginx receives incoming traffic and forwards requests to the application through the internal Docker network.

## Technologies

- Python
- Flask
- Gunicorn
- Docker
- Docker Compose
- Nginx

## Features

- Dockerized Flask application
- Gunicorn application server
- Nginx reverse proxy
- Docker Compose orchestration
- Internal container networking
- Application health check
- Restart policies
- /health endpoint

## Run Locally

Build and start the environment:

docker compose up -d --build

Open:

http://localhost

Health check:

http://localhost/health

## Check Services

docker compose ps

## View Logs

docker compose logs nginx
docker compose logs app

## Stop

docker compose down

## Next Phase

Deploy the same architecture to an AWS EC2 instance.

# Real-Time Notifications Service (FastAPI & WebSocket)

## Overview

This service is responsible for handling real-time notifications for order updates in a simulated e-commerce platform. It utilizes FastAPI with WebSockets to push updates to the User Management Service whenever an order update is received from the Order Processing Service via RabbitMQ.

## Project Structure

```
app/
├── main.py          # Runs the FastAPI WebSocket server
├── rabbitmq.py      # Handles RabbitMQ queue consumption
├── websocket.py     # WebSocket manager for handling user connections
```
## Functionality

 - Users connect to the WebSocket server at ```ws://localhost:600/ws/{user_id}``` to receive real-time order updates.

 - Order Processing Service sends messages to RabbitMQ when an order is updated.

 - This service listens for messages on the RabbitMQ queue and pushes them to connected WebSocket clients.

 - Error monitoring is integrated using Sentry.

 - Swagger documentation is not provided as this service only contains a WebSocket route.

## Deployment Instructions

Prerequisites

Ensure you have the following installed:

 - Python 3.9+

 - RabbitMQ

 - Docker (Optional, for containerized deployment)

## Environment Variables

Create a .env file in the project root with the following variables:

```

RABBITMQ_URL = your_rabbitmq_url
QUEUE_NAME = your_queue_name
DATABASE_URL = your_database_url
SENTRY_DSN = your_sentry_dsn
```

## Local Setup

 - Setup Virtual env

```
python -m venv venv
source venv/bin/activate (on macOS), venv/Scripts/activate (on Windows)
```

 - Install dependencies:
```
pip install -r requirements.txt
```



 - Start the WebSocket server:

```
uvicorn app.main:app --port 6000 --reload
```

## Docker Deployment

 - Build the Docker image:
```
docker build -t realtime-notifications .
```

 - Run the container:
```
docker run -d -p 600:600 --name notifications-service --env-file .env realtime-notifications
```

## Logs & Monitoring

 - View logs in real-time:
```
docker logs -f notifications-service
```
 - Check Sentry for error tracking.

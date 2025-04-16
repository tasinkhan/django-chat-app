# Django Chat Application

A real-time chat application built with Django, Django Channels, and PostgreSQL with master-slave replication.

## Features

- Real-time chat using WebSocket connections
- User authentication with JWT tokens
- Organization-based user management
- Role-based access control
- API documentation with Swagger/OpenAPI
- PostgreSQL master-slave replication
- Asynchronous task processing with Celery
- Docker containerization
- Continuos Integration using Github actions

## Tech Stack

- **Backend Framework**: Django 5.2
- **API Framework**: Django REST Framework
- **WebSocket**: Django Channels
- **Database**: PostgreSQL 14 (Master-Slave Configuration)
- **Cache & Message Broker**: Redis
- **Task Queue**: Celery
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Authentication**: JWT (Simple JWT)
- **Web Server**: Nginx
- **ASGI Server**: Daphne
- **Container Platform**: Docker & Docker Compose


## Prerequisites

- Docker
- Docker Compose
- Make (optional, for Makefile usage)

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/tasinkhan/django-chat-app.git
cd django-chat-app
```

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Access the application:
- Web Application: http://localhost
- API Documentation: http://localhost/docs/
- Admin Interface: http://localhost/admin/

## API Endpoints

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token
- `POST /api/organization/create/`: Create organization(s)
- `POST /api/role/create/`: Create role(s)
- `POST /api/user/create/`: Create user(s)

## WebSocket Endpoints

- `ws://localhost/ws/chat/{user_id}/`: Chat WebSocket connection

## Development

### Code Linting
```bash
docker-compose exec web flake8
```

### Database Migrations
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Project Structure

```
django-chat-app/
├── apps/
│   ├── chat/
│   ├── core/
│   ├── organizations/
│   ├── roles_permissions/
│   └── users/
├── compose/
│   ├── nginx/
│   └── postgres/
├── django_chat_app/
└── docker-compose.yml
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Market Info API

A Django REST API for fetching and storing website information.

## Features

- Validate URLs
- Extract website information (domain name, protocol, title, images, stylesheets count)
- Store website information in a database
- RESTful API for CRUD operations on website information

## Project Structure

The project follows a clean, modular structure:

```
market-info-api/
├── apps/                  # Main Django project directory
│   ├── core/              # Core app with models, views, and serializers
│   │   ├── admin.py       # Admin configuration
│   │   ├── models.py      # Database models
│   │   ├── serializers.py # REST API serializers
│   │   ├── urls.py        # URL routing for the core app
│   │   └── views.py       # API views and logic
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration for deployment
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── manage.py              # Django management script
├── Makefile               # Utility commands
└── pyproject.toml         # Poetry dependency management
```

## Requirements

- Python 3.11+
- Docker and Docker Compose
- Poetry (for dependency management)

## Setup

### Using Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd market-info-api
   ```

2. Build and run the Docker containers:
   ```bash
   make build
   make up
   ```

3. Run migrations:
   ```bash
   make migrate
   ```

4. Create a superuser (optional):
   ```bash
   make superuser
   ```

5. The API will be available at http://localhost:8000/api/

### Without Docker (Local Development)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd market-info-api
   ```

2. Install dependencies using Poetry:
   ```bash
   make local-install
   ```

3. Run migrations:
   ```bash
   make local-migrate
   ```

4. Create a superuser (optional):
   ```bash
   make local-superuser
   ```

5. Run the development server:
   ```bash
   make local-run
   ```

6. The API will be available at http://localhost:8000/api/

## Makefile Commands

The project includes a Makefile to simplify common tasks:

### Docker Commands
- `make build` - Build Docker containers
- `make up` - Start Docker containers
- `make down` - Stop Docker containers
- `make shell` - Open a shell in the web container

### Django Commands
- `make migrate` - Run Django migrations
- `make makemigrations` - Create new Django migrations
- `make superuser` - Create a Django superuser
- `make collectstatic` - Collect static files

### Development Commands
- `make test` - Run tests
- `make lint` - Run linting checks
- `make format` - Format code with black and isort
- `make clean` - Remove Python cache files

### Local Development Commands
- `make local-install` - Install dependencies with Poetry
- `make local-migrate` - Run Django migrations locally
- `make local-makemigrations` - Create new Django migrations locally
- `make local-superuser` - Create a Django superuser locally
- `make local-run` - Run the development server locally
- `make local-test` - Run tests locally
- `make local-lint` - Run linting checks locally
- `make local-format` - Format code locally

## API Endpoints

### Website Information

- `GET /api/websites/` - List all website information
- `POST /api/websites/` - Create new website information
  - Required parameters: `url` (string)
- `GET /api/websites/{id}/` - Retrieve specific website information
- `DELETE /api/websites/{id}/` - Delete specific website information

## Example Usage

### Create Website Information

```bash
curl -X POST http://localhost:8000/api/websites/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

### List All Website Information

```bash
curl -X GET http://localhost:8000/api/websites/
```

### Retrieve Specific Website Information

```bash
curl -X GET http://localhost:8000/api/websites/1/
```

### Delete Website Information

```bash
curl -X DELETE http://localhost:8000/api/websites/1/
```

## License

[MIT License](LICENSE)

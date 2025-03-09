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
├── apps/                     # Main Django project directory
│   ├── website_info/         # Website info app with models, views, and serializers
│   │   ├── admin.py          # Admin configuration
│   │   ├── models.py         # Database models
│   │   ├── serializers.py    # REST API serializers
│   │   ├── urls.py           # URL routing for the website_info app
│   │   └── views.py          # API views and logic
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration for deployment
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration
├── manage.py                 # Django management script
├── Makefile                  # Utility commands
└── pyproject.toml            # Poetry dependency management
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

2. Build, migrate, and start the application in one command:
   ```bash
   make start
   ```

   Or step by step:
   ```bash
   make build
   make up
   make migrate
   ```

3. Create a superuser (optional):
   ```bash
   make superuser
   ```

4. The API will be available at http://localhost:8000/api/
   The admin interface will be available at http://localhost:8000/admin/

### Without Docker (Local Development)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd market-info-api
   ```

2. Install dependencies using Poetry in a virtual environment:
   ```bash
   make local-install
   ```

3. Activate the virtual environment (optional):
   ```bash
   make local-shell
   ```
   
   Or run commands with `poetry run` prefix (handled by the Makefile commands).

4. Run migrations:
   ```bash
   make local-migrate
   ```

5. Create a superuser (optional):
   ```bash
   make local-superuser
   ```

6. Run the development server:
   ```bash
   make local-run
   ```

7. The API will be available at http://localhost:8000/api/
   The admin interface will be available at http://localhost:8000/admin/

## Makefile Commands

The project includes a Makefile to simplify common tasks:

### Docker Commands
- `make build` - Build Docker containers
- `make up` - Start Docker containers
- `make down` - Stop Docker containers
- `make shell` - Open a shell in the web container
- `make start` - Build, migrate, and start the application in one command

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
- `make local-install` - Install dependencies in a virtual environment
- `make local-shell` - Activate the virtual environment
- `make local-migrate` - Run Django migrations locally
- `make local-makemigrations` - Create new Django migrations locally
- `make local-superuser` - Create a Django superuser locally
- `make local-run` - Run the development server locally
- `make local-test` - Run tests locally
- `make local-lint` - Run linting checks locally
- `make local-format` - Format code locally

## API Endpoints

### Website Information

- `GET /api/website-info/` - List all website information
- `POST /api/website-info/` - Create new website information
  - Required parameters: `url` (string)
- `GET /api/website-info/{id}/` - Retrieve specific website information
- `DELETE /api/website-info/{id}/` - Delete specific website information

## Example Usage

### Create Website Information

```bash
curl -X POST http://localhost:8000/api/website-info/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

### List All Website Information

```bash
curl -X GET http://localhost:8000/api/website-info/
```

### Retrieve Specific Website Information

```bash
curl -X GET http://localhost:8000/api/website-info/1/
```

### Delete Website Information

```bash
curl -X DELETE http://localhost:8000/api/website-info/1/
```

## License

[MIT License](LICENSE)

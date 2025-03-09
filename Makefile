.PHONY: help build up down shell migrate makemigrations superuser test lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make build         - Build Docker containers"
	@echo "  make up            - Start Docker containers"
	@echo "  make down          - Stop Docker containers"
	@echo "  make shell         - Open a shell in the web container"
	@echo "  make migrate       - Run Django migrations"
	@echo "  make makemigrations - Create new Django migrations"
	@echo "  make superuser     - Create a Django superuser"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Remove Python cache files"
	@echo "  make start         - Build, migrate, and start the application"
	@echo "  make local-install - Install dependencies in a virtual environment"
	@echo "  make local-shell   - Activate the virtual environment"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

shell:
	docker-compose exec web bash

# Django commands
migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

superuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Development commands
test:
	docker-compose exec web python manage.py test

lint:
	docker-compose exec web flake8 .

format:
	docker-compose exec web black .
	docker-compose exec web isort .

# Combined commands
start: build
	docker-compose up -d
	@echo "Waiting for containers to start..."
	@sleep 5
	docker-compose exec web python manage.py migrate

# Local development commands (with virtual environment)
local-install:
	poetry config virtualenvs.in-project true
	poetry install

local-shell:
	poetry shell

local-migrate:
	poetry run python manage.py migrate

local-makemigrations:
	poetry run python manage.py makemigrations

local-superuser:
	poetry run python manage.py createsuperuser

local-run:
	poetry run python manage.py runserver

local-test:
	poetry run python manage.py test

local-lint:
	poetry run flake8 .

local-format:
	poetry run black .
	poetry run isort .

# Utility commands
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name ".nox" -exec rm -rf {} +

# Default target
all: help

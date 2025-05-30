.PHONY: help build up down shell migrate makemigrations superuser test lint format clean

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Docker commands:"
	@echo "  make build         - Build Docker containers"
	@echo "  make up            - Start Docker containers"
	@echo "  make down          - Stop Docker containers"
	@echo "  make shell         - Open a shell in the web container"
	@echo ""
	@echo "Django commands:"
	@echo "  make migrate       - Run Django migrations"
	@echo "  make makemigrations - Create new Django migrations"
	@echo "  make superuser     - Create a Django superuser"
	@echo "  make collectstatic - Collect static files"
	@echo ""
	@echo "Development commands:"
	@echo "  make test          - Run tests with pytest"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Remove Python cache files"
	@echo ""
	@echo "Combined commands:"
	@echo "  make start         - Build, migrate, and start the application"
	@echo ""
	@echo "Local development commands:"
	@echo "  make local-install - Install dependencies in a virtual environment"
	@echo "  make local-shell   - Show instructions to activate the virtual environment"
	@echo "  make local-migrate - Run Django migrations locally"
	@echo "  make local-makemigrations - Create new Django migrations locally"
	@echo "  make local-superuser - Create a Django superuser locally"
	@echo "  make local-run     - Start development server locally"
	@echo "  make local-test    - Run tests locally with pytest"
	@echo "  make local-test-coverage - Run tests locally with coverage report"
	@echo "  make local-lint    - Run linting checks locally"
	@echo "  make local-format  - Format code locally"

# Docker commands
build:
	@echo "Building Docker containers..."
	docker-compose build

up:
	@echo "Starting Docker containers..."
	docker-compose up

down:
	@echo "Stopping Docker containers..."
	docker-compose down

shell:
	@echo "Opening shell in web container..."
	docker-compose exec web bash

# Django commands
migrate:
	@echo "Running migrations..."
	docker-compose exec web python manage.py migrate

makemigrations:
	@echo "Creating migrations..."
	docker-compose exec web python manage.py makemigrations

superuser:
	@echo "Creating superuser..."
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	@echo "Collecting static files..."
	docker-compose exec web python manage.py collectstatic --noinput

# Development commands
test:
	@echo "Running tests with pytest..."
	docker-compose exec web pytest

lint:
	@echo "Running linting checks..."
	docker-compose exec web flake8 .

format:
	@echo "Formatting code..."
	docker-compose exec web black .
	docker-compose exec web isort .

# Combined commands
start: build
	@echo "Starting application..."
	docker-compose up -d
	@echo "Waiting for containers to start..."
	@sleep 5
	@echo "Running migrations..."
	docker-compose exec web python manage.py migrate
	@echo "Application is running at http://localhost:8000"

# Local development commands (with virtual environment)
local-install:
	@echo "Setting up Python virtual environment..."
	python3 -m venv .venv 
	@echo "Installing Poetry in virtual environment..."
	.venv/bin/pip install --upgrade pip poetry
	@echo "Installing dependencies with Poetry..."
	.venv/bin/poetry install
	@echo "Dependencies installed successfully in .venv directory."
	@echo "To activate the virtual environment, run: source .venv/bin/activate"

local-shell:
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"

local-migrate:
	@echo "Running migrations..."
	.venv/bin/python manage.py migrate

local-makemigrations:
	@echo "Creating migrations..."
	.venv/bin/python manage.py makemigrations

local-superuser:
	@echo "Creating superuser..."
	.venv/bin/python manage.py createsuperuser

local-run:
	@echo "Starting development server..."
	.venv/bin/python manage.py runserver
	
local-test:
	@echo "Running tests with pytest..."
	.venv/bin/pytest

local-lint:
	@echo "Running linting checks..."
	.venv/bin/flake8 .

local-format:
	@echo "Formatting code..."
	.venv/bin/black .
	.venv/bin/isort .

# Add coverage commands
test-coverage:
	@echo "Running tests with coverage..."
	docker-compose exec web pytest --cov=apps --cov-report=html

local-test-coverage:
	@echo "Running tests with coverage..."
	.venv/bin/pytest --cov=apps --cov-report=html

# Utility commands
clean:
	@echo "Cleaning up Python cache files..."
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
	@echo "Cleanup complete."

# Default target
all: help

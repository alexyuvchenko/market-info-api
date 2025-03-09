FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==2.1.1

# Copy poetry configuration files
COPY pyproject.toml ./

# Configure poetry to not use a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies without the root package
RUN poetry install --no-interaction --no-ansi --no-root

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 

FROM python:3.12-slim

# Set environment variables to avoid writing .pyc files and buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency definitions first to leverage Docker cache
COPY pyproject.toml ./

# Install dependencies
RUN uv sync

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Run the app using uv
CMD ["uv", "run", "python", "main.py"]
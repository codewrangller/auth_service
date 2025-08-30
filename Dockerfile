# Use simple Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV=dev

# Set work directory
WORKDIR /app

# Install system dependencies
RUN set -eux; \
    # Add retry logic and use a different mirror
    for i in $(seq 1 3); do \
        apt-get update -o Acquire::Retries=3 && \
        apt-get install -y --no-install-recommends \
            gcc \
            python3-dev \
            postgresql-client \
            libpq5 \
            libpq-dev && \
        rm -rf /var/lib/apt/lists/* && \
        break || \
        if [ $i -lt 3 ]; then sleep 1; fi; \
    done

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt file into the container
COPY requirements.txt /app/

# Install system dependencies (example for common packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port your backend is running on
EXPOSE 8000

# Command to run the backend application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
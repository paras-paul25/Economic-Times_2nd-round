FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=10000
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose the port
EXPOSE 10000

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]

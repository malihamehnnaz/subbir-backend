FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for JSON files
RUN mkdir -p /app/data

# Set environment variables
ENV PORT=8000
ENV PYTHONPATH=/app

EXPOSE 8000

# Run with Uvicorn directly
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

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

# Run with Uvicorn using the platform-provided PORT (fallback to 8000)
# Many PaaS platforms (Railway, Heroku, etc.) provide the port to listen on
# via the PORT environment variable. Use a shell command so the variable
# is expanded at container start time.
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

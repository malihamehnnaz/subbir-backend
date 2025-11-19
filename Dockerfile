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
# Use an explicit startup script as ENTRYPOINT so the container always
# launches Uvicorn with the platform-provided PORT. This is more robust
# against platform overrides of the CMD.
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
ENTRYPOINT ["/app/start.sh"]

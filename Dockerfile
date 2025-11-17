FROM python:3.12-slim

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 8000

# Run the FastAPI app directly using the full module path.
# Since WORKDIR is /app (repo root), we reference services.email_api.main:app
CMD ["uvicorn", "services.email_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

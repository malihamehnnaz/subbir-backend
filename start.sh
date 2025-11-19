#!/bin/sh
# Start script ensures the app binds to the platform-provided PORT
PORT=${PORT:-8000}
exec python -m uvicorn main:app --host 0.0.0.0 --port "$PORT"

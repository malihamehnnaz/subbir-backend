#!/usr/bin/env python
"""Start uvicorn server with proper environment variable handling."""
import os
import subprocess
import sys

port = os.environ.get("PORT", "8000")
host = os.environ.get("HOST", "0.0.0.0")

print(f"Starting uvicorn on {host}:{port}")

subprocess.run([
    sys.executable,
    "-m",
    "uvicorn",
    "main:app",
    "--host",
    host,
    "--port",
    port,
])

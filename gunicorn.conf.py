"""Gunicorn configuration file."""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8008"

# Worker processes
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() + 1))
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Process naming
proc_name = "fastapi-auth"

# Server mechanics
daemon = False
pidfile = None

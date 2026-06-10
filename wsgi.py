#!/usr/bin/env python3
"""
WSGI entry point for production deployment
Use with Gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from main import app

if __name__ == "__main__":
    app.run()

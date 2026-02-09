"""
WSGI configuration for PythonAnywhere deployment.
This file should be used to replace the default WSGI file in PythonAnywhere.
"""
import sys
import os

# Add your project directory to the sys.path
path = '/home/Azeem123/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Import and run FastAPI app
from server import app as application

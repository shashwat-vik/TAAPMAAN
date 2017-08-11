import sys, os, logging

root = os.path.join(os.getcwd(), "app")
import_path = os.path.abspath(root)

if import_path not in sys.path:
    sys.path.insert(0, import_path)

from app import app

# Initialize WSGI app object
application = app

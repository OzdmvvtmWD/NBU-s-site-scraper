"""
File for configurations 
"""
import os

from headers import DEFAULT_HEADERS

#path to save json requests from site
create_dir = lambda file_name: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', file_name))

JSON_DIR = create_dir('json')
LOGS_DIR = create_dir('logs')

os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
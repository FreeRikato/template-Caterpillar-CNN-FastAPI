# gunicorn_config.py

import multiprocessing

# Bind to port 8000 on localhost
bind = "0.0.0.0:8000"
# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1
# Log level
loglevel = "debug"
# Access log - format (this is the default anyway)
accesslog = "-"
# Error log - format (this is the default anyway)
errorlog = "-"

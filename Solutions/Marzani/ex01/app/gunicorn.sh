#!/bin/sh
gunicorn -w 1 app:app -b 0.0.0.0:5000 --access-logfile=-
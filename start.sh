#!/usr/bin/env bash
echo "-----> Starting application"
gunicorn app:app --workers 4 --worker-class gevent --bind 0.0.0.0:10000
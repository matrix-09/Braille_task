#!/usr/bin/env bash
echo "-----> Starting Braille Auto-Correct System"
exec gunicorn app:app \
  --workers 2 \
  --worker-class gevent \
  --bind 0.0.0.0:$PORT \
  --timeout 120 \
  --log-file - \
  --access-logfile -
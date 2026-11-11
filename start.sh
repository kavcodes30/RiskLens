#!/bin/bash

# Backend: bound to localhost only, so it is not reachable from outside the container
uvicorn app:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Frontend: the only thing exposed to the outside
streamlit run frontend.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true &
FRONTEND_PID=$!

# Forward docker stop / Ctrl+C to both processes
trap 'kill -TERM $BACKEND_PID $FRONTEND_PID 2>/dev/null' TERM INT

# If either process exits, stop the container so Docker can restart it
wait -n $BACKEND_PID $FRONTEND_PID
EXIT_CODE=$?
kill -TERM $BACKEND_PID $FRONTEND_PID 2>/dev/null
wait
exit $EXIT_CODE
#!/bin/bash
set -e

# Start backend and frontend for development/deployment
python main.py &
backend_pid=$!

streamlit run frontend/app.py --server.port "${FRONTEND_PORT:-8501}" --server.address 0.0.0.0 &
frontend_pid=$!

wait $backend_pid $frontend_pid

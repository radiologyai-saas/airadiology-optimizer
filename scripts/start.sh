#!/bin/bash
# Start Flask backend and Streamlit frontend
set -e

python main.py &
streamlit run frontend/app.py

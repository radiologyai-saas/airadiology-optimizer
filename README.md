# AI Radiology Optimizer

This project provides a minimal Radiology SaaS prototype with a Flask backend and a Streamlit frontend.

## Features
- Image upload and dummy analysis
- PDF report generation
- Referral tracking with Stripe checkout session stub
- Scan scoring and leaderboard
- Simple intern quiz mode

## Requirements
Install dependencies with:
```
pip install -r requirements.txt
```

## Running locally
1. Install dependencies and launch both services with:
   ```
   bash scripts/start.sh
   ```
   This starts the Flask API in the background and opens the Streamlit UI.
   Set `BACKEND_URL` in `.streamlit/secrets.toml` if the backend runs on a different host.

## Deploying to Render
- Use a Python environment.
- Set the start command to `bash scripts/start.sh`.
- Add environment variables such as `STRIPE_API_KEY` and `OPENAI_API_KEY`.

## Deploying to Replit
- Create a new Replit using Python.
- Add the contents of this repository.
- In the shell run `pip install -r requirements.txt`.
- Use the Run button to execute `bash scripts/start.sh` or customize the `replit.nix`/Run configuration to start both backend and frontend.


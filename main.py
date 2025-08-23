"""Entry point for running the Flask backend."""
import logging
import os

from backend import create_app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

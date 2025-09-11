import os


def get_openai_api_key(secrets=None):
    """Return OpenAI API key.

    Tries to pull the key from provided Streamlit secrets dictionary. If the
    key is not present, falls back to the ``OPENAI_API_KEY`` environment
    variable. Returns ``None`` when no key is found or the value is an empty
    string.
    """
    if secrets:
        key = secrets.get("OPENAI_API_KEY", "").strip()
        if key:
            return key
    key = os.getenv("OPENAI_API_KEY", "").strip()
    return key or None

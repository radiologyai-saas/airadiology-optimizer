import os


def get_openai_api_key(secrets=None):
    """Return OpenAI API key.

    Tries to pull the key from provided Streamlit secrets dictionary. If the
    key is not present, falls back to the ``OPENAI_API_KEY`` environment
    variable. Returns ``None`` when no key is found.
    """
    if secrets and "OPENAI_API_KEY" in secrets:
        return secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY")

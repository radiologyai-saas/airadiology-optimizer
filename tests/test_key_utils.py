import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from key_utils import get_openai_api_key


def test_returns_secret_when_available(monkeypatch):
    secrets = {"OPENAI_API_KEY": "secret"}
    monkeypatch.setenv("OPENAI_API_KEY", "env")
    assert get_openai_api_key(secrets) == "secret"


def test_falls_back_to_environment(monkeypatch):
    secrets = {}
    monkeypatch.setenv("OPENAI_API_KEY", "env")
    assert get_openai_api_key(secrets) == "env"
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert get_openai_api_key(secrets) is None

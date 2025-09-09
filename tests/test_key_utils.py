from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from key_utils import get_openai_api_key


def test_returns_secret_when_available(monkeypatch):
    secrets = {"OPENAI_API_KEY": "secret"}
    monkeypatch.setenv("OPENAI_API_KEY", "env")
    assert get_openai_api_key(secrets) == "secret"


def test_falls_back_to_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "env")
    assert get_openai_api_key() == "env"
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert get_openai_api_key() is None

import pytest

from backend import create_app
from backend.quiz import QUESTIONS
from backend.scoreboard import _scores, add_score, get_leaderboard


@pytest.fixture
def client():
    """Test client fixture."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_app():
    """Test that the Flask app is created."""
    app = create_app()
    assert app is not None


def test_leaderboard():
    """Test the leaderboard logic."""
    _scores.clear()
    add_score("alice", 10)
    add_score("bob", 5)
    board = get_leaderboard()
    assert board[0]["user"] == "alice"


def test_add_new_user_score():
    """Test adding a score for a new user."""
    _scores.clear()
    add_score("new_user", 100)
    board = get_leaderboard()
    assert any(u["user"] == "new_user" for u in board)


def test_quiz_answer_string(client):
    """Test answering a quiz question with a string answer."""
    question = QUESTIONS[0]
    response = client.post(
        "/api/quiz/answer", json={"id": question["id"], "answer": str(question["answer"])}
    )
    assert response.status_code == 200
    assert response.json["correct"] is True

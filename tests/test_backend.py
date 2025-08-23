from backend import create_app
from backend.scoreboard import add_score, get_leaderboard


def test_create_app():
    app = create_app()
    assert app is not None


def test_leaderboard():
    add_score('alice', 10)
    add_score('bob', 5)
    board = get_leaderboard()
    assert board[0]['user'] == 'alice'

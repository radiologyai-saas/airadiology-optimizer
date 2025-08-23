"""Scan scoring and leaderboard utilities."""
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)
_scores = defaultdict(int)


def add_score(user: str, score: int) -> None:
    if not user:
        return
    _scores[user] = max(score, _scores[user])
    logger.info("Recorded score %s for %s", score, user)


def get_leaderboard() -> list:
    return [
        {"user": user, "score": score}
        for user, score in sorted(_scores.items(), key=lambda x: x[1], reverse=True)
    ]

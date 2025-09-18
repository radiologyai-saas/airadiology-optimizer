"""Intern quiz utilities."""
import logging
import random

logger = logging.getLogger(__name__)

QUESTIONS = [
    {
        "id": 1,
        "question": "Which modality uses ionizing radiation?",
        "options": ["MRI", "CT", "Ultrasound", "PET"],
        "answer": 1,
    },
    {
        "id": 2,
        "question": "What does MRI stand for?",
        "options": [
            "Magnetic Resonance Imaging",
            "Minimal Radiation Imaging",
            "Motion Radio Imaging",
            "Magnetized Rotation Indicator",
        ],
        "answer": 0,
    },
]


def get_question() -> dict:
    """Return a random question without the answer."""
    q = random.choice(QUESTIONS)
    return {"id": q["id"], "question": q["question"], "options": q["options"]}


def check_answer(qid: int, answer_index: int) -> bool:
    for q in QUESTIONS:
        if q["id"] == qid:
            try:
                correct = q["answer"] == int(answer_index)
            except (ValueError, TypeError):
                correct = False
            logger.info("Question %s answered %s", qid, correct)
            return correct
    return False

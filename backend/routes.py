"""Flask routes for the Radiology AI backend."""
import io
import logging
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

from .pdf_generator import generate_report
from .image_analysis import analyze_image
from .referral import register_referral, create_checkout_session
from .scoreboard import add_score, get_leaderboard
from .quiz import get_question, check_answer

logger = logging.getLogger(__name__)

bp = Blueprint("api", __name__)


@bp.route("/api/analyze", methods=["POST"])
def analyze_route():
    """Analyze an uploaded image and return findings."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    filename = secure_filename(file.filename)
    try:
        findings = analyze_image(file.read())
        logger.info("Analyzed image %s", filename)
        return jsonify({"filename": filename, "findings": findings})
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Image analysis failed: %s", exc)
        return jsonify({"error": "analysis_failed"}), 500


@bp.route("/api/report", methods=["POST"])
def report_route():
    """Generate a PDF report from findings."""
    data = request.get_json(force=True)
    patient = data.get("patient", "Unknown")
    findings = data.get("findings", "No findings")
    try:
        pdf_bytes = generate_report(patient, findings)
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=f"{patient.replace(' ', '_')}_report.pdf",
            mimetype="application/pdf",
        )
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Report generation failed: %s", exc)
        return jsonify({"error": "report_failed"}), 500


@bp.route("/api/referral", methods=["POST"])
def referral_route():
    code = request.json.get("code")
    count = register_referral(code)
    return jsonify({"code": code, "count": count})


@bp.route("/api/checkout", methods=["POST"])
def checkout_route():
    data = request.get_json(force=True)
    session = create_checkout_session(data.get("price_id"))
    return jsonify(session)


@bp.route("/api/score", methods=["POST"])
def score_route():
    data = request.get_json(force=True)
    user = data.get("user")
    score = data.get("score", 0)
    add_score(user, score)
    return jsonify({"status": "ok"})


@bp.route("/api/leaderboard", methods=["GET"])
def leaderboard_route():
    return jsonify(get_leaderboard())


@bp.route("/api/quiz/question", methods=["GET"])
def quiz_question():
    return jsonify(get_question())


@bp.route("/api/quiz/answer", methods=["POST"])
def quiz_answer():
    data = request.get_json(force=True)
    correct = check_answer(data.get("id"), data.get("answer"))
    return jsonify({"correct": correct})


def register_routes(app):
    app.register_blueprint(bp)

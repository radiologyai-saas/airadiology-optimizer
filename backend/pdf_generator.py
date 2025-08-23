"""PDF report generation utilities."""
import io
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)


def generate_report(patient: str, findings: str) -> bytes:
    """Generate a simple PDF report and return its bytes."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Patient: {patient}")
    c.drawString(100, 730, "Findings:")
    text = c.beginText(100, 710)
    for line in findings.splitlines():
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    logger.info("Generated report for %s", patient)
    return buffer.getvalue()

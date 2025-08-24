"""Simple image analysis placeholder."""
import io
import logging
from PIL import Image

logger = logging.getLogger(__name__)


def analyze_image(data: bytes) -> str:
    """Return a dummy analysis of the uploaded image."""
    image = Image.open(io.BytesIO(data))
    width, height = image.size
    logger.info("Image processed with size %sx%s", width, height)
    return f"Image size: {width}x{height}. No anomalies detected."

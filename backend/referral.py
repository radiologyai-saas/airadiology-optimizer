"""Referral tracking and Stripe integration."""
import logging
import os
from collections import defaultdict

import stripe

logger = logging.getLogger(__name__)

stripe.api_key = os.getenv("STRIPE_API_KEY", "")
_referrals = defaultdict(int)


def register_referral(code: str) -> int:
    """Register a referral code and return its count."""
    if not code:
        return 0
    _referrals[code] += 1
    logger.info("Referral %s has count %s", code, _referrals[code])
    return _referrals[code]


def create_checkout_session(price_id: str) -> dict:
    """Create a Stripe Checkout session."""
    if not stripe.api_key:
        logger.warning("Stripe API key not configured")
        return {"error": "stripe_not_configured"}
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    logger.info("Created Stripe session %s", session.id)
    return {"id": session.id, "url": session.url}

"""
bank_response.py -- Mock bank/CFCFRMS response simulation.

After an auto-freeze smart-contract-style lien fires for a high-risk ring,
this simulates what the bank side would report back -- closing the loop
visually instead of leaving the auto-freeze as just a ledger line with no
visible outcome.
"""

import random
import uuid

BANK_NAMES = [
    "HDFC Bank", "State Bank of India", "ICICI Bank",
    "Axis Bank", "Punjab National Bank", "Kotak Mahindra Bank",
]


def simulate_bank_response(ring_id: str, amount_at_risk: float) -> dict:
    return {
        "ring_id": ring_id,
        "bank": random.choice(BANK_NAMES),
        "reference_id": f"CFCFRMS-{uuid.uuid4().hex[:10].upper()}",
        "status": "Lien Placed \u2013 Funds Held Pending Investigation",
        "amount_held": round(amount_at_risk, 2),
    }

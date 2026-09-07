"""
alert_engine.py -- Owned by: Sehaj Mahajan

Scans the ring-scored complaints DataFrame, flags rings above a risk
threshold, and produces the alerts DataFrame. Every alert also gets logged
to the AuditLedger so the audit trail tab has something to show.

Input: complaints DataFrame with ring_id, ring_risk_score, lat, lon, city
       (i.e. the output of ring_detection.detect_rings())
Output: alerts DataFrame:
    alert_id (str), ring_id (str), predicted_location (str),
    predicted_lat (float), predicted_lon (float), predicted_time_window (str),
    risk_score (float), status (str: "New" / "Investigated")
"""

import random
import uuid

import pandas as pd

from ledger import AuditLedger
from notifications import notify_all_channels
from bank_response import simulate_bank_response


def generate_alerts(df: pd.DataFrame, ledger: AuditLedger, threshold: float = 0.6) -> pd.DataFrame:
    flagged = df[df["ring_risk_score"] >= threshold].copy()
    if flagged.empty:
        return pd.DataFrame(columns=[
            "alert_id", "ring_id", "predicted_location", "predicted_lat",
            "predicted_lon", "predicted_time_window", "risk_score", "status",
            "bank_response",
        ])

    time_windows = ["Next 1-2 hours", "Next 2-4 hours", "Next 4-6 hours"]

    alerts = []
    for ring_id, group in flagged.groupby("ring_id"):
        row = group.iloc[0]
        alert = {
            "alert_id": f"ALT{uuid.uuid4().hex[:8].upper()}",
            "ring_id": ring_id,
            "predicted_location": row["city"],
            "predicted_lat": row["lat"],
            "predicted_lon": row["lon"],
            "predicted_time_window": random.choice(time_windows),
            "risk_score": float(group["ring_risk_score"].max()),
            "status": "New",
            "bank_response": None,
        }

        # Fire real notification channels (email / SMS / API webhook).
        # Each returns sent/skipped/failed -- logged to the ledger so the
        # audit trail shows exactly what notification attempt happened.
        notification_results = notify_all_channels(alert)
        ledger.add_block({
            "type": "ALERT",
            "ring_id": ring_id,
            "location": alert["predicted_location"],
            "risk_score": alert["risk_score"],
            "notifications": notification_results,
        })
        # Simulate the auto-freeze / lien step for high-confidence rings,
        # then simulate the bank/CFCFRMS side responding -- closes the loop
        # visually instead of leaving auto-freeze as just a ledger line.
        if alert["risk_score"] >= 0.8:
            ledger.add_block({
                "type": "AUTO_FREEZE",
                "ring_id": ring_id,
                "action": "Multi-bank temporary lien triggered via CFCFRMS (mock)",
            })
            bank_response = simulate_bank_response(ring_id, group["amount"].sum())
            alert["bank_response"] = bank_response
            ledger.add_block({
                "type": "BANK_RESPONSE",
                "ring_id": ring_id,
                "bank": bank_response["bank"],
                "reference_id": bank_response["reference_id"],
                "status": bank_response["status"],
                "amount_held": bank_response["amount_held"],
            })

        alerts.append(alert)

    return pd.DataFrame(alerts)


if __name__ == "__main__":
    from data_gen import generate_complaints
    from ring_detection import detect_rings

    complaints = generate_complaints(300)
    scored = detect_rings(complaints)
    ledger = AuditLedger()
    alerts = generate_alerts(scored, ledger, threshold=0.5)
    print(alerts)
    print("\nLedger blocks:", len(ledger.get_chain()))

"""
data_gen.py -- Owned by: Prachi

Produces the synthetic complaints DataFrame used by the whole prototype.

Schema (must not change column names):
    complaint_id (str), account_id (str), linked_account_id (str),
    timestamp (datetime), lat (float), lon (float), amount (float), city (str),
    crime_type (str)
"""

import random
import uuid
from datetime import datetime, timedelta

import pandas as pd

# Rough hotspot zones inside Chandigarh/Mohali/Panchkula tricity area.
# Replace with real-looking coordinates for whichever city you pick.
HOTSPOTS = [
    {"city": "Chandigarh Sec-17", "lat": 30.7410, "lon": 76.7822},
    {"city": "Mohali Phase-7", "lat": 30.7046, "lon": 76.7179},
    {"city": "Panchkula Sec-8", "lat": 30.6942, "lon": 76.8606},
    {"city": "Chandigarh Sec-35", "lat": 30.7268, "lon": 76.7692},
]


CRIME_TYPES = ["UPI Fraud", "Investment Scam", "OTP Fraud", "Loan App Fraud", "Job Fraud"]


def _jitter(value, spread=0.01):
    return value + random.uniform(-spread, spread)


def generate_complaints(n: int = 300) -> pd.DataFrame:
    """Generate n synthetic cybercrime complaints, clustered around HOTSPOTS,
    with ~20% of accounts sharing a linked_account_id to simulate mule rings.
    """
    random.seed(42)
    rows = []
    account_pool = [f"ACC{i:04d}" for i in range(1, int(n * 0.6))]

    # Pre-build a few "ring" groups of linked accounts (mule networks)
    ring_groups = []
    pool_copy = account_pool.copy()
    random.shuffle(pool_copy)
    idx = 0
    while idx < len(pool_copy) - 4 and len(ring_groups) < 12:
        size = random.randint(2, 4)
        ring_groups.append(pool_copy[idx: idx + size])
        idx += size

    base_time = datetime(2026, 8, 20, 9, 0, 0)

    for i in range(n):
        hotspot = random.choice(HOTSPOTS)
        account_id = random.choice(account_pool)

        # 20% chance this complaint's account belongs to a ring -> link it
        linked_account_id = ""
        for ring in ring_groups:
            if account_id in ring:
                others = [a for a in ring if a != account_id]
                if others:
                    linked_account_id = random.choice(others)
                break

        rows.append({
            "complaint_id": f"CMP{uuid.uuid4().hex[:8].upper()}",
            "account_id": account_id,
            "linked_account_id": linked_account_id,
            "timestamp": base_time + timedelta(minutes=random.randint(0, 60 * 24 * 10)),
            "lat": round(_jitter(hotspot["lat"]), 6),
            "lon": round(_jitter(hotspot["lon"]), 6),
            "amount": round(random.uniform(2000, 150000), 2),
            "city": hotspot["city"],
            "crime_type": random.choice(CRIME_TYPES),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_complaints(300)
    print(df.shape)
    print(df.head(10))
    print("\nAccounts with a linked_account_id (potential ring members):")
    print(df[df["linked_account_id"] != ""].shape[0])

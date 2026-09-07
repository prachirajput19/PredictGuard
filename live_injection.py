"""
live_injection.py -- Live "Simulate New Complaint" feature.

Lets a presenter type in a brand-new cybercrime complaint DURING the demo
and watch it flow live through the real pipeline: joins/creates a mule
ring via graph detection, gets risk-scored, may trigger a real alert +
notification attempt, and gets logged into the audit ledger -- all without
reloading the page. This is the strongest proof that the system is a live
pipeline, not a replay of precomputed results.
"""

import random
import uuid
from datetime import datetime

import streamlit as st

from data_gen import HOTSPOTS, CRIME_TYPES
from ring_detection import detect_rings


def render_live_injection_tab(get_complaints_df, set_complaints_df):
    """get_complaints_df() returns the current working DataFrame (session
    state). set_complaints_df(new_df) stores the updated DataFrame back so
    every other tab picks up the change on this same rerun."""

    st.markdown("### \U0001F9EA Live Signal Simulator")
    df = get_complaints_df()
    existing_accounts = sorted(df["account_id"].unique())
    city_names = [h["city"] for h in HOTSPOTS]

    with st.form("live_injection_form"):
        col1, col2 = st.columns(2)

        with col1:
            new_account = st.text_input(
                "New account ID (leave blank to auto-generate)", value="",
                placeholder="e.g. ACC9001",
            )
            link_choice = st.selectbox(
                "Link this complaint to an existing account? (simulates joining a ring)",
                options=["-- No link (isolated complaint) --"] + existing_accounts,
            )
            crime_type = st.selectbox("Crime type", options=CRIME_TYPES)

        with col2:
            city = st.selectbox("Location", options=city_names)
            amount = st.number_input(
                "Complaint amount (Rs)", min_value=1000.0, max_value=500000.0,
                value=50000.0, step=1000.0,
            )

        submitted = st.form_submit_button("\U0001F6A8 Inject Complaint Now", type="primary")

    if not submitted:
        return

    account_id = new_account.strip() or f"ACC{random.randint(9000, 9999)}"
    linked_account_id = "" if link_choice.startswith("--") else link_choice

    hotspot = next(h for h in HOTSPOTS if h["city"] == city)
    new_row = {
        "complaint_id": f"CMP{uuid.uuid4().hex[:8].upper()}",
        "account_id": account_id,
        "linked_account_id": linked_account_id,
        "timestamp": datetime.now(),
        "lat": hotspot["lat"] + random.uniform(-0.008, 0.008),
        "lon": hotspot["lon"] + random.uniform(-0.008, 0.008),
        "amount": float(amount),
        "city": city,
        "crime_type": crime_type,
    }

    # Append and re-run ring detection on the FULL updated dataset -- cheap
    # at this scale (a few hundred rows), and guarantees ring_id/risk stay
    # consistent with the rest of the app.
    with st.spinner("\U0001F9EA Injecting complaint into live pipeline -- running ring detection & risk scoring..."):
        updated_df = df.copy()
        updated_df.loc[len(updated_df)] = new_row
        updated_df = detect_rings(updated_df)
        set_complaints_df(updated_df)

    # Show immediate feedback about what just happened
    new_row_scored = updated_df[updated_df["complaint_id"] == new_row["complaint_id"]].iloc[0]
    ring_id = new_row_scored["ring_id"]
    risk_score = new_row_scored["ring_risk_score"]

    st.toast(f"Complaint {new_row['complaint_id']} injected live.", icon="\U0001F6A8")
    st.success(f"Complaint {new_row['complaint_id']} injected for account {account_id}.")
    st.session_state["last_injected_complaint_id"] = new_row["complaint_id"]
    st.session_state["last_injected_account_id"] = account_id

    if ring_id and not (risk_score != risk_score):  # not NaN
        st.toast(f"{ring_id} risk score updated to {risk_score:.2f}.", icon="\U0001F517")
        st.warning(
            f"\U0001F517 This account is now part of **{ring_id}** "
            f"with a computed risk score of **{risk_score:.2f}**. "
            f"Switch to **Network Intelligence** or **Predictive Hotspots** to see "
            f"it highlighted live, or **Priority Alerts** / **Audit & Evidence** to "
            f"see it flow through alerting and the ledger on the next threshold check."
        )
    else:
        st.info(
            "This complaint is not currently linked to any detected ring "
            "(risk score 0). Try linking it to an existing account above "
            "to simulate it joining a mule network."
        )

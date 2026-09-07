"""
lea_interface.py -- Owned by: Prerna Gupta

Deliverable (c): "Secure interface for investigators to access alerts,
intelligence reports, and evidence documentation."

Functions:
  - render_login(): login gate, returns True once authenticated
  - render_alerts_tab(alerts_df, complaints_df): alerts table, per-alert
    intelligence report, and evidence documentation with CSV export
  - render_audit_tab(ledger): blockchain-style audit ledger table
"""

import pandas as pd
import streamlit as st

import config
from ui_theme import get_severity_badge_html
from pdf_report import build_intelligence_report_pdf


def render_login() -> bool:
    """Simple session-based login gate. Returns True once authenticated.
    Demo-only credential check against config.LEA_CREDENTIALS -- production
    would use hashed passwords / SSO / I4C's identity provider."""
    if st.session_state.get("authenticated"):
        return True

    # Center-aligned SaaS login container
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="pg-fade-in d1" style="text-align: center; margin-bottom: 24px;">
                <div style="font-size: 4rem; font-weight: 800; color: #f8fafc; letter-spacing: 0.04em; font-family: 'Playfair Display', serif;
                            background: linear-gradient(90deg, #f8fafc 0%, #a78bfa 55%, #38bdf8 120%);
                            -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">
                     PREDICTGUARD
                </div>
                <div style="font-size: 0.78rem; color: #94a3b8; letter-spacing: 0.18em; text-transform: uppercase; margin-top: 4px; font-family: 'Space Grotesk', sans-serif;">
                    SEE THE FRAUD BEFORE IT MOVES
                </div>
                <div style="font-size: 0.85rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 10px;">
                    ● Secure Access
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
                    <span style="font-size: 0.85rem; font-weight: 700; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'Space Grotesk', sans-serif;">
                        Investigator Authentication
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            username = st.text_input("Investigator ID", placeholder="e.g. investigator1")
            password = st.text_input("Security Key / Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("INITIALIZE SESSION ➔", use_container_width=True)

        if submitted:
            if config.LEA_CREDENTIALS.get(username) == password:
                st.session_state.authenticated = True
                st.session_state.lea_username = username
                st.toast(f"Welcome back, {username}. Session authenticated.", icon="🔓")
                st.rerun()
            else:
                st.error("Authentication failed: Invalid Investigator ID or Security Key.")

        # Demo Credentials Box
        st.markdown(
            """
            <div class="pg-glass-card" style="margin-top: 18px; text-align: center;">
                <div style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; font-family: 'Space Grotesk', sans-serif;">
                    Demo Access Credentials
                </div>
                <div style="font-size: 0.82rem; color: #e2e8f0; font-family: monospace;">
                    ID: <b style="color: #38bdf8;">investigator1</b> &nbsp;|&nbsp; Key: <b style="color: #38bdf8;">1234</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return False


def _build_intelligence_report(alert_row, ring_complaints: pd.DataFrame) -> str:
    total_amount = ring_complaints["amount"].sum()
    account_count = ring_complaints["account_id"].nunique()
    crime_types = ring_complaints["crime_type"].value_counts().to_dict()
    date_min = ring_complaints["timestamp"].min()
    date_max = ring_complaints["timestamp"].max()

    breakdown_str = ", ".join([f"{k}: {v}" for k, v in crime_types.items()])

    report = f"""
### 📋 Operational Intelligence Dossier — {alert_row['ring_id']}

**1. TARGET & LOCATION SUMMARY**
- **Alert Reference ID:** `{alert_row['alert_id']}`
- **Predicted Withdrawal Location:** **{alert_row['predicted_location']}**
- **Forecast Window:** **{alert_row['predicted_time_window']}**
- **Syndicate Risk Assessment:** **{alert_row['risk_score']:.2f} ({int(alert_row['risk_score'] * 100)}% severity)**

---

**2. FINANCIAL ACCUMULATION & LINKED EXPOSURE**
- **Total Fraud Inflow Tracked:** **₹ {total_amount:,.2f}**
- **Syndicate Account Density:** **{account_count} distinct accounts**
- **Earliest Incident:** {date_min}
- **Latest Incident:** {date_max}

---

**3. CRIME CATEGORY DISPERSION**
{breakdown_str}

---

**4. ACTIONABLE TACTICAL RECOMMENDATION**
Deploy immediate field verification unit in sector **{alert_row['predicted_location']}** covering banking/ATM kiosks within the predicted time window (**{alert_row['predicted_time_window']}**). Cross-reference active linked account IDs against the CFCFRMS portal for concurrent multi-bank lien and temporary debit freeze prior to physical interception.

---

**5. PREDICTIVE EXPLAINABILITY**
This alert was autonomously generated because the detected syndicate graph exhibited high transaction frequency clustering, community cohesion across multiple complaints, and concentrated spatial-temporal withdrawal indicators above the assigned risk threshold.
"""
    return report


def render_alerts_tab(alerts_df: pd.DataFrame, complaints_df: pd.DataFrame):
    st.markdown(
        """
        <div class="pg-fade-in d1" style="display:flex; align-items:center; gap:10px;">
            <h3 style="margin:0;">🚨 Threat Signals</h3>
            <span class="pg-live-chip"><span class="pg-live-dot"></span>MONITORING</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if alerts_df.empty:
        st.info("No active alerts above the current risk threshold. Adjust sensitivity in the sidebar controls.")
        return

    if "alert_status" not in st.session_state:
        st.session_state.alert_status = {}

    # Status summary
    investigated_count = sum(1 for a in alerts_df["alert_id"] if st.session_state.alert_status.get(a) == "Investigated")
    pending_count = len(alerts_df) - investigated_count

    scol1, scol2, scol3 = st.columns(3)
    scol1.metric("Active High-Priority Alerts", len(alerts_df))
    scol2.metric("Pending Review", pending_count)
    scol3.metric("Investigated & Logged", investigated_count)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    for idx, (_, row) in enumerate(alerts_df.iterrows()):
        current_status = st.session_state.alert_status.get(row["alert_id"], row["status"])
        ring_complaints = complaints_df[complaints_df["ring_id"] == row["ring_id"]]
        badge_html = get_severity_badge_html(row["risk_score"])

        status_badge = (
            '<span class="saas-badge badge-verified">✓ INVESTIGATED</span>'
            if current_status == "Investigated"
            else '<span class="saas-badge badge-critical">● PENDING ACTION</span>'
        )
        card_class = "pg-glass-card critical" if row["risk_score"] >= 0.8 else "pg-glass-card"
        delay_class = f"d{min(idx % 6 + 1, 6)}"

        with st.container():
            st.markdown(
                f"""
                <div class="{card_class} pg-fade-in {delay_class}">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.1rem; font-weight: 800; color: #f8fafc;">{row['ring_id']}</span>
                            <span style="font-size: 0.8rem; color: #64748b; font-family: monospace;">ID: {row['alert_id']}</span>
                            {badge_html}
                        </div>
                        <div>{status_badge}</div>
                    </div>
                    <div style="display: flex; gap: 24px; font-size: 0.86rem; color: #cbd5e1; margin-top: 6px; flex-wrap: wrap;">
                        <div>📍 <b>Location:</b> {row['predicted_location']}</div>
                        <div>⏱️ <b>Window:</b> {row['predicted_time_window']}</div>
                        <div>⚡ <b>Risk Score:</b> <b style="color: #38bdf8;">{int(row['risk_score'] * 100)}%</b></div>
                        <div>👥 <b>Accounts:</b> {ring_complaints['account_id'].nunique()}</div>
                        <div>💰 <b>Total Exposure:</b> ₹ {ring_complaints['amount'].sum():,.2f}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            bank_response = row.get("bank_response")
            if bank_response:
                st.markdown(
                    f"""
                    <div style="background: #0c1f17; border: 1px solid #14532d; border-radius: 8px; padding: 12px 18px; margin-bottom: 12px;">
                        <div style="font-size: 0.78rem; font-weight: 700; color: #4ade80; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                            \U0001F3E6 Bank / CFCFRMS Response Received
                        </div>
                        <div style="display: flex; gap: 24px; font-size: 0.85rem; color: #cbd5e1; flex-wrap: wrap;">
                            <div><b>Bank:</b> {bank_response['bank']}</div>
                            <div><b>Reference:</b> <span style="font-family: monospace;">{bank_response['reference_id']}</span></div>
                            <div><b>Status:</b> {bank_response['status']}</div>
                            <div><b>Amount Held:</b> Rs {bank_response['amount_held']:,.2f}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            act_col1, act_col2 = st.columns([1, 4])
            with act_col1:
                if current_status == "New":
                    if st.button("Mark Investigated", key=f"btn_{row['alert_id']}", use_container_width=True):
                        st.session_state.alert_status[row["alert_id"]] = "Investigated"
                        st.toast(f"{row['ring_id']} marked as investigated.", icon="✅")
                        st.rerun()
                else:
                    st.button("✓ Completed", key=f"btn_{row['alert_id']}", disabled=True, use_container_width=True)

            with act_col2:
                with st.expander(f"Inspect Intelligence Dossier & Ground Evidence — {row['ring_id']}"):
                    report_tab, evidence_tab = st.tabs(["📄 Intelligence Dossier", "📁 Ground Evidence Records"])

                    with report_tab:
                        st.markdown(_build_intelligence_report(row, ring_complaints))

                    with evidence_tab:
                        st.caption(f"{len(ring_complaints)} linked complaint records for this mule network")
                        evidence_view = ring_complaints[
                            ["complaint_id", "account_id", "linked_account_id", "timestamp", "amount", "crime_type", "city"]
                        ]
                        st.dataframe(evidence_view, use_container_width=True)

                        dl_col1, dl_col2 = st.columns(2)
                        with dl_col1:
                            st.download_button(
                                "\U0001F4E5 Download Evidence as CSV",
                                data=evidence_view.to_csv(index=False),
                                file_name=f"evidence_{row['ring_id']}.csv",
                                mime="text/csv",
                                key=f"download_csv_{row['alert_id']}",
                                use_container_width=True,
                            )
                        with dl_col2:
                            pdf_bytes = build_intelligence_report_pdf(
                                row, ring_complaints,
                                st.session_state.get("lea_username", "unknown"),
                            )
                            st.download_button(
                                "\U0001F4C4 Download Intelligence Report (PDF)",
                                data=pdf_bytes,
                                file_name=f"intelligence_report_{row['ring_id']}.pdf",
                                mime="application/pdf",
                                key=f"download_pdf_{row['alert_id']}",
                                use_container_width=True,
                            )

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)


def render_audit_tab(ledger):
    st.markdown(
        """
        <div class="pg-fade-in d1" style="display:flex; align-items:center; gap:10px;">
            <h3 style="margin:0;">🔗 Immutable Evidence Vault</h3>
            <span class="pg-live-chip"><span class="pg-live-dot"></span>SECURED</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    chain = ledger.get_chain()
    if not chain:
        st.info("No ledger entries yet.")
        return

    # Cryptographic Status Panel
    tampered_idx = st.session_state.get("tampered_index")
    is_tampered = tampered_idx is not None

    status_color = "#f87171" if is_tampered else "#34d399"
    status_label = "TAMPERING SIMULATED" if is_tampered else "INTACT & VERIFIED"

    st.markdown(
        f"""
        <div class="pg-glass-card pg-fade-in d1" style="margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">LEDGER INTEGRITY STATUS</span>
                    <div style="font-size: 1.1rem; font-weight: 700; color: {status_color}; margin-top: 2px;">
                        ● {status_label}
                    </div>
                </div>
                <div style="text-align: right; font-size: 0.8rem; color: #cbd5e1;">
                    <div><b>Total Blocks:</b> {len(chain)}</div>
                    <div><b>Hashing Algorithm:</b> SHA-256 Merkle-Chain</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    verify_clicked = col1.button("Verify Chain Integrity", use_container_width=True)
    tamper_clicked = col2.button("Simulate Tampering (Demo)", type="secondary", use_container_width=True)

    if tamper_clicked and len(chain) > 1:
        target_index = max(1, len(chain) // 2)
        ledger.tamper_block(target_index, {"type": "ALERT", "ring_id": "FAKE_RING", "risk_score": 0.01})
        st.session_state["tampered_index"] = target_index
        st.toast(f"Block #{target_index} silently mutated.", icon="⚠️")
        st.warning(
            f"Simulated an attacker silently mutating Block #{target_index}'s "
            "data without recomputing subsequent hashes. Click 'Verify Chain Integrity' to see the audit trail catch it."
        )

    if verify_clicked:
        valid, bad_index = ledger.verify_chain()
        if valid:
            st.toast("Chain verified -- all blocks intact.", icon="✅")
            st.success("✅ Chain Verified: All blocks mathematically intact. No tampering or alteration detected.")
        else:
            st.toast(f"Tampering detected at Block #{bad_index}.", icon="🚨")
            st.error(
                f"🚨 TAMPERING DETECTED at Block #{bad_index}: Recomputed SHA-256 hash does "
                "not match stored block header! Chain cryptographic linkage is broken from this block onward."
            )

    # Clean formatted audit entries table
    rows = []
    for block in chain:
        evt = block["event"]
        evt_type = evt.get("type", "UNKNOWN")
        if evt_type == "ALERT":
            notifs = evt.get("notifications", [])
            notif_summary = " | ".join([f"{n.get('channel')}:{n.get('status')}" for n in notifs]) if notifs else "None"
            desc = f"Ring: {evt.get('ring_id')} (Risk: {evt.get('risk_score')}) | Notifs: [{notif_summary}]"
        elif evt_type == "AUTO_FREEZE":
            desc = f"Freeze: {evt.get('ring_id')} - {evt.get('action')}"
        elif evt_type == "BANK_RESPONSE":
            desc = (
                f"Bank Response: {evt.get('bank')} | Ref: {evt.get('reference_id')} | "
                f"{evt.get('status')} | Rs {evt.get('amount_held', 0):,.2f} held"
            )
        elif evt_type == "GENESIS":
            desc = f"Genesis Block: {evt.get('detail')}"
        else:
            desc = str(evt)

        flagged = " ⚠️ [TAMPERED]" if block["index"] == tampered_idx else ""
        rows.append({
            "Block #": block["index"],
            "Timestamp": block["timestamp"],
            "Event Type": evt_type,
            "Summary": desc + flagged,
            "Block Hash": block["hash"][:16] + "...",
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with st.expander("🔍 Inspect Full Cryptographic Block Payloads"):
        st.json(chain)

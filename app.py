import streamlit as st

from data_gen import generate_complaints          # Prachi
from ring_detection import detect_rings            # Prachi
from ledger import AuditLedger                      # Sehaj
from alert_engine import generate_alerts            # Sehaj
from dashboard import (
    configure_page,
    render_header,
    render_sidebar_brand,
    render_sidebar_nav,
    render_sidebar_threshold,
    render_map,
    render_command_center,
)  # Jeevan
from lea_interface import render_login, render_alerts_tab, render_audit_tab  # Prerna
from network_viz import render_network_tab  # mule-network graph visualization
from live_injection import render_live_injection_tab  # live "simulate new complaint" feature


def get_complaints_df():
    """Session-state working copy of the complaints dataset. Starts from
    the cached base dataset, but can grow via live injection -- every tab
    reads from THIS, not the raw generator, so injected complaints show up
    everywhere immediately."""
    if "complaints_df" not in st.session_state:
        base_df = generate_complaints(300)
        base_df = detect_rings(base_df)
        st.session_state.complaints_df = base_df
    return st.session_state.complaints_df


def set_complaints_df(new_df):
    st.session_state.complaints_df = new_df


def get_ledger():
    if "ledger" not in st.session_state:
        st.session_state.ledger = AuditLedger()
    return st.session_state.ledger


def main():
    configure_page()

    # Deliverable (c): secure LEA login gate -- nothing else renders until
    # the investigator authenticates.
    if not render_login():
        return

    render_header()

    render_sidebar_brand()
    active_page = render_sidebar_nav()
    threshold = render_sidebar_threshold(default=0.6)

    complaints_df = get_complaints_df()
    ledger = get_ledger()

    # Alerts are regenerated on threshold change but ledger persists in session.
    # Each alert also fires real email/SMS/API notification attempts (see
    # notifications.py) -- results are logged into the ledger automatically.
    alerts_df = generate_alerts(complaints_df, ledger, threshold=threshold)

    if active_page == "cmd":
        render_command_center(complaints_df, alerts_df)

    elif active_page == "map":
        render_map(complaints_df)

    elif active_page == "network":
        render_network_tab(complaints_df)

    elif active_page == "alerts":
        render_alerts_tab(alerts_df, complaints_df)

    elif active_page == "audit":
        render_audit_tab(ledger)

    elif active_page == "live":
        render_live_injection_tab(get_complaints_df, set_complaints_df)


if __name__ == "__main__":
    main()

import folium
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.neighbors import KernelDensity
from streamlit_folium import st_folium

from ui_theme import (
    apply_custom_css,
    render_brand_header,
    get_severity_badge_html,
    render_animated_kpi_card,
)

def configure_page():
    st.set_page_config(
        page_title="PredictGuard — Cybercrime Intelligence",
        layout="wide",
    )
    apply_custom_css()

def render_header():
    render_brand_header()


def render_sidebar_brand():
    with st.sidebar:
        st.markdown(
            """
            <div style="padding-bottom: 12px; margin-bottom: 14px; border-bottom: 1px solid rgba(139,92,246,0.2);">
                <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; letter-spacing: 0.02em; font-family: 'Playfair Display', serif;">
                    PREDICTGUARD
                </div>
                <div style="font-size: 0.68rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px; font-family: 'Playfair Display', serif;">
                    SEE THE FRAUD BEFORE IT MOVES
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# (key, label) pairs -- key is used internally in session_state / app.py routing,
# label is what's shown in the sidebar nav (keeps the same icons/text that used
# to live in the top st.tabs() call).
NAV_ITEMS = [
    ("cmd", "\U0001F4CA Command Center"),
    ("map", "\U0001F5FA\uFE0F Predictive Hotspots"),
    ("network", "\U0001F578\uFE0F Network Intelligence"),
    ("alerts", "\U0001F6A8 Priority Alerts"),
    ("audit", "\U0001F517 Audit & Evidence"),
    ("live", "\U0001F9EA Live Simulation"),
]


def render_sidebar_nav(default_key: str = "cmd") -> str:
    """Left-sidebar section navigation -- replaces the old top st.tabs() row.
    Returns the currently selected page's key (e.g. 'cmd', 'map', ...)."""
    with st.sidebar:
        st.markdown(
            "<div style='font-size: 0.72rem; font-weight: 700; color: #94a3b8; "
            "text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;'>"
            "Navigation</div>",
            unsafe_allow_html=True,
        )

        keys = [key for key, _label in NAV_ITEMS]
        labels = [label for _key, label in NAV_ITEMS]

        if "pg_active_page" not in st.session_state:
            st.session_state.pg_active_page = default_key

        current_index = keys.index(st.session_state.pg_active_page)
        selected_label = st.radio(
            "Navigation",
            options=labels,
            index=current_index,
            label_visibility="collapsed",
            key="pg_nav_radio",
        )
        st.session_state.pg_active_page = keys[labels.index(selected_label)]

        st.markdown(
            "<div style='margin: 14px 0; border-bottom: 1px solid rgba(139,92,246,0.15);'></div>",
            unsafe_allow_html=True,
        )

    return st.session_state.pg_active_page


def render_sidebar_threshold(default: float = 0.6) -> float:
    with st.sidebar:
        # Status & User Badges
        investigator = st.session_state.get("lea_username", "investigator1")
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f293d; border-radius: 6px; padding: 10px 12px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-size: 0.7rem; color: #64748b; font-weight: 600;">SYSTEM STATUS</span>
                    <span style="font-size: 0.68rem; background: rgba(16,185,129,0.15); color: #34d399; padding: 2px 8px; border-radius: 4px; font-weight: 700; border: 1px solid rgba(16,185,129,0.3); display: inline-flex; align-items: center;">
                        <span class="pg-live-dot" style="margin-right: 5px;"></span>OPERATIONAL
                    </span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 6px;">
                    <span style="font-size: 0.8rem; color: #cbd5e1;">👤</span>
                    <span style="font-size: 0.78rem; font-weight: 600; color: #e2e8f0;">{investigator}</span>
                    <span style="font-size: 0.68rem; color: #64748b; margin-left: auto;">LEA Session</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;'>System Controls</div>",
            unsafe_allow_html=True,
        )
        threshold = st.slider(
            "Alerting Risk Threshold",
            min_value=0.0,
            max_value=1.0,
            value=default,
            step=0.05,
            help="Rings with risk score at or above this threshold trigger real-time alerts.",
        )
        st.caption(f"Sensitivity: **{int(threshold * 100)}%** minimum risk to flag")
    return threshold


def compute_kde_hotspots(df, grid_resolution: int = 45, bandwidth: float = 0.008):
    """Fit a Kernel Density Estimate over complaint locations, weighted by
    ring_risk_score, and evaluate it on a grid. This is the actual
    'predicted withdrawal hotspot' surface -- not just a replay of raw
    complaint points -- which is what the problem statement asks for.

    Returns a list of [lat, lon, weight] usable directly by folium's HeatMap.
    """
    coords = df[["lat", "lon"]].to_numpy()
    weights = df["ring_risk_score"].fillna(0.05).clip(lower=0.05).to_numpy()

    kde = KernelDensity(bandwidth=bandwidth, kernel="gaussian")
    kde.fit(coords, sample_weight=weights)

    lat_min, lat_max = coords[:, 0].min(), coords[:, 0].max()
    lon_min, lon_max = coords[:, 1].min(), coords[:, 1].max()
    # small padding so the surface doesn't clip exactly at the data edge
    pad_lat = (lat_max - lat_min) * 0.1 or 0.01
    pad_lon = (lon_max - lon_min) * 0.1 or 0.01

    lat_grid = np.linspace(lat_min - pad_lat, lat_max + pad_lat, grid_resolution)
    lon_grid = np.linspace(lon_min - pad_lon, lon_max + pad_lon, grid_resolution)
    grid_points = np.array([[la, lo] for la in lat_grid for lo in lon_grid])

    log_density = kde.score_samples(grid_points)
    density = np.exp(log_density)
    density_norm = (density - density.min()) / (density.max() - density.min() + 1e-9)

    heat_data = [
        [float(grid_points[i][0]), float(grid_points[i][1]), float(density_norm[i])]
        for i in range(len(grid_points))
        if density_norm[i] > 0.08  # drop near-zero noise for a cleaner surface
    ]
    return heat_data


def render_command_center(complaints_df, alerts_df):
    """Deliverable Overview: Executive SaaS command center summarizing active alerts,
    detected rings, spatial hotspots, and financial risk exposure from real data.
    """
    st.markdown(
        """
        <div class="pg-fade-in d1" style="display:flex; align-items:center; gap:10px;">
            <h3 style="margin:0;">📊 Threat Intelligence Overview</h3>
            <span class="pg-live-chip"><span class="pg-live-dot"></span>LIVE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # 4 SaaS KPI Cards derived strictly from real project data
    total_complaints = len(complaints_df)
    active_alerts = len(alerts_df)
    high_risk_rings = alerts_df[alerts_df["risk_score"] >= 0.7]["ring_id"].nunique() if not alerts_df.empty else 0
    monitored_hotspots = complaints_df["city"].nunique()

    # Financial exposure: total complaint amounts tied to actively flagged rings
    if not alerts_df.empty:
        alerted_rings = alerts_df["ring_id"].unique()
        risk_exposure = complaints_df[complaints_df["ring_id"].isin(alerted_rings)]["amount"].sum()
    else:
        risk_exposure = 0.0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        render_animated_kpi_card(
            "Active Mule Alerts", active_alerts,
            subtitle="Rings flagged above current risk threshold",
            accent="#38bdf8", delay_ms=0,
        )
    with kpi2:
        render_animated_kpi_card(
            "High-Risk Rings (≥70%)", high_risk_rings,
            subtitle="Mule rings with severe coordination score",
            accent="#fb923c", delay_ms=80,
        )
    with kpi3:
        render_animated_kpi_card(
            "Monitored Hotspots", monitored_hotspots,
            subtitle="Clustered urban sectors under spatial observation",
            accent="#8B5CF6", delay_ms=160,
        )
    with kpi4:
        render_animated_kpi_card(
            "Risk Exposure", risk_exposure,
            subtitle="Total illicit complaint value linked to active rings",
            prefix="₹ ", decimals=2, accent="#34d399", delay_ms=240,
        )

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    # Trend charts: crime-type breakdown + complaints over time
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### \U0001F4CA Crime Category Breakdown")
        crime_counts = complaints_df["crime_type"].value_counts()
        bar_fig = go.Figure(go.Bar(
            x=crime_counts.values, y=crime_counts.index, orientation="h",
            marker=dict(color="#38bdf8"),
        ))
        bar_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10), height=260,
            font=dict(color="#cbd5e1", size=11, family="DM Sans, sans-serif"),
            xaxis=dict(gridcolor="rgba(139,92,246,0.15)"), yaxis=dict(gridcolor="rgba(139,92,246,0.15)"),
            transition={"duration": 500, "easing": "cubic-in-out"},
        )
        st.plotly_chart(bar_fig, use_container_width=True, config={"displaylogo": False})

    with chart_col2:
        st.markdown("#### \U0001F4C8 Complaint Volume Over Time")
        daily_counts = complaints_df.set_index("timestamp").resample("D").size()
        line_fig = go.Figure(go.Scatter(
            x=daily_counts.index, y=daily_counts.values, mode="lines",
            line=dict(color="#38bdf8", width=2), fill="tozeroy",
            fillcolor="rgba(56, 189, 248, 0.15)",
        ))
        line_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10), height=260,
            font=dict(color="#cbd5e1", size=11, family="DM Sans, sans-serif"),
            xaxis=dict(gridcolor="rgba(139,92,246,0.15)"), yaxis=dict(gridcolor="rgba(139,92,246,0.15)"),
            transition={"duration": 500, "easing": "cubic-in-out"},
        )
        st.plotly_chart(line_fig, use_container_width=True, config={"displaylogo": False})

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    # Priority Alerts Snapshot
    st.markdown("#### 🚨 Immediate Action Required (Priority Alerts)")
    if alerts_df.empty:
        st.info("No active alerts at the current threshold sensitivity. Lower the threshold in the sidebar to view lower-risk clusters.")
    else:
        top_alerts = alerts_df.sort_values(by="risk_score", ascending=False).head(3)
        for i, (_, alert) in enumerate(top_alerts.iterrows()):
            badge_html = get_severity_badge_html(alert["risk_score"])
            status_text = st.session_state.get("alert_status", {}).get(alert["alert_id"], alert["status"])
            status_color = "#34d399" if status_text == "Investigated" else "#f87171"
            status_badge = f"<span style='color: {status_color}; font-weight: 700; font-size: 0.75rem;'>● {status_text.upper()}</span>"
            card_class = "pg-glass-card critical" if alert["risk_score"] >= 0.8 else "pg-glass-card"
            delay_class = f"d{min(i + 1, 6)}"

            st.markdown(
                f"""
                <div class="{card_class} pg-fade-in {delay_class}">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                        <div>
                            <span style="font-weight: 700; font-size: 1rem; color: #f8fafc; margin-right: 8px;">{alert['ring_id']}</span>
                            <span style="color: #64748b; font-size: 0.8rem; font-family: monospace;">({alert['alert_id']})</span>
                            &nbsp; {badge_html}
                        </div>
                        <div>{status_badge}</div>
                    </div>
                    <div style="display: flex; gap: 24px; font-size: 0.85rem; color: #cbd5e1; margin-top: 8px; flex-wrap: wrap;">
                        <div>📍 <b>Target Location:</b> {alert['predicted_location']}</div>
                        <div>⏱️ <b>Forecast Window:</b> {alert['predicted_time_window']}</div>
                        <div>⚡ <b>Risk Score:</b> <span style="color: #38bdf8; font-weight: 700;">{int(alert['risk_score'] * 100)}%</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_map(df):
    """df must have lat, lon, ring_risk_score, city, crime_type, timestamp
    columns. Renders drill-down filters (crime category + time range) plus
    TWO toggleable map layers: raw complaint points, and the KDE-predicted
    risk surface (the actual 'forecast' the PS asks for).
    """
    st.markdown("### 🗺️ Predictive Hotspot Analysis — Cash-Withdrawal Risk Surface")
    if df.empty:
        st.info("No complaint data available yet.")
        return

    # --- Drill-down filters (crime category + location + time range) ---
    filt_col1, filt_col2, filt_col3 = st.columns([1, 1, 2])

    with filt_col1:
        all_categories = sorted(df["crime_type"].unique())
        selected_categories = st.multiselect(
            "Filter by crime category", options=all_categories, default=all_categories,
        )

    with filt_col2:
        all_locations = sorted(df["city"].unique())
        selected_locations = st.multiselect(
            "Filter by location", options=all_locations, default=all_locations,
        )

    with filt_col3:
        min_date = df["timestamp"].min().date()
        max_date = df["timestamp"].max().date()
        if min_date == max_date:
            st.caption(f"All complaints fall on {min_date}")
            date_range = (min_date, max_date)
        else:
            date_range = st.slider(
                "Filter by time range", min_value=min_date, max_value=max_date,
                value=(min_date, max_date),
            )

    filtered_df = df[
        df["crime_type"].isin(selected_categories)
        & df["city"].isin(selected_locations)
        & (df["timestamp"].dt.date >= date_range[0])
        & (df["timestamp"].dt.date <= date_range[1])
    ]

    # Map Telemetry Chips
    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        stat1.metric("Active Filtered Records", f"{len(filtered_df)} / {len(df)}")
    with stat2:
        stat2.metric("Active Sectors", f"{filtered_df['city'].nunique()}")
    with stat3:
        high_risk_pts = len(filtered_df[filtered_df.get("ring_risk_score", 0) >= 0.6])
        stat3.metric("High-Risk Points (≥0.6)", f"{high_risk_pts}")

    if filtered_df.empty:
        st.warning("No complaints match the current filters.")
        return

    center_lat = filtered_df["lat"].mean()
    center_lon = filtered_df["lon"].mean()
    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

    # --- Layer 1: predicted risk surface (KDE) ---
    heat_data = compute_kde_hotspots(filtered_df)
    heat_layer = folium.FeatureGroup(name="Predicted Risk Hotspots (KDE)", show=True)
    # Circle markers avoid the heatmap canvas plugin, which can receive a
    # zero-sized canvas when Streamlit initially renders this tab hidden.
    for latitude, longitude, intensity in heat_data:
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=3 + (12 * intensity),
            color="#38bdf8",
            fill=True,
            fill_color="#8B5CF6",
            fill_opacity=0.18 + (0.62 * intensity),
            weight=1,
        ).add_to(heat_layer)
    heat_layer.add_to(fmap)

    # --- Layer 2: raw complaint points (ground truth data) ---
    points_layer = folium.FeatureGroup(name="Raw Complaint Points", show=False)
    last_injected_id = st.session_state.get("last_injected_complaint_id")
    for _, row in filtered_df.iterrows():
        score = row.get("ring_risk_score", 0) or 0
        is_new = last_injected_id is not None and row.get("complaint_id") == last_injected_id

        if is_new:
            color = "#facc15"  # gold highlight for the just-injected complaint
            radius = 11
        elif score >= 0.6:
            color = "red"
            radius = 5
        elif score >= 0.3:
            color = "orange"
            radius = 5
        else:
            color = "green"
            radius = 5

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            color=color,
            fill=True,
            fill_opacity=0.9 if is_new else 0.7,
            popup=(
                ("\U0001F195 Just injected via Live Simulation<br>" if is_new else "")
                + f"Account: {row['account_id']}<br>"
                f"Crime type: {row['crime_type']}<br>"
                f"Risk: {score}"
            ),
        ).add_to(points_layer)
    points_layer.add_to(fmap)

    if last_injected_id is not None and last_injected_id in filtered_df["complaint_id"].values:
        st.caption("\U0001F195 Gold marker on **Raw Complaint Points** layer = complaint just injected via Live Simulation.")

    folium.LayerControl(collapsed=False).add_to(fmap)

    st_folium(fmap, width=1100, height=520)

if __name__ == "__main__":
    # Standalone smoke test with dummy data
    import pandas as pd

    configure_page()
    render_header()
    threshold = render_sidebar_threshold()
    dummy_df = pd.DataFrame({
        "account_id": ["ACC0001", "ACC0002"],
        "lat": [30.741, 30.705],
        "lon": [76.782, 76.718],
        "ring_risk_score": [0.8, 0.2],
    })
    render_map(dummy_df)

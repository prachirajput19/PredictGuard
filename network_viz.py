"""
network_viz.py -- Mule-account network graph visualization.

This makes the graph-based ring detection VISIBLE, instead of it being an
invisible step that only shows up as colored map dots. Renders the actual
node-edge structure: nodes = accounts, edges = linked-account relationships,
colored by ring_id, sized by ring_risk_score.

Uses Plotly (not static matplotlib) so the graph is hoverable, zoomable,
and pannable during the live demo.
"""

import networkx as nx
import plotly.graph_objects as go
import streamlit as st


def build_ring_graph(df):
    """Build a networkx graph restricted to accounts that belong to a
    detected ring (unlinked/isolated accounts are dropped -- they'd just be
    visual noise and aren't part of any mule network)."""
    ring_df = df[df["ring_id"].notna()].copy()

    G = nx.Graph()
    for _, row in ring_df.iterrows():
        G.add_node(row["account_id"], ring_id=row["ring_id"], risk=row["ring_risk_score"])
        if row["linked_account_id"]:
            G.add_node(row["linked_account_id"], ring_id=row["ring_id"], risk=row["ring_risk_score"])
            G.add_edge(row["account_id"], row["linked_account_id"])

    return G


def _build_plotly_figure(G, highlight_account=None):
    palette = [
        "#8B5CF6", "#38bdf8", "#fb923c", "#34d399", "#f87171",
        "#a78bfa", "#f472b6", "#fbbf24", "#60a5fa", "#4ade80",
        "#2dd4bf", "#e879f9", "#facc15", "#818cf8", "#fb7185",
        "#22d3ee", "#c084fc", "#a3e635", "#94a3b8", "#f43f5e", "#0ea5e9",
    ]
    ring_ids = list({G.nodes[n]["ring_id"] for n in G.nodes})
    ring_color = {rid: palette[i % len(palette)] for i, rid in enumerate(ring_ids)}

    pos = nx.spring_layout(G, seed=42, k=0.6)

    # Edge trace: one continuous line with None separators between segments
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1.2, color="#475569"),
        hoverinfo="none", showlegend=False,
    )

    node_x, node_y, node_text, node_hover, node_color, node_size, node_line_color, node_line_width = (
        [], [], [], [], [], [], [], []
    )
    for n in G.nodes():
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        ring_id = G.nodes[n]["ring_id"]
        risk = G.nodes[n]["risk"]
        is_new = highlight_account is not None and n == highlight_account
        node_text.append(("\U0001F195 " if is_new else "") + n)
        node_hover.append(
            f"Account: {n}<br>Ring: {ring_id}<br>Risk score: {risk:.2f}"
            + ("<br><b>Just injected via Live Simulation</b>" if is_new else "")
        )
        node_color.append("#facc15" if is_new else ring_color[ring_id])
        node_size.append((28 + 32 * risk) if is_new else (18 + 32 * risk))
        node_line_color.append("#facc15" if is_new else "#0f172a")
        node_line_width.append(3 if is_new else 1.5)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_text, textposition="top center",
        textfont=dict(size=10, color="#f8fafc", family="DM Sans, sans-serif"),
        hovertext=node_hover, hoverinfo="text",
        marker=dict(
            size=node_size, color=node_color,
            line=dict(width=node_line_width, color=node_line_color),
        ),
        showlegend=False,
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode="closest",
        height=520,
    )
    return fig


def render_network_tab(df):
    st.subheader("\U0001F578 Mule Network Constellation")
    G = build_ring_graph(df)

    if G.number_of_nodes() == 0:
        st.info("No linked-account rings detected in the current dataset.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Flagged Accounts", G.number_of_nodes(), help="Accounts confirmed in coordinated mule activity")
    col2.metric("Linked Pairs", G.number_of_edges(), help="Direct financial routing links identified between accounts")
    col3.metric("Distinct Rings", df["ring_id"].nunique(), help="Independent syndicates detected via Louvain community partitioning")

    fig = _build_plotly_figure(G, highlight_account=st.session_state.get("last_injected_account_id"))
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

    if st.session_state.get("last_injected_account_id") in G.nodes:
        st.caption("\U0001F195 Gold-highlighted node = account just injected via Live Simulation.")

    st.markdown("---")

    # Professional Ring Deep-Dive Inspector
    st.markdown("#### \U0001F50D Selected Ring Deep-Dive Inspector")
    ring_options = sorted([r for r in df["ring_id"].dropna().unique()])
    if ring_options:
        sel_ring = st.selectbox("Select ring to inspect:", options=ring_options, key="net_ring_select")
        ring_complaints = df[df["ring_id"] == sel_ring]
        ring_accounts = sorted(list(set(
            ring_complaints["account_id"].dropna().tolist() +
            [a for a in ring_complaints["linked_account_id"].dropna().tolist() if a]
        )))
        ring_risk = float(ring_complaints["ring_risk_score"].iloc[0]) if not ring_complaints.empty else 0.0
        ring_total = float(ring_complaints["amount"].sum()) if not ring_complaints.empty else 0.0

        rcol1, rcol2, rcol3, rcol4 = st.columns(4)
        with rcol1:
            rcol1.metric("Ring ID", sel_ring)
        with rcol2:
            rcol2.metric("Syndicate Risk", f"{int(ring_risk * 100)}%")
        with rcol3:
            rcol3.metric("Member Accounts", f"{len(ring_accounts)}")
        with rcol4:
            rcol4.metric("Linked Exposure", f"\u20b9 {ring_total:,.2f}")

        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f293d; border-radius: 6px; padding: 10px 14px; margin-top: 8px; font-size: 0.85rem;">
                <span style="color: #94a3b8; font-weight: 600;">Affiliated Account Nodes:</span>
                <span style="color: #38bdf8; font-family: monospace; font-weight: 600; margin-left: 8px;">
                    {', '.join(ring_accounts)}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

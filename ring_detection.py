"""
ring_detection.py -- Owned by: Prachi

Builds a graph from account_id <-> linked_account_id and runs community
detection to flag "mule rings". Adds ring_id and ring_risk_score columns.

Input: complaints DataFrame from data_gen.generate_complaints()
Output: same DataFrame + ring_id (str or None), ring_risk_score (float 0-1)
"""

import networkx as nx
import pandas as pd

try:
    import community as community_louvain  # python-louvain package
except ImportError:
    community_louvain = None


def detect_rings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row["account_id"])
        if row["linked_account_id"]:
            G.add_node(row["linked_account_id"])
            G.add_edge(row["account_id"], row["linked_account_id"])

    if community_louvain is not None and G.number_of_edges() > 0:
        partition = community_louvain.best_partition(G)
    else:
        # Fallback: connected components as "communities" if louvain unavailable
        partition = {}
        for i, comp in enumerate(nx.connected_components(G)):
            for node in comp:
                partition[node] = i

    # Only treat groups of size >= 2 as an actual "ring"
    from collections import Counter
    community_sizes = Counter(partition.values())

    account_to_ring = {}
    for account, comm_id in partition.items():
        if community_sizes[comm_id] >= 2:
            account_to_ring[account] = f"RING{comm_id:03d}"

    df["ring_id"] = df["account_id"].map(account_to_ring)

    # Risk score: normalized by ring size and complaint frequency within ring
    ring_txn_counts = df.groupby("ring_id")["complaint_id"].count()
    max_count = ring_txn_counts.max() if len(ring_txn_counts) else 1

    def score_row(ring_id):
        if pd.isna(ring_id):
            return 0.0
        count = ring_txn_counts.get(ring_id, 0)
        return round(min(count / max_count, 1.0), 3)

    df["ring_risk_score"] = df["ring_id"].apply(score_row)

    return df


if __name__ == "__main__":
    from data_gen import generate_complaints

    complaints = generate_complaints(300)
    scored = detect_rings(complaints)
    print(scored[scored["ring_id"].notna()][
        ["account_id", "linked_account_id", "ring_id", "ring_risk_score"]
    ].drop_duplicates().head(20))

"""
Origin Propagation Graph Builder.

Constructs directed acyclic graphs (DAGs) representing how a piece of media
propagated across the open indexable web.

Nodes: Indexed public instances (News sites, X posts, public Telegram channels).
Edges: Inferred transformations (ORIGINAL -> REPOST -> SCREENSHOT -> CROP -> VIRAL FORWARD).
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime


def build_propagation_graph(
    candidates: List[Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """
    Constructs the propagation graph and identifies the Earliest Indexed Source.

    Returns:
        (graph_structure, summary_metrics, explanation)
    """
    if not candidates:
        return (
            {"nodes": [], "edges": []},
            {"propagation_count": 0, "earliest_source": None},
            "No prior public web instances found. (Media may be newly generated or shared exclusively in private groups)."
        )

    # Sort candidates chronologically by platform timestamp
    def parse_time(c):
        try:
            return datetime.fromisoformat(c["platform_timestamp"].replace("Z", "+00:00"))
        except Exception:
            return datetime.max

    sorted_candidates = sorted(candidates, key=parse_time)
    earliest = sorted_candidates[0]

    # Build node-link graph data (compatible with React Flow / vis-network)
    nodes = []
    edges = []

    for i, c in enumerate(sorted_candidates):
        node_id = f"node_{i+1}"
        is_earliest = (i == 0)
        nodes.append({
            "id": node_id,
            "label": f"{c['platform']}\n({c['account_name']})",
            "url": c["source_url"],
            "platform": c["platform"],
            "timestamp": c["platform_timestamp"],
            "is_earliest": is_earliest,
            "similarity": c.get("clip_similarity", 0.95),
            "type": "earliest" if is_earliest else "derivative",
        })

        if i > 0:
            edges.append({
                "id": f"edge_{i}",
                "source": f"node_{i}",
                "target": node_id,
                "label": c.get("transformation", "REPOST"),
                "similarity": c.get("clip_similarity", 0.95),
            })

    # Confidence estimation for earliest source
    # Higher if timestamp is cryptographically verified or on trusted CDN
    source_conf = 0.90 if earliest.get("timestamp_verified") else 0.75

    summary_metrics = {
        "earliest_source": {
            "platform": earliest["platform"],
            "account": earliest["account_name"],
            "url": earliest["source_url"],
            "timestamp": earliest["platform_timestamp"],
            "source_confidence": source_conf,
        },
        "derivative_count": len(sorted_candidates) - 1,
        "total_instances_found": len(sorted_candidates),
        "propagation_velocity": f"{len(sorted_candidates)} posts across {len(set(c['platform'] for c in sorted_candidates))} platforms",
    }

    explanation = (
        f"Earliest Indexed Source: {earliest['platform']} ({earliest['account_name']}) "
        f"at {earliest['platform_timestamp']} (Source Confidence: {round(source_conf * 100)}%). "
        f"Tracked across {len(sorted_candidates)} derivative hops."
    )

    graph_structure = {"nodes": nodes, "edges": edges}

    return graph_structure, summary_metrics, explanation

from typing import List
from agent.state import CodeResult


def format_results_table(results: List[CodeResult]) -> str:
    """Format code results as a readable text table."""
    if not results:
        return "No results found."

    lines = []
    current_system = None
    for r in results:
        if r["system"] != current_system:
            current_system = r["system"]
            lines.append(f"\n{'='*60}")
            lines.append(f"  {current_system}")
            lines.append(f"{'='*60}")
        meta = ""
        if r["metadata"]:
            meta_parts = [f"{k}: {v}" for k, v in r["metadata"].items() if v]
            if meta_parts:
                meta = f"  [{', '.join(meta_parts)}]"
        lines.append(f"  {r['code']:<15} {r['display']}{meta}")
    return "\n".join(lines)


def format_results_json(results: List[CodeResult]) -> dict:
    """Group results by coding system for JSON output."""
    grouped = {}
    for r in results:
        sys = r["system"]
        if sys not in grouped:
            grouped[sys] = []
        grouped[sys].append({
            "code": r["code"],
            "display": r["display"],
            "metadata": r["metadata"]
        })
    return grouped

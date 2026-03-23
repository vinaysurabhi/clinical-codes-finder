from typing import List, dict as Dict
from agent.state import CodeResult


def deduplicate_results(raw_results: List[dict]) -> List[CodeResult]:
    """
    Normalize and deduplicate raw API results.
    Deduplication key: (system, code)
    """
    seen = set()
    unique = []
    for item in raw_results:
        system = item.get("system", "Unknown")
        code = item.get("code", "").strip()
        if not code:
            continue
        key = (system, code)
        if key not in seen:
            seen.add(key)
            unique.append(CodeResult(
                system=system,
                code=code,
                display=item.get("display", code),
                metadata=item.get("metadata", {})
            ))
    # Sort by system then code for consistent output
    unique.sort(key=lambda x: (x["system"], x["code"]))
    return unique

import os
from typing import List
from .clinical_tables import query_clinical_tables


class HCPCSTool:
    """Tool to search HCPCS codes for procedures, supplies, equipment."""
    SYSTEM = "HCPCS"
    ENDPOINT = "hcpcs/v3/search"

    def search(self, term: str) -> List[dict]:
        max_results = int(os.getenv("MAX_RESULTS_PER_SYSTEM", 5))
        raw = query_clinical_tables(
            self.ENDPOINT, term, max_results=max_results,
            extra_params={"df": "HCPC,LONG_DESCRIPTION,SHORT_DESCRIPTION"}
        )
        return self._parse(raw)

    def _parse(self, raw) -> List[dict]:
        results = []
        if not raw or len(raw) < 4:
            return results
        codes = raw[1] or []
        displays = raw[3] or []
        for i, code in enumerate(codes):
            row = displays[i] if displays and i < len(displays) else []
            display = row[1] if len(row) > 1 else (row[2] if len(row) > 2 else code)
            metadata = {}
            if len(row) > 2:
                metadata["short_description"] = row[2]
            results.append({
                "system": self.SYSTEM,
                "code": code,
                "display": display,
                "metadata": metadata
            })
        return results

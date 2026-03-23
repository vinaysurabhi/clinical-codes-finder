import os
from typing import List
from .clinical_tables import query_clinical_tables


class HPOTool:
    """Tool to search HPO phenotypic features and clinical symptoms."""
    SYSTEM = "HPO"
    ENDPOINT = "hpo/v3/search"

    def search(self, term: str) -> List[dict]:
        max_results = int(os.getenv("MAX_RESULTS_PER_SYSTEM", 5))
        raw = query_clinical_tables(
            self.ENDPOINT, term, max_results=max_results,
            extra_params={"df": "id,name,definition"}
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
            display = row[1] if len(row) > 1 else code
            metadata = {}
            if len(row) > 2 and row[2]:
                metadata["definition"] = row[2][:200]
            results.append({
                "system": self.SYSTEM,
                "code": code,
                "display": display,
                "metadata": metadata
            })
        return results

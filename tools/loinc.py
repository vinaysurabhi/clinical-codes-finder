import os
from typing import List
from .clinical_tables import query_clinical_tables


class LOINCTool:
    """Tool to search LOINC codes for lab tests and observations."""
    SYSTEM = "LOINC"
    ENDPOINT = "loinc/v3/search"

    def search(self, term: str) -> List[dict]:
        max_results = int(os.getenv("MAX_RESULTS_PER_SYSTEM", 5))
        raw = query_clinical_tables(
            self.ENDPOINT, term, max_results=max_results,
            extra_params={"df": "LOINC_NUM,LONG_COMMON_NAME,COMPONENT,SYSTEM"}
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
            if len(row) > 2:
                metadata["component"] = row[2]
            if len(row) > 3:
                metadata["system"] = row[3]
            results.append({
                "system": self.SYSTEM,
                "code": code,
                "display": display,
                "metadata": metadata
            })
        return results

import os
from typing import List
from .clinical_tables import query_clinical_tables


class ICD10CMTool:
    """Tool to search ICD-10-CM diagnosis codes."""
    SYSTEM = "ICD-10-CM"
    ENDPOINT = "icd10cm/v3/search"

    def search(self, term: str) -> List[dict]:
        max_results = int(os.getenv("MAX_RESULTS_PER_SYSTEM", 5))
        raw = query_clinical_tables(self.ENDPOINT, term, max_results=max_results)
        return self._parse(raw)

    def _parse(self, raw) -> List[dict]:
        """
        NLM API returns: [total, [codes], null, [display_fields]]
        icd10cm: display field is [code, name]
        """
        results = []
        if not raw or len(raw) < 4:
            return results
        codes = raw[1] or []
        displays = raw[3] or []
        for i, code in enumerate(codes):
            display = displays[i][1] if displays and i < len(displays) and displays[i] else code
            results.append({
                "system": self.SYSTEM,
                "code": code,
                "display": display,
                "metadata": {}
            })
        return results

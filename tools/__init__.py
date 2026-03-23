from .icd10cm import ICD10CMTool
from .loinc import LOINCTool
from .rxterms import RxTermsTool
from .hcpcs import HCPCSTool
from .ucum import UCUMTool
from .hpo import HPOTool

_TOOL_REGISTRY = {
    "ICD-10-CM": ICD10CMTool(),
    "LOINC": LOINCTool(),
    "RxTerms": RxTermsTool(),
    "HCPCS": HCPCSTool(),
    "UCUM": UCUMTool(),
    "HPO": HPOTool(),
}


def get_tool_for_system(system: str):
    """Return the tool instance for a given coding system name."""
    # Flexible matching
    system_upper = system.upper()
    for key, tool in _TOOL_REGISTRY.items():
        if key.upper() in system_upper or system_upper in key.upper():
            return tool
    return None


__all__ = [
    "ICD10CMTool", "LOINCTool", "RxTermsTool",
    "HCPCSTool", "UCUMTool", "HPOTool", "get_tool_for_system"
]

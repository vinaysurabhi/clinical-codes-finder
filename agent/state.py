from typing import TypedDict, Annotated, List, Optional
from operator import add


class CodeResult(TypedDict):
    system: str
    code: str
    display: str
    metadata: Optional[dict]


class AgentState(TypedDict):
    query: str
    planned_systems: List[str]
    search_terms: dict
    raw_results: Annotated[List[dict], add]
    code_results: List[CodeResult]
    reasoning: Annotated[List[str], add]
    summary: str
    iterations: int
    finished: bool

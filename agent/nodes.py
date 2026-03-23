import json
import logging
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentState
from .prompts import PLANNER_SYSTEM_PROMPT, SUMMARIZER_SYSTEM_PROMPT, REFINER_SYSTEM_PROMPT
from tools import get_tool_for_system

logger = logging.getLogger(__name__)


def make_llm(model: str = "gpt-4o-mini") -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=0)


def planner_node(state: AgentState) -> dict:
    """LLM decides which coding systems to query and with what terms."""
    llm = make_llm()
    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=f'Clinical query: "{state["query"]}"')
    ]
    response = llm.invoke(messages)
    content = response.content.strip()

    # Strip markdown code blocks if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3].strip()
        elif "```" in content:
            content = content[:content.rfind("```")].strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        logger.warning("Planner returned non-JSON; using fallback.")
        parsed = {
            "relevant_systems": ["ICD-10-CM"],
            "search_terms": {"ICD-10-CM": state["query"]},
            "reasoning": "Fallback: defaulting to ICD-10-CM"
        }

    reasoning_entry = f"[Planner] {parsed.get('reasoning', '')}"
    return {
        "planned_systems": parsed.get("relevant_systems", []),
        "search_terms": parsed.get("search_terms", {}),
        "reasoning": [reasoning_entry],
        "iterations": state.get("iterations", 0)
    }


def executor_node(state: AgentState) -> dict:
    """Calls the relevant Clinical Tables APIs based on the plan."""
    raw_results = []
    reasoning_entries = []

    for system in state["planned_systems"]:
        term = state["search_terms"].get(system, state["query"])
        tool = get_tool_for_system(system)
        if tool is None:
            logger.warning(f"No tool found for system: {system}")
            continue

        try:
            results = tool.search(term)
            raw_results.extend(results)
            reasoning_entries.append(
                f"[Executor] {system}: queried '{term}', got {len(results)} results"
            )
        except Exception as e:
            logger.error(f"Error querying {system}: {e}")
            reasoning_entries.append(f"[Executor] {system}: ERROR - {str(e)}")

    return {
        "raw_results": raw_results,
        "reasoning": reasoning_entries,
        "iterations": state.get("iterations", 0) + 1
    }


def refiner_node(state: AgentState) -> dict:
    """LLM evaluates results and optionally refines the search."""
    if state.get("iterations", 0) >= 2:
        return {"finished": True, "reasoning": ["[Refiner] Max iterations reached, proceeding to summarize."]}

    llm = make_llm()
    results_summary = json.dumps(state["raw_results"][:20], indent=2)
    messages = [
        SystemMessage(content=REFINER_SYSTEM_PROMPT),
        HumanMessage(content=f'Query: "{state["query"]}"\n\nResults so far:\n{results_summary}')
    ]
    response = llm.invoke(messages)
    content = response.content.strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if "```" in content:
            content = content[:content.rfind("```")].strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {"finished": True, "reasoning": ["[Refiner] Could not parse response, finishing."]}

    if parsed.get("sufficient", True) or not parsed.get("additional_searches"):
        return {
            "finished": True,
            "reasoning": [f"[Refiner] {parsed.get('reasoning', 'Results sufficient.')}"]
        }
    else:
        # Merge additional searches into plan for next iteration
        additional = parsed.get("additional_searches", {})
        updated_systems = list(additional.keys())
        updated_terms = {**state["search_terms"], **additional}
        return {
            "planned_systems": updated_systems,
            "search_terms": updated_terms,
            "finished": False,
            "reasoning": [f"[Refiner] Refining search: {parsed.get('reasoning', '')}"]
        }


def consolidator_node(state: AgentState) -> dict:
    """Deduplicates and normalizes raw results into structured CodeResults."""
    from utils.deduplication import deduplicate_results
    code_results = deduplicate_results(state["raw_results"])
    return {
        "code_results": code_results,
        "reasoning": [f"[Consolidator] {len(code_results)} unique codes retained from {len(state['raw_results'])} raw results"]
    }


def summarizer_node(state: AgentState) -> dict:
    """LLM produces a human-readable summary of findings."""
    llm = make_llm()
    codes_text = json.dumps(state["code_results"], indent=2)
    messages = [
        SystemMessage(content=SUMMARIZER_SYSTEM_PROMPT),
        HumanMessage(content=f'Query: "{state["query"]}"\n\nCodes found:\n{codes_text}')
    ]
    response = llm.invoke(messages)
    return {"summary": response.content.strip()}

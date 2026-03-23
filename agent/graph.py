from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import planner_node, executor_node, refiner_node, consolidator_node, summarizer_node


def should_continue(state: AgentState) -> str:
    """Route: continue iterating or move to consolidation."""
    if state.get("finished", False):
        return "consolidate"
    return "execute"


def build_agent_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("refiner", refiner_node)
    graph.add_node("consolidator", consolidator_node)
    graph.add_node("summarizer", summarizer_node)

    # Define flow
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "refiner")
    graph.add_conditional_edges(
        "refiner",
        should_continue,
        {
            "execute": "executor",
            "consolidate": "consolidator"
        }
    )
    graph.add_edge("consolidator", "summarizer")
    graph.add_edge("summarizer", END)

    return graph.compile()

"""Integration tests for the agent graph."""
import pytest
from unittest.mock import patch, MagicMock


class TestAgentGraph:
    def test_graph_builds(self):
        """Test that the graph compiles without errors."""
        from agent import build_agent_graph
        graph = build_agent_graph()
        assert graph is not None

    def test_planner_output_structure(self):
        """Test planner returns expected state keys."""
        from agent.nodes import planner_node
        mock_llm_response = MagicMock()
        mock_llm_response.content = '''{
            "relevant_systems": ["ICD-10-CM"],
            "search_terms": {"ICD-10-CM": "diabetes"},
            "reasoning": "Diabetes is a diagnosis, so ICD-10-CM is relevant."
        }'''

        with patch("agent.nodes.ChatOpenAI") as MockLLM:
            MockLLM.return_value.invoke.return_value = mock_llm_response
            result = planner_node({"query": "diabetes", "iterations": 0})

        assert "planned_systems" in result
        assert "ICD-10-CM" in result["planned_systems"]
        assert "search_terms" in result

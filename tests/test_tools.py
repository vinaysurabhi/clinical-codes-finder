"""Tests for individual coding system tools."""
import pytest
from unittest.mock import patch, MagicMock


class TestICD10CMTool:
    def test_search_returns_list(self):
        from tools.icd10cm import ICD10CMTool
        tool = ICD10CMTool()
        mock_response = [
            2,
            ["E11", "E11.9"],
            None,
            [["E11", "Type 2 diabetes mellitus"], ["E11.9", "Type 2 diabetes mellitus without complications"]]
        ]
        with patch("tools.icd10cm.query_clinical_tables", return_value=mock_response):
            results = tool.search("diabetes")
        assert len(results) == 2
        assert results[0]["system"] == "ICD-10-CM"
        assert results[0]["code"] == "E11"
        assert "diabetes" in results[0]["display"].lower()

    def test_empty_response(self):
        from tools.icd10cm import ICD10CMTool
        tool = ICD10CMTool()
        with patch("tools.icd10cm.query_clinical_tables", return_value=[]):
            results = tool.search("nonexistent")
        assert results == []


class TestLOINCTool:
    def test_search_returns_list(self):
        from tools.loinc import LOINCTool
        tool = LOINCTool()
        mock_response = [
            1,
            ["2345-7"],
            None,
            [["2345-7", "Glucose [Mass/volume] in Blood", "Glucose", "Blood"]]
        ]
        with patch("tools.loinc.query_clinical_tables", return_value=mock_response):
            results = tool.search("glucose test")
        assert len(results) == 1
        assert results[0]["system"] == "LOINC"
        assert results[0]["metadata"]["component"] == "Glucose"


class TestRxTermsTool:
    def test_search_returns_list(self):
        from tools.rxterms import RxTermsTool
        tool = RxTermsTool()
        mock_response = [
            1,
            ["860974"],
            None,
            [["860974", "Metformin 500 MG Oral Tablet", "Oral", "500 MG"]]
        ]
        with patch("tools.rxterms.query_clinical_tables", return_value=mock_response):
            results = tool.search("metformin 500 mg")
        assert len(results) == 1
        assert results[0]["metadata"]["strength"] == "500 MG"


class TestToolRegistry:
    def test_get_tool_for_system(self):
        from tools import get_tool_for_system
        assert get_tool_for_system("ICD-10-CM") is not None
        assert get_tool_for_system("LOINC") is not None
        assert get_tool_for_system("UNKNOWN") is None

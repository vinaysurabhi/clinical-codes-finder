#!/usr/bin/env python3
"""
Clinical Codes Finder - CLI Entry Point
Usage: python main.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY not set. Please copy .env.example to .env and add your key.")
    sys.exit(1)

from agent import build_agent_graph
from utils.formatting import format_results_table

BANNER = """
╔══════════════════════════════════════════════════════╗
║          🏥 Clinical Codes Finder                    ║
║  ICD-10-CM · LOINC · RxTerms · HCPCS · UCUM · HPO   ║
╚══════════════════════════════════════════════════════╝
"""

SAMPLE_QUERIES = [
    "diabetes",
    "glucose test",
    "metformin 500 mg",
    "wheelchair",
    "mg/dL",
    "ataxia"
]


def run_query(query: str):
    print(f"\n🔍 Query: '{query}'")
    print("-" * 60)

    graph = build_agent_graph()

    initial_state = {
        "query": query,
        "planned_systems": [],
        "search_terms": {},
        "raw_results": [],
        "code_results": [],
        "reasoning": [],
        "summary": "",
        "iterations": 0,
        "finished": False
    }

    result = graph.invoke(initial_state)

    # Print reasoning trace
    print("\n📋 Agent Reasoning:")
    for step in result.get("reasoning", []):
        print(f"  {step}")

    # Print code results
    print("\n📊 Codes Found:")
    print(format_results_table(result.get("code_results", [])))

    # Print summary
    print("\n💡 Summary:")
    print(result.get("summary", "No summary generated."))
    print("\n" + "=" * 60)


def main():
    print(BANNER)
    print("Enter a clinical term to find codes, or type 'demo' to run sample queries.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("🩺 Enter clinical term: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "demo":
            for q in SAMPLE_QUERIES:
                run_query(q)
        else:
            run_query(user_input)


if __name__ == "__main__":
    main()

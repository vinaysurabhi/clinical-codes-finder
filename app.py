"""Streamlit UI for Clinical Codes Finder."""
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Clinical Codes Finder",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinical Codes Finder")
st.caption("Agentic RAG · ICD-10-CM · LOINC · RxTerms · HCPCS · UCUM · HPO")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    max_results = st.slider("Max results per system", 1, 10, 5)
    show_reasoning = st.checkbox("Show agent reasoning", value=True)
    st.markdown("---")
    st.markdown("**Sample Queries:**")
    samples = ["diabetes", "glucose test", "metformin 500 mg", "wheelchair", "mg/dL", "ataxia"]
    for s in samples:
        if st.button(s, key=f"sample_{s}"):
            st.session_state["query_input"] = s

# Main area
query = st.text_input(
    "🔍 Enter a clinical term",
    placeholder="e.g. diabetes, glucose test, metformin 500 mg...",
    key="query_input"
)

if st.button("Find Codes", type="primary") and query:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["MAX_RESULTS_PER_SYSTEM"] = str(max_results)

        with st.spinner("🤖 Agent is searching across coding systems..."):
            from agent import build_agent_graph
            from utils.formatting import format_results_json

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

        # Summary
        st.success("✅ Search complete!")
        st.subheader("💡 Summary")
        st.info(result.get("summary", "No summary generated."))

        # Results by system
        st.subheader("📊 Results by Coding System")
        grouped = format_results_json(result.get("code_results", []))

        if not grouped:
            st.warning("No codes found for this query.")
        else:
            cols = st.columns(min(len(grouped), 3))
            for idx, (system, codes) in enumerate(grouped.items()):
                with cols[idx % 3]:
                    st.markdown(f"**{system}**")
                    for c in codes:
                        with st.expander(f"`{c['code']}` — {c['display'][:60]}"):
                            st.write(f"**Code:** `{c['code']}`")
                            st.write(f"**Display:** {c['display']}")
                            if c.get("metadata"):
                                st.write("**Metadata:**")
                                for k, v in c["metadata"].items():
                                    if v:
                                        st.write(f"  - {k}: {v}")

        # Reasoning trace
        if show_reasoning:
            with st.expander("🧠 Agent Reasoning Trace"):
                for step in result.get("reasoning", []):
                    st.text(step)

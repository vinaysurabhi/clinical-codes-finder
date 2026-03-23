# 🏥 Clinical Codes Finder

An intelligent **Agentic RAG** system that takes a clinical term (e.g., `"diabetes"`, `"metformin 500 mg"`, `"glucose test"`) and returns the most relevant medical codes across **6 major coding systems** — powered by **LangGraph**, **LangChain**, and **OpenAI**.

## 🎯 Supported Coding Systems

| System | Coverage |
|--------|----------|
| **ICD-10-CM** | Diagnosis codes |
| **LOINC** | Lab tests & measurements |
| **RxTerms / RxNorm** | Drug names & strengths |
| **HCPCS** | Medical supplies & services |
| **UCUM** | Units of measure |
| **HPO** | Phenotypic traits & symptoms |

## 🧠 How It Works (Agentic RAG)

1. **Intent Understanding** — LLM interprets the query and identifies relevant coding systems
2. **Dynamic Planning** — Chooses which APIs to query and in what order
3. **Iterative Action** — Calls NLM Clinical Tables APIs, observes results, adjusts strategy
4. **Refinement** — Expands/narrows searches based on relevance signals
5. **Consolidation** — Deduplicates, normalizes, and groups results
6. **Explanation** — Generates a plain-English summary of findings

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation

```bash
git clone https://github.com/vinaysurabhi/clinical-codes-finder.git
cd clinical-codes-finder
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Run CLI

```bash
python main.py
```

### Run Streamlit App

```bash
streamlit run app.py
```

## 📁 Project Structure

```
clinical-codes-finder/
├── main.py                  # CLI entry point
├── app.py                   # Streamlit UI
├── agent/
│   ├── __init__.py
│   ├── graph.py             # LangGraph state machine
│   ├── nodes.py             # Agent nodes (planner, executor, summarizer)
│   ├── state.py             # Shared agent state definition
│   └── prompts.py           # System and user prompt templates
├── tools/
│   ├── __init__.py
│   ├── clinical_tables.py   # NLM Clinical Tables API client
│   ├── icd10cm.py           # ICD-10-CM tool
│   ├── loinc.py             # LOINC tool
│   ├── rxterms.py           # RxTerms/RxNorm tool
│   ├── hcpcs.py             # HCPCS tool
│   ├── ucum.py              # UCUM tool
│   └── hpo.py               # HPO tool
├── utils/
│   ├── __init__.py
│   ├── deduplication.py     # Result normalization & dedup
│   └── formatting.py        # Output formatting helpers
├── tests/
│   ├── test_tools.py
│   └── test_agent.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🧪 Test Queries

| Query | Expected Focus |
|-------|----------------|
| `diabetes` | ICD-10-CM |
| `glucose test` | LOINC |
| `metformin 500 mg` | RxTerms / RxNorm |
| `wheelchair` | HCPCS |
| `mg/dL` | UCUM |
| `ataxia` | HPO |

## 📹 Demo Video

> 🎬 [Watch the Demo on Loom](#) *(link to be added)*

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│          LangGraph Agent                │
│                                         │
│  ┌──────────┐    ┌──────────────────┐  │
│  │ Planner  │───▶│  Tool Executor   │  │
│  │  (LLM)   │    │  (API Calls)     │  │
│  └──────────┘    └────────┬─────────┘  │
│       ▲                   │             │
│       └───────────────────┘             │
│            (iterate)                    │
│                   │                     │
│          ┌────────▼────────┐           │
│          │   Summarizer    │           │
│          │    (LLM)        │           │
│          └────────┬────────┘           │
└───────────────────┼─────────────────────┘
                    ▼
           Structured Output
           (Codes + Summary)
```

## 📡 Data Sources

All coding data is fetched live from the [NLM Clinical Tables Search Service](https://clinicaltables.nlm.nih.gov/) — no static databases.

## 📄 License

MIT License

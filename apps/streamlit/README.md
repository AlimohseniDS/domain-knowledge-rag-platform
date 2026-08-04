# Streamlit RAG Console

Thin user and engineering interface for the RAG platform. It communicates only with FastAPI and never connects directly to PostgreSQL, Redis, document storage, embedding services, or vLLM.

## Run locally

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e 'apps/streamlit[dev]'
streamlit run apps/streamlit/app.py
```

The default API URL is `http://localhost:8000`. Override it when FastAPI runs elsewhere:

```bash
RAG_API_BASE_URL=http://gpu-server:8000 \
  streamlit run apps/streamlit/app.py
```

The console remains usable when the API is unavailable and displays a clear connection message. Backend operations become active as the corresponding Phase 1 endpoints are implemented.

## Pages

- Documents: upload, inspect, refresh, and delete documents
- Chat: ask grounded questions and inspect structured citations
- Retrieval Debug: inspect chunks and similarity scores without generation
- System Status: check API and dependency readiness

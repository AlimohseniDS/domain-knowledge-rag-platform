# ADR 0001: Use Streamlit for the Initial Interface

- Status: Accepted
- Date: 2026-08-04

## Context

Phase 1 needs a usable interface for document ingestion, grounded chat, citation inspection, retrieval debugging, and dependency health. Building a polished customer frontend before validating the RAG pipeline would slow feedback on the higher-risk retrieval and grounding work.

## Decision

Use one evolving Streamlit application for the Phase 1 interface and the long-term engineering console. Streamlit communicates exclusively with FastAPI. It does not connect directly to PostgreSQL, Redis, document storage, embedding services, or vLLM.

## Consequences

- Phase 1 workflows can be exercised early.
- Backend contracts remain reusable by a future Next.js application.
- Streamlit can remain an internal evaluation and operations interface.
- A separate customer-facing frontend may still be required for advanced branding, accessibility, and interaction requirements.

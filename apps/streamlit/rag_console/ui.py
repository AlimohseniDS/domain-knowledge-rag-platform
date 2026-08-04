from __future__ import annotations

from typing import Any

import streamlit as st

from .client import APIClient, APIError
from .config import ConsoleSettings


def configure_page(title: str, icon: str) -> None:
    st.set_page_config(page_title=f"{title} · RAG Platform", page_icon=icon, layout="wide")


@st.cache_resource
def api_client() -> APIClient:
    return APIClient(ConsoleSettings.from_environment())


def render_sidebar() -> APIClient:
    client = api_client()
    with st.sidebar:
        st.header("RAG Platform")
        st.caption("Phase 1 engineering console")
        st.code(client.settings.api_base_url, language=None)
        try:
            health = client.health()
            status = str(health.get("status", "ok")).lower()
            st.success(f"API: {status}")
        except APIError:
            st.warning("API unavailable")
        st.divider()
        st.caption("Primary model")
        st.code("Qwen3.5-35B-A3B GPTQ Int4", language=None)
    return client


def show_api_error(error: APIError) -> None:
    st.error(str(error))
    if error.status_code is None:
        st.info("Start FastAPI or set `RAG_API_BASE_URL` to the running backend.")


def render_citations(citations: list[dict[str, Any]]) -> None:
    if not citations:
        return
    st.markdown("#### Sources")
    for index, citation in enumerate(citations, start=1):
        title = citation.get("title") or citation.get("document_title") or "Untitled source"
        page = citation.get("page") or citation.get("page_number")
        label = f"{index}. {title}" + (f" — page {page}" if page else "")
        with st.expander(label):
            passage = citation.get("passage") or citation.get("content")
            if passage:
                st.write(passage)
            st.json(citation)

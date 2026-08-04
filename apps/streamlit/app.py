import streamlit as st

from rag_console.ui import configure_page, render_sidebar

configure_page("Home", "📚")
render_sidebar()

st.title("Domain Knowledge RAG Platform")
st.write(
    "Use this console to ingest domain documents, test grounded answers, inspect retrieval, "
    "and check platform health."
)

st.info(
    "The Streamlit console is ready. Backend actions will become available as the Phase 1 "
    "FastAPI endpoints are implemented."
)

left, right = st.columns(2)
with left:
    st.subheader("Phase 1 workflow")
    st.markdown(
        """
1. Upload a supported document.
2. Wait for ingestion to complete.
3. Ask a domain question in Chat.
4. Verify the cited passages.
5. Inspect retrieval scores when an answer is weak.
"""
    )
with right:
    st.subheader("Console boundaries")
    st.markdown(
        """
- All operations go through FastAPI.
- Streamlit never accesses PostgreSQL directly.
- Documents are never read directly from storage.
- Model calls are owned by the backend provider gateway.
"""
    )

import streamlit as st

from rag_console import APIError
from rag_console.ui import configure_page, render_sidebar, show_api_error

configure_page("Retrieval Debug", "🔎")
client = render_sidebar()

st.title("Retrieval Debug")
st.caption("Inspect evidence selection without generating an LLM answer.")

query = st.text_input("Query")
top_k = st.slider("Maximum chunks", min_value=1, max_value=20, value=8)

if st.button("Run retrieval", type="primary", disabled=not query.strip()):
    try:
        result = client.debug_retrieval(query.strip(), top_k=top_k)
        chunks = result.get("chunks") or result.get("results") or []
        if not chunks:
            st.warning("No passages passed the retrieval threshold.")
        for index, chunk in enumerate(chunks, start=1):
            score = chunk.get("score")
            title = chunk.get("document_title") or chunk.get("title") or "Untitled source"
            score_label = f" · score {score:.4f}" if isinstance(score, (int, float)) else ""
            with st.expander(f"{index}. {title}{score_label}", expanded=index <= 3):
                st.write(chunk.get("content") or chunk.get("passage") or "No passage returned")
                st.json(chunk)
    except APIError as error:
        show_api_error(error)

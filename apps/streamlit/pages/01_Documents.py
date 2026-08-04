import streamlit as st

from rag_console import APIError
from rag_console.ui import configure_page, render_sidebar, show_api_error

configure_page("Documents", "📄")
client = render_sidebar()

st.title("Documents")
st.caption("Upload and monitor the domain knowledge corpus.")

uploaded = st.file_uploader(
    "Select a document",
    type=["pdf", "docx", "md", "txt", "html", "csv"],
)
if uploaded and st.button("Upload and index", type="primary"):
    try:
        result = client.upload_document(
            uploaded.name,
            uploaded.getvalue(),
            uploaded.type or "application/octet-stream",
        )
        st.success("Document accepted for ingestion.")
        st.json(result)
        st.cache_data.clear()
    except APIError as error:
        show_api_error(error)

st.divider()
header, refresh = st.columns([5, 1])
header.subheader("Knowledge corpus")
if refresh.button("Refresh"):
    st.rerun()

try:
    documents = client.list_documents()
except APIError as error:
    show_api_error(error)
    documents = []

if documents:
    st.dataframe(documents, use_container_width=True, hide_index=True)
    identifiers = {
        f"{item.get('display_name') or item.get('name') or item.get('id')} ({item.get('id')})": str(
            item.get("id")
        )
        for item in documents
        if item.get("id")
    }
    selected = st.selectbox("Document to delete", options=list(identifiers))
    confirmation = st.checkbox("I understand this removes the document from retrieval")
    if st.button("Delete document", disabled=not confirmation):
        try:
            client.delete_document(identifiers[selected])
            st.success("Document deletion requested.")
            st.rerun()
        except APIError as error:
            show_api_error(error)
else:
    st.info("No indexed documents are available, or the API is not running.")

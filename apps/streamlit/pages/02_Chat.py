import streamlit as st

from rag_console import APIError
from rag_console.ui import configure_page, render_citations, render_sidebar, show_api_error

configure_page("Chat", "💬")
client = render_sidebar()

st.title("Grounded Chat")
st.caption("Answers should be supported by passages from the indexed domain corpus.")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("citations"):
            render_citations(message["citations"])

question = st.chat_input("Ask a question about your domain knowledge")
if question:
    st.session_state.chat_messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Retrieving evidence and asking Qwen…"):
                response = client.chat(question)
            answer = str(response.get("answer") or response.get("content") or "")
            citations = response.get("citations") or []
            if not answer:
                raise APIError("The chat endpoint returned no answer.")
            st.markdown(answer)
            render_citations(citations)
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": answer, "citations": citations}
            )
        except APIError as error:
            show_api_error(error)

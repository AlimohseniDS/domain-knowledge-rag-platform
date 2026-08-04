import streamlit as st

from rag_console import APIError
from rag_console.ui import configure_page, render_sidebar

configure_page("System Status", "🩺")
client = render_sidebar()

st.title("System Status")
st.caption("Liveness confirms the API process; readiness checks its dependencies.")

checks = [("API liveness", client.health), ("Platform readiness", client.readiness)]
for label, check in checks:
    st.subheader(label)
    try:
        result = check()
        st.success(str(result.get("status", "available")))
        st.json(result)
    except APIError as error:
        st.error(str(error))

if st.button("Refresh status"):
    st.rerun()

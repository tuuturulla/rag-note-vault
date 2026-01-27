import streamlit as st
import httpx

st.title("RAG Note Vault")

resp = httpx.get("http://127.0.0.1:8000/health")
st.json(resp.json())
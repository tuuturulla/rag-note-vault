import os 
import streamlit as st
import httpx
from dotenv import load_dotenv

# Environment and Configuration 
# Load environment variables from .evn file 
# Define where the API is located (defaulting to localhost:8000)
load_dotenv() 
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.title("RAG Note Vault")

# Sidebar: Health Check 
# Ping the /health endpoint of our FastAPI app to ensure it's online 
with st.sidebar:
    st.subheader("API Health Check")
    try:
        r = httpx.get(f"{API_BASE_URL}/health", timeout=5)
        st.json(r.json()) 
    except Exception as e:
        st.error(f"API Health Check Failed: {e}")

# File upload section 
# Streamlit provides a built-in file uploader widget that allows users to select files from their local system.
st.header("Upload") 
uploaded = st.file_uploader("Choose a file", type=None)

if uploaded is not None:
    # Send the file to the FastAPI endpoint when user clicks the button
    if st.button("Upload to vault:"): 
        # Prepare the file for upload by creating a multipart/form-data request. 
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        resp = httpx.post(f"{API_BASE_URL}/documents/upload", files=files, timeout=60)
        if resp.status_code == 200: 
            st.success(f"Uploaded: {resp.json()['filename']}") 
        else: 
            st.error(f"Upload failed: {resp.status_code} {resp.text}")

# Document listing section
# Fetch the list of documents from the API 
st.header("Documents") 
if st.button("Refresh list"): 
    st.rerun() # forces streamlit to restart the script and fetch fresh data 

try:
    # fetch the list of documents from the API 
    docs= httpx.get(f"{API_BASE_URL}/documents", timeout=10).json() 
    if not docs: 
        st.info("No documents yet.")
    else:
        # loop throught the list (array) and display each documents metadata 
        for d in docs: 
            st.write(f"**{d['filename']}** \n{d['created_at']}")
            st.caption(d["file_path"])
            st.divider() 
except Exception as e:
    st.error(f"Failed to load documents: {e}") 





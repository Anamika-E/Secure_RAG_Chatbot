import os
import re
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="Secure RAG Chatbot", page_icon="🛡️", layout="wide")

st.title("🛡️ Secure RAG Chatbot (with PII Masking)")

# 2. Sidebar Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

uploaded_file = st.sidebar.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    st.sidebar.success("File Uploaded Successfully!")

# Helper function for PII Masking
def mask_pii(text):
    # Email Masking
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    masked_text = re.sub(email_pattern, '<EMAIL_ADDRESS>', text)
    
    # Phone Number Masking
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    masked_text = re.sub(phone_pattern, '<PHONE_NUMBER>', masked_text)
    
    return masked_text

# Text Extraction
extracted_text = ""
if uploaded_file is not None:
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""
    elif uploaded_file.name.endswith('.txt'):
        extracted_text = uploaded_file.read().decode("utf-8")

    # Apply PII Masking
    masked_document = mask_pii(extracted_text)

    # View Masked Document Section
    with st.expander("🔍 View Masked Document (What LLM sees)"):
        st.write(masked_document)

# 3. Chat / Query Section
user_query = st.text_input("Ask something about your document:")

if user_query:
    if not api_key:
        st.error("Please enter your Google Gemini API Key in the sidebar.")
    elif not extracted_text:
        st.error("Please upload a document first.")
    else:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)

            # BUG FIX: Updated model name to gemini-2.0-flash
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Create Prompt with Context
            prompt = f"""
            You are a helpful assistant. Answer the user's question based ONLY on the context provided below.
            
            Context:
            {masked_document}
            
            User Question:
            {user_query}
            """

            # Generate Response
            with st.spinner("Analyzing document..."):
                response = model.generate_content(prompt)
                
            st.markdown("### Answer:")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error occurred: {e}")
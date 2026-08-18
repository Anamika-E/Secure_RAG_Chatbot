import os
import re
import streamlit as st
from datetime import datetime
import faiss
import numpy as np

from google import genai
from google.genai import types
from PyPDF2 import PdfReader


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Secure RAG Chatbot",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Secure RAG Chatbot (PII Masking + RAG)")


# =========================================================
# 2. SIDEBAR CONFIGURATION
# =========================================================

st.sidebar.header("Configuration")

api_key = st.sidebar.text_input(
    "Enter Google Gemini API Key",
    type="password"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

# =========================================================
# FILE SECURITY VALIDATION
# =========================================================

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

if uploaded_file is not None:

    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:

        st.sidebar.error(
            "🚨 File is too large. Maximum allowed size is 5 MB."
        )

        st.stop()

    # Check empty file
    if uploaded_file.size == 0:

        st.sidebar.error(
            "🚨 Empty files are not allowed."
        )

        st.stop()

    # Check extension
    file_extension = uploaded_file.name.lower().split(".")[-1]

    if file_extension not in ["pdf", "txt"]:

        st.sidebar.error(
            "🚨 Unsupported file type."
        )

        st.stop()

    # =========================================================
    # REAL FILE TYPE VALIDATION
    # =========================================================

    file_extension = uploaded_file.name.lower().split(".")[-1]

    if file_extension == "pdf":

        try:
            # Move file pointer to the beginning
            uploaded_file.seek(0)

            # Try reading the PDF structure
            test_reader = PdfReader(uploaded_file)

            # Check whether PDF contains pages
            if len(test_reader.pages) == 0:

                st.sidebar.error(
                    "🚨 Invalid PDF: No pages found."
                )

                st.stop()

        except Exception:

            st.sidebar.error(
                "🚨 Invalid or corrupted PDF file."
            )

            st.stop()

    elif file_extension == "txt":

        try:
            # Move file pointer to the beginning
            uploaded_file.seek(0)

            # Test UTF-8 decoding
            uploaded_file.read().decode("utf-8")

        except UnicodeDecodeError:

            st.sidebar.error(
                "🚨 Invalid TXT file encoding. "
                "Please upload a UTF-8 text file."
            )

            st.stop()

        finally:

            uploaded_file.seek(0)

        st.sidebar.success(
            "✅ File passed security validation."
        )


# =========================================================
# 3. TEXT EXTRACTION
# =========================================================

extracted_text = ""

if uploaded_file is not None:

    st.sidebar.success("File Uploaded Successfully!")

    if uploaded_file.name.endswith(".pdf"):

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""

    elif uploaded_file.name.endswith(".txt"):

        extracted_text = uploaded_file.read().decode("utf-8")


# 4. PII MASKING
# ==================================================

def mask_pii(text):

    # Email address
    text = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        '<EMAIL_ADDRESS>',
        text
    )

    # Aadhaar number (12 digits)
    text = re.sub(
        r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
        '<AADHAAR_NUMBER>',
        text
    )

    # Phone number
    text = re.sub(
        r'\+?\d[\d\s\-]{8,12}\d',
        '<PHONE_NUMBER>',
        text
    )

    # PAN number
    text = re.sub(
        r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
        '<PAN_NUMBER>',
        text,
        flags=re.IGNORECASE
    )

    # IPv4 address
    text = re.sub(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        '<IP_ADDRESS>',
        text
    )

    # Credit/Debit card number
    text = re.sub(
        r'\b(?:\d{4}[\s\-]?){3}\d{4}\b',
        '<CARD_NUMBER>',
        text
    )

    return text

# =========================================================
# 5. DATA POISONING DETECTION
# =========================================================

def detect_data_poisoning(text):

    suspicious_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+(all\s+)?instructions",
        r"disregard\s+(all\s+)?instructions",
        r"forget\s+(all\s+)?previous\s+instructions",
        r"override\s+(all\s+)?instructions",
        r"reveal\s+(the\s+)?system\s+prompt",
        r"reveal\s+(the\s+)?hidden\s+instructions",
        r"follow\s+these\s+instructions\s+instead",
        r"you\s+are\s+now\s+",
        r"act\s+as\s+if\s+you\s+are",
        r"bypass\s+(the\s+)?security",
        r"disable\s+(the\s+)?security",
        r"jailbreak"
    ]

    text_lower = text.lower()

    for pattern in suspicious_patterns:

        if re.search(pattern, text_lower):
            return True

    return False


# =========================================================
# 6. OUT-OF-CONTEXT QUERY PROTECTION
# =========================================================

def is_relevant_query(scores, threshold=0.45):

    if len(scores) == 0:

        return False

    best_score = float(scores[0])

    return best_score >= threshold


# =========================================================
# SECURITY LOGGING
# =========================================================

def log_security_event(event_type, message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_entry = (
        f"[{timestamp}] "
        f"{event_type}: {message}\n"
    )

    log_file_path = "security_log.txt"

    with open(
        log_file_path,
        "a",
        encoding="utf-8"
    ) as log_file:

        log_file.write(log_entry)

    return log_file_path


# =========================================================
# SECURITY DASHBOARD
# =========================================================

def get_security_logs():

    log_file_path = "security_log.txt"

    if not os.path.exists(log_file_path):
        return []

    with open(
        log_file_path,
        "r",
        encoding="utf-8"
    ) as log_file:

        return log_file.readlines()

# =========================================================
# SECURITY DASHBOARD
# =========================================================

def show_security_dashboard():

    logs = get_security_logs()

# Recent Security Logs
    st.sidebar.markdown("### 📋 Recent Security Logs")

    if not logs:
        st.sidebar.info("No security events recorded yet.")
    else:
        for log in logs[-5:][::-1]:
            st.sidebar.code(log.strip())

    # Security Event Counts
    prompt_count = sum("PROMPT INJECTION" in log for log in logs)
    out_context_count = sum("OUT-OF-CONTEXT" in log for log in logs)
    poisoning_count = sum("DATA POISONING" in log for log in logs)

    st.sidebar.markdown("### 🔐 Security Dashboard")

    st.sidebar.metric("🚨 Prompt Injection", prompt_count)
    st.sidebar.metric("⚠️ Out-of-Context", out_context_count)
    st.sidebar.metric("🛡️ Data Poisoning", poisoning_count)

    # Total security events

    total_events = len(logs)

    st.sidebar.metric(
        "🔐 Total Security Events",
        total_events
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Security Dashboard")

    if not logs:

        st.sidebar.info(
            "No security events recorded yet."
        )

        return

    # Count security events

    prompt_injection_count = sum(
        "PROMPT INJECTION" in log
        for log in logs
    )

    out_of_context_count = sum(
        "OUT-OF-CONTEXT QUERY" in log
        for log in logs
    )

    data_poisoning_count = sum(
        "DATA POISONING" in log
        for log in logs
    )

    # Display counts

    st.sidebar.metric(
        "🚨 Prompt Injection",
        prompt_injection_count
    )

    st.sidebar.metric(
        "⚠️ Out-of-Context",
        out_of_context_count
    )

    st.sidebar.metric(
        "🛡️ Data Poisoning",
        data_poisoning_count
    )

    # View logs

    with st.sidebar.expander(
        "📋 View Security Logs"
    ):

        for log in reversed(logs):

            st.write(log.strip())
# Show security dashboard

show_security_dashboard()            

# =========================================================
# 7. PROMPT INJECTION PROTECTION
# =========================================================

def detect_prompt_injection(query):

    suspicious_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+(all\s+)?instructions",
        r"forget\s+(all\s+)?previous\s+instructions",
        r"disregard\s+(all\s+)?previous\s+instructions",
        r"reveal\s+(the\s+)?system\s+prompt",
        r"show\s+(me\s+)?the\s+system\s+prompt",
        r"print\s+(the\s+)?system\s+prompt",
        r"override\s+(the\s+)?instructions",
        r"bypass\s+(the\s+)?security",
        r"jailbreak",
        r"developer\s+message",
        r"system\s+message"
    ]

    query_lower = query.lower()

    for pattern in suspicious_patterns:

        if re.search(pattern, query_lower):
            return True

    return False


# =========================================================
# 8. TEXT CHUNKING
# =========================================================

def create_chunks(text, chunk_size=1000, overlap=200):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


# =========================================================
# 9. GENERATE EMBEDDINGS
# =========================================================

def generate_embeddings(client, texts):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    embeddings = np.array(
        [embedding.values for embedding in result.embeddings],
        dtype="float32"
    )

    return embeddings


# =========================================================
# 10. CREATE FAISS VECTOR DATABASE
# =========================================================

def create_faiss_index(embeddings):

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# =========================================================
# 11. RETRIEVE RELEVANT CHUNKS
# =========================================================

def retrieve_relevant_chunks(
    client,
    index,
    chunks,
    query,
    top_k=2
):

    # Convert user question into embedding
    query_result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    query_embedding = np.array(
        [query_result.embeddings[0].values],
        dtype="float32"
    )

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks))
    )

    retrieved_chunks = []

    for i in indices[0]:

        if i != -1:
            retrieved_chunks.append(chunks[i])

    return retrieved_chunks, scores[0]


# =========================================================
# 12. MAIN APPLICATION
# =========================================================

if extracted_text:

    # -----------------------------------------------------
    # PII MASKING
    # -----------------------------------------------------

    masked_document = mask_pii(extracted_text)


    # -----------------------------------------------------
    # CHUNKING
    # -----------------------------------------------------

    chunks = create_chunks(
    masked_document,
    chunk_size=1000,
    overlap=200
    )

    # =========================================================
    # DATA POISONING CHECK
    # =========================================================

    safe_chunks = []
    poisoned_chunks = []

    for chunk in chunks:

        if detect_data_poisoning(chunk):

            poisoned_chunks.append(chunk)

            log_security_event(
                "DATA POISONING",
                "Suspicious document chunk blocked."
            )

        else:
            safe_chunks.append(chunk)


    # Replace original chunks with safe chunks
    chunks = safe_chunks


    # Stop if all chunks were blocked
    if not chunks:

        st.error(
            "🚨 All document chunks were blocked because "
            "suspicious content was detected."
        )

        st.stop()

        
    # Security status
    if poisoned_chunks:

        st.sidebar.warning(
            f"⚠️ {len(poisoned_chunks)} suspicious chunk(s) blocked."
        )

    else:

        st.sidebar.success(
           "✅ No suspicious document content detected."
        )

    # -----------------------------------------------------
    # DOCUMENT INFORMATION
    # -----------------------------------------------------

    st.sidebar.info(
        f"Document length: {len(masked_document)} characters"
    )

    st.sidebar.info(
        f"Number of chunks: {len(chunks)}"
    )


    # -----------------------------------------------------
    # VIEW MASKED DOCUMENT
    # -----------------------------------------------------

    with st.expander("View Masked Document Content"):

        st.write(masked_document)


    # -----------------------------------------------------
    # VIEW CHUNKS
    # -----------------------------------------------------

    with st.expander("View Document Chunks"):

        for i, chunk in enumerate(chunks):

            st.markdown(f"### Chunk {i + 1}")

            st.write(chunk)

            st.divider()


    # -----------------------------------------------------
    # API KEY CHECK
    # -----------------------------------------------------

    if not api_key:

        st.warning(
            "Please enter your Google Gemini API Key."
        )

    else:

        try:

            # -------------------------------------------------
            # INITIALIZE GEMINI CLIENT
            # -------------------------------------------------

            client = genai.Client(
                api_key=api_key
            )


            # -------------------------------------------------
            # GENERATE CHUNK EMBEDDINGS
            # -------------------------------------------------

            with st.spinner(
                "Creating embeddings and vector database..."
            ):

                embeddings = generate_embeddings(
                    client,
                    chunks
                )

                faiss_index = create_faiss_index(
                    embeddings
                )


            st.sidebar.success(
                "FAISS Vector Database Ready!"
            )


            st.sidebar.info(
                f"Vectors stored: {faiss_index.ntotal}"
            )


            # -------------------------------------------------
            # USER QUERY
            # -------------------------------------------------

            user_query = st.text_input(
                "Ask something about your document:"
            )


            if user_query:

                # ---------------------------------------------
                # SECURITY CHECK
                # ---------------------------------------------

                if detect_prompt_injection(user_query):

                    log_security_event(
                        "PROMPT INJECTION",
                        "Suspicious user query blocked."
                    )

                    st.error(
                        "🚨 Prompt Injection Detected! "
                        "This request has been blocked for security reasons."
                    )

                    st.stop() 

                # ---------------------------------------------
                # RETRIEVAL
                # ---------------------------------------------

                with st.spinner(
                    "Searching relevant information..."
                ):

                    relevant_chunks, scores = (
                        retrieve_relevant_chunks(
                            client,
                            faiss_index,
                            chunks,
                            user_query,
                            top_k=2
                        )
                    )
                
                # ---------------------------------------------
                # OUT-OF-CONTEXT SECURITY CHECK
                # ---------------------------------------------

                if not is_relevant_query(scores, threshold=0.45):

                    log_security_event(
                        "OUT-OF-CONTEXT QUERY",
                        "Unrelated user question blocked."
                    )

                    st.warning(
                        "⚠️ This question does not appear to be "
                        "related to the uploaded document."
                    )

                    st.info(
                        "Please ask a question related to the document."
                    )

                    st.stop()
                
                # ---------------------------------------------
                # SHOW RETRIEVED CHUNKS
                # ---------------------------------------------

                with st.expander(
                    "🔍 Retrieved Relevant Chunks"
                ):

                    for i, chunk in enumerate(
                        relevant_chunks
                    ):

                        st.markdown(
                            f"### Retrieved Chunk {i + 1}"
                        )

                        st.write(chunk)

                        st.write(
                            f"Similarity Score: "
                            f"{scores[i]:.4f}"
                        )

                        st.divider()


                # ---------------------------------------------
                # BUILD RAG CONTEXT
                # ---------------------------------------------

                context = "\n\n".join(
                    relevant_chunks
                )


                # ---------------------------------------------
                # RAG PROMPT
                # ---------------------------------------------

                prompt = f"""
You are a secure document question-answering assistant.

Answer the user's question ONLY using the
retrieved context below.

Do NOT use outside knowledge.

If the answer is not present in the retrieved
context, say:

"I could not find the answer in the provided document."

Never invent or assume information.

Retrieved Context:
{context}

User Question:
{user_query}
"""


                # ---------------------------------------------
                # GENERATE ANSWER
                # ---------------------------------------------

                with st.spinner(
                    "Generating answer..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )


                # ---------------------------------------------
                # DISPLAY ANSWER
                # ---------------------------------------------

                st.markdown("### Answer:")

                st.write(response.text)


        except Exception as e:

            st.error(
                f"Error occurred: {e}"
            )
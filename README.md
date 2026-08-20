🔒 Secure RAG Chatbot

A security-focused Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF/TXT documents and ask questions about their content while protecting the system against common AI security threats.

🚀 Project Overview

The Secure RAG Chatbot combines Retrieval-Augmented Generation with multiple security mechanisms.

Instead of sending the entire document directly to the language model, the system:

1. Validates the uploaded file.
2. Extracts the document text.
3. Detects and masks sensitive PII.
4. Splits the document into smaller chunks.
5. Generates embeddings for the chunks.
6. Stores embeddings in a FAISS vector database.
7. Retrieves the most relevant chunks for each user query.
8. Blocks unrelated or malicious queries.
9. Generates an answer using only the retrieved document context.
10. Records security events in a security log.

🛡️ Security Features

1. File Security Validation

The system validates uploaded files before processing them.

* Supports PDF and TXT files
* Maximum file size: 5 MB
* Rejects empty files
* Validates PDF structure
* Validates UTF-8 encoding for TXT files
* Rejects corrupted or invalid PDF files

2. PII Masking

Sensitive information is masked before document processing.

Currently protected:

* Email addresses
* Phone numbers
* Aadhaar numbers
* PAN numbers
* IPv4 addresses
* Credit/Debit card numbers

Example:

Original:
rahul123@gmail.com
Masked:
<EMAIL_ADDRESS>

3. Data Poisoning Detection

The system scans document chunks for suspicious instructions that could manipulate the AI system.

Suspicious content is blocked before the chunks are stored in the vector database.

4. Prompt Injection Protection

User queries are checked for malicious instructions such as attempts to:

* Ignore previous instructions
* Reveal system prompts
* Override security rules
* Bypass security
* Perform jailbreak-style attacks

Detected malicious queries are blocked.

5. Out-of-Context Query Protection

The system compares the user’s question with retrieved document chunks using similarity scores.

If the question is not sufficiently related to the uploaded document, the request is blocked instead of generating an unrelated answer.

6. Secure RAG Generation

The language model is instructed to answer only from retrieved document context.

If the required information is not available in the retrieved context, the system instructs the model not to invent an answer.

7. Security Logging

Security events are recorded in security_log.txt.

Logged events include:

* Prompt Injection
* Out-of-Context Queries
* Data Poisoning

8. Security Dashboard

The application provides a dashboard showing:

* Prompt Injection count
* Out-of-Context Query count
* Data Poisoning count
* Total security events
* Recent security logs

🏗️ System Architecture

                User
                  │
                  ▼
          Upload PDF / TXT
                  │
                  ▼
        File Security Validation
                  │
                  ▼
          Text Extraction
                  │
                  ▼
             PII Masking
                  │
                  ▼
          Text Chunking
                  │
                  ▼
      Data Poisoning Detection
                  │
                  ▼
        Gemini Embeddings
                  │
                  ▼
        FAISS Vector Database
                  │
                  ▼
             User Query
                  │
                  ▼
       Prompt Injection Check
                  │
                  ▼
       Query Embedding + Search
                  │
                  ▼
       Out-of-Context Check
                  │
                  ▼
        Relevant Chunks
                  │
                  ▼
          Secure RAG Prompt
                  │
                  ▼
        Gemini Language Model
                  │
                  ▼
            Final Answer

🧰 Technologies Used

* Python
* Streamlit
* Google Gemini API
* Gemini Embeddings
* FAISS
* NumPy
* PyPDF2
* Regular Expressions

📂 Project Structure

Secure_RAG_Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── security_log.txt
│
├── pii.test.txt
├── poison_test.txt
├── position_test.txt
├── empty.txt
├── fake.pdf
│
└── .gitignore

⚙️ Installation

Clone or download the project and open the project directory.

Create and activate a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

🔑 Gemini API Key

The application requires a Google Gemini API key.

Enter the API key through the Streamlit sidebar when running the application.

Do not hard-code the API key inside the source code.

▶️ Run the Application

python -m streamlit run app.py

The application will open in the browser.

🧪 Security Testing

The project was tested against:

Test	Expected Result
Normal PDF/TXT upload	Accepted
Empty file	Blocked
Invalid PDF	Blocked
Large file	Blocked
PII-containing document	PII masked
Normal document question	Answer generated
Prompt injection	Blocked
Data poisoning	Suspicious chunks blocked
Out-of-context question	Blocked
Security event logging	Event recorded

🎯 Project Objective

The main objective of this project is to demonstrate how a RAG-based AI application can be designed with security controls instead of relying only on the language model.

The project focuses on protecting the RAG pipeline against document-level threats, user-level prompt attacks, sensitive-data exposure, and irrelevant queries.

🔮 Future Improvements

Possible future enhancements include:

* Named Entity Recognition (NER) for better name/address PII detection
* More advanced prompt injection detection
* Improved data poisoning detection
* Better semantic relevance thresholds
* Authentication and role-based access control
* Encrypted document storage
* Secure cloud deployment
* Automated security testing
* More detailed security analytics

👩‍💻 Author

Anamika

BCA — Artificial Intelligence & Data Science
🔒 Secure RAG Chatbot

A security-focused Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF or TXT documents and ask questions about their content while protecting the application against common AI security threats.

🚀 Project Overview

The Secure RAG Chatbot combines Retrieval-Augmented Generation with multiple security mechanisms.

Instead of sending the entire document directly to the language model, the system follows a secure processing pipeline:

1. Validates the uploaded file.
2. Extracts text from the document.
3. Detects and masks sensitive Personally Identifiable Information (PII).
4. Splits the document into smaller text chunks.
5. Scans chunks for suspicious or potentially malicious content.
6. Generates embeddings for safe document chunks.
7. Stores embeddings in a FAISS vector database.
8. Retrieves the most relevant chunks for each user query.
9. Checks user queries for prompt injection attempts.
10. Blocks questions that are unrelated to the uploaded document.
11. Generates an answer using only the retrieved document context.
12. Records security events and displays them in a security dashboard.

⸻

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

Sensitive information is masked before the document is processed by the RAG pipeline.

Currently protected:

* Email addresses
* Phone numbers
* Aadhaar numbers
* PAN numbers
* IPv4 addresses
* Credit and debit card numbers

Example:

Original:

rahul123@gmail.com

Masked:

<EMAIL_ADDRESS>

3. Data Poisoning Detection

The system scans document chunks for suspicious instructions that may attempt to manipulate the AI system.

Suspicious chunks are blocked before they are stored in the vector database.

Examples of suspicious patterns include attempts to:

* Ignore previous instructions
* Override instructions
* Reveal hidden instructions
* Bypass or disable security
* Perform jailbreak-style attacks

4. Prompt Injection Protection

User queries are checked for malicious instructions before retrieval and answer generation.

The system detects attempts to:

* Ignore previous instructions
* Reveal system prompts
* Override instructions
* Bypass security
* Perform jailbreak-style attacks
* Access hidden system or developer instructions

Detected malicious queries are blocked.

5. Out-of-Context Query Protection

The system compares the user’s question with retrieved document chunks using similarity scores.

If the question does not appear sufficiently related to the uploaded document, the request is blocked instead of generating an unrelated answer.

6. Secure RAG Generation

The language model is instructed to answer only using the retrieved document context.

If the required information is not available in the retrieved context, the model is instructed not to invent or assume information.

7. Security Logging

Security-related events are recorded in security_log.txt.

Logged events include:

* Prompt Injection
* Out-of-Context Queries
* Data Poisoning
* Application Errors

8. Security Dashboard

The Streamlit application includes a security dashboard that displays:

* Prompt Injection count
* Out-of-Context Query count
* Data Poisoning count
* Total security events
* Recent security logs

⸻

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

⸻

🧰 Technologies Used

* Python
* Streamlit
* Google Gemini API
* Gemini Embeddings
* FAISS
* NumPy
* PyPDF2
* Regular Expressions

⸻

📂 Project Structure

Secure_RAG_Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pii.test.txt
├── poison_test.txt
├── position_test.txt
├── empty.txt
├── fake.pdf
│
└── security_log.txt   # Generated during application runtime

Note: security_log.txt is generated automatically when security events or application errors occur and may be excluded from the Git repository through .gitignore.

⸻

⚙️ Installation

Clone or download the project and open the project directory.

1. Create a Virtual Environment

python -m venv venv

2. Activate the Virtual Environment

On Windows:

venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

⸻

🔑 Gemini API Key

The application requires a Google Gemini API key.

Enter the API key through the Streamlit sidebar when running the application.

For security reasons, do not hard-code the API key inside the source code.

⸻

▶️ Run the Application

Run the following command:

python -m streamlit run app.py

The application will open in your web browser.

⸻

🧪 Security Testing

The application was tested against the following scenarios:

Test	Expected Result
Normal PDF/TXT upload	Accepted
Empty file	Blocked
Invalid or corrupted PDF	Blocked
File larger than 5 MB	Blocked
PII-containing document	Sensitive data masked
Normal document question	Answer generated
Prompt injection attempt	Blocked
Data poisoning attempt	Suspicious chunks blocked
Out-of-context question	Blocked
Security event	Logged
Security dashboard	Event counts displayed

⸻

🎯 Project Objective

The main objective of this project is to demonstrate how a RAG-based AI application can be designed with security controls instead of relying only on the language model.

The project focuses on protecting the RAG pipeline against:

* Malicious document content
* Prompt injection attacks
* Sensitive data exposure
* Out-of-context queries
* Invalid or corrupted file uploads

⸻

🔮 Future Improvements

Possible future enhancements include:

* Named Entity Recognition (NER) for improved PII detection
* More advanced prompt injection detection
* Improved data poisoning detection techniques
* Dynamic semantic relevance thresholds
* Authentication and role-based access control
* Encrypted document storage
* Secure cloud deployment
* Automated security testing
* More detailed security analytics and monitoring

⸻

👩‍💻 Author

Anamika

BCA — Artificial Intelligence & Data Science
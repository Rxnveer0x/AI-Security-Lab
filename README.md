# AI Security Lab

A beginner-friendly AI security platform that combines a local AI chatbot with multiple security layers to detect, block, monitor, and test common AI security threats.

## 🚀 Project Overview

AI Security Lab is a security-focused AI application built with Python, Flask, and Ollama.

The project follows a **secure AI pipeline**:

```text
User Input
    ↓
Input Validation
    ↓
Prompt Injection Detection
    ↓
Jailbreak Detection
    ↓
PII Detection
    ↓
Risk Scoring
    ↓
RAG Security
    ↓
Secure Tool Execution
    ↓
Local AI Model (Ollama)
    ↓
Output Security
    ↓
Security Logging & Monitoring
🔐 Security Features
Input Security
Input validation
Empty input detection
Message length limits
Prompt injection detection
Jailbreak detection
PII detection
Risk scoring
AI Output Security
Sensitive information detection
API key detection
JWT detection
Private key detection
Password and secret detection
Output validation
RAG Security
Secure document loading
Document retrieval
RAG prompt-injection detection
Unsafe document blocking
Retrieved-document logging
AI Tool Security
Tool allowlisting
Tool request validation
Safe calculator tool
Unsafe tool blocking
Tool execution logging
Security Monitoring
Security event logging
Recent security events
Risk-level monitoring
Security summary dashboard
Security report generation
Attack Testing

The project includes automated tests for:

Prompt injection
Jailbreak attempts
PII detection
Sensitive output detection
RAG injection
Unsafe tool requests
Calculator tool execution
Advanced attack variations
🧠 AI Model

The project uses Ollama to run a local AI model.

This allows the chatbot to operate locally without requiring a paid external AI API.

🛠️ Tech Stack
Python
Flask
Ollama
HTML
CSS
JavaScript
Pytest
Git & GitHub
📁 Project Structure
AI-Security-Lab/
│
├── app/
│   ├── main.py
│   ├── ollama_client.py
│   ├── tools.py
│   ├── tool_executor.py
│   ├── tool_router.py
│   └── templates/
│       └── index.html
│
├── security/
│   ├── input_validator.py
│   ├── prompt_detector.py
│   ├── jailbreak_detector.py
│   ├── pii_detector.py
│   ├── risk_scorer.py
│   ├── output_security.py
│   ├── output_validator.py
│   ├── rag_security.py
│   ├── document_loader.py
│   ├── document_retriever.py
│   ├── rag_processor.py
│   ├── tool_security.py
│   ├── security_logger.py
│   ├── security_events.py
│   ├── security_monitor.py
│   └── security_report.py
│
├── tests/
│   ├── attack_tests.py
│   ├── ai_attack_suite.py
│   ├── advanced_attack_tests.py
│   └── security unit tests
│
├── data/
│   ├── documents/
│   └── reports/
│
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
⚙️ Installation

Clone the repository:

git clone https://github.com/Rxnveer0x/AI-Security-Lab.git
cd AI-Security-Lab

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Make sure Ollama is installed and a local model is available.

▶️ Running the Application

Start the Flask application:

python -m app.main

Then open:

http://127.0.0.1:5000
🧪 Running Security Tests

Run the security test suite:

python tests/run_security_tests.py

Run the attack test suite:

python tests/ai_attack_suite.py

Run the advanced attack tests:

python tests/advanced_attack_tests.py

Run all Pytest tests:

python -m pytest -v
📊 Security Dashboard

The application includes a security dashboard that provides visibility into:

Security events
Risk levels
Attack test results
Blocked requests
Tool security events
RAG security events
🎯 Project Goals

The main goal of this project is to understand how AI applications can be protected using multiple security layers.

The project focuses on practical AI security concepts including:

Prompt Injection
Jailbreaking
PII Protection
Secure RAG
AI Tool Security
Output Validation
Risk Scoring
Security Monitoring
Automated AI Attack Testing
⚠️ Disclaimer

This project is developed for educational and defensive security research purposes.

It is intended to demonstrate security concepts in AI applications and should not be used to attack systems without authorization.
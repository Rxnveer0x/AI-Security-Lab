# AI Security Lab

A local AI Security Lab for detecting, blocking, monitoring, and testing security threats in AI applications.

## Overview

AI Security Lab is a local AI security platform built with Python and Flask. It places security controls around an AI chatbot to detect suspicious input, protect sensitive information, secure RAG and tool usage, validate AI output, and monitor security events.

The project uses Ollama to run the AI model locally.

## Security Architecture

```text
User
  │
  ▼
Flask AI Application
  │
  ▼
Security Middleware
  │
  ├── Input Validation
  ├── Prompt Injection Detection
  ├── Jailbreak Detection
  ├── PII Detection
  ├── Risk Scoring
  ├── Rate Limiting
  │
  ▼
RAG / Tool Security
  │
  ├── Secure Document Retrieval
  └── Secure Tool Execution
  │
  ▼
Local AI Model
(Ollama)
  │
  ▼
Output Security
  │
  ├── PII Detection
  └── Sensitive Output Detection
  │
  ▼
Security Logging & Monitoring
  │
  ▼
Security Dashboard
Features
AI Security
Prompt injection detection
Jailbreak detection
PII detection
Risk scoring
Input validation
Rate limiting
Sensitive output detection
Output validation
RAG Security
Document loading
Document processing
Secure document retrieval
RAG injection detection and blocking
Tool Security
Secure calculator tool
Tool request routing
Tool input validation
Unsafe tool request blocking
Security Monitoring
Security event logging
Security event monitoring
Risk-level tracking
Security event filtering
Event pagination
Event details
JSON event export
CSV event export
Security report generation
Security Dashboard

The dashboard provides:

System status
Security summary
Threat overview
Security analytics
Risk-level statistics
Recent security events
Event filtering
Event details
Attack-test results
Security report download
Attack Testing

The project includes automated security testing for:

Prompt injection
Jailbreak attempts
PII detection
Sensitive output detection
RAG injection
Unsafe tool requests
Safe calculator execution
Additional advanced security cases

Security tests are also executed automatically using GitHub Actions.

Technology Stack
Python
Flask
Ollama
Qwen3 4B
Flask-Limiter
Pytest
HTML
CSS
JavaScript
Git
GitHub Actions
Project Structure
AI-Security-Lab/
│
├── app/
│   ├── main.py
│   ├── ollama_client.py
│   ├── tools.py
│   ├── tool_executor.py
│   ├── tool_router.py
│   └── templates/
│
├── security/
│   ├── input_validator.py
│   ├── prompt_detector.py
│   ├── jailbreak_detector.py
│   ├── pii_detector.py
│   ├── risk_scorer.py
│   ├── output_security.py
│   ├── output_validator.py
│   ├── security_logger.py
│   ├── security_monitor.py
│   ├── security_events.py
│   ├── security_report.py
│   ├── rag_security.py
│   ├── document_loader.py
│   ├── rag_processor.py
│   ├── document_retriever.py
│   └── tool_security.py
│
├── tests/
│   ├── ai_attack_suite.py
│   ├── advanced_attack_tests.py
│   ├── attack_tests.py
│   └── security tests
│
├── data/
│   ├── documents/
│   └── reports/
│
├── .github/
│   └── workflows/
│       └── security-tests.yml
│
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
Requirements
Python 3.14
Ollama
Git
Windows/Linux/macOS
Local Setup

Clone the repository:

git clone https://github.com/Rxnveer0x/AI-Security-Lab.git
cd AI-Security-Lab

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Ollama Setup

Install Ollama and make sure it is running.

Pull the model:

ollama pull qwen3:4b

Verify the model:

ollama list
Run the Application

Start the Flask application:

python -m app.main

The application will run at:

http://127.0.0.1:5000

Open the address in your browser.

Run Security Tests

Run the complete automated test suite:

python -m pytest -v

Run the AI attack suite:

python -m tests.ai_attack_suite
GitHub Actions

The project includes a GitHub Actions workflow that automatically runs the security test suite when changes are pushed to the master branch or submitted through a pull request.

Workflow:

.github/workflows/security-tests.yml
Security Reports

Security reports and attack-test results are stored under:

data/reports/

The application also provides security reports through the dashboard.

Security Event Monitoring

Security events are logged with information such as:

Timestamp
Event type
Message
Risk level
Security metadata

The dashboard provides filtering, pagination, event details, and export functionality.

Project Goal

The goal of this project is to understand how security controls can be designed around AI applications and LLM-based systems.

The project focuses on defensive AI security concepts including:

LLM security
Prompt injection
Jailbreak detection
PII protection
RAG security
Tool security
Output security
Security monitoring
Automated security testing
Author

Ranveer Singh

GitHub:

https://github.com/Rxnveer0x/AI-Security-Lab


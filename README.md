# AI Security Lab

A local AI Security Lab for detecting, blocking, monitoring, and testing security threats in AI applications.

---

## Overview

AI Security Lab is a local AI security platform built with **Python and Flask**.

It places security controls around an AI chatbot to:

- Detect suspicious input
- Detect prompt injection attacks
- Detect jailbreak attempts
- Protect sensitive information
- Secure RAG and tool usage
- Validate AI output
- Monitor security events
- Test AI security controls

The project uses **Ollama** to run the AI model locally.

---

## Security Architecture

<p align="center">
  <img src="docs/architecture.svg" alt="AI Security Lab Architecture" width="100%">
</p>



## Features

### AI Security

- Prompt injection detection
- Jailbreak detection
- PII detection
- Risk scoring
- Input validation
- Rate limiting
- Sensitive output detection
- Output validation

### RAG Security

- Document loading
- Document processing
- Secure document retrieval
- RAG injection detection
- RAG injection blocking

### Tool Security

- Secure calculator tool
- Tool request routing
- Tool input validation
- Unsafe tool request blocking

### Security Monitoring

- Security event logging
- Security event monitoring
- Risk-level tracking
- Security event filtering
- Event pagination
- Event details
- JSON event export
- CSV event export
- Security report generation

---

## Security Dashboard

The Security Dashboard provides a web-based interface for monitoring the security status of the AI application.
## Security Demonstration

The AI Security Lab protects a local AI application through multiple security layers.

## Project Screenshots

### Security Dashboard

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="AI Security Dashboard" width="100%">
</p>

### Security Event Details

<p align="center">
  <img src="docs/screenshots/security-event-details.png" alt="Security Event Details" width="100%">
</p>

### Normal Request

A legitimate request is processed by the AI application.

```text
User Request
     ↓
Input Security
     ↓
Risk Assessment
     ↓
Ollama / Qwen3 4B
     ↓
Output Security
     ↓
Response
```

### Prompt Injection

Suspicious prompt-injection requests are detected and blocked before reaching the AI model.

```text
Malicious Request
        ↓
Prompt Injection Detection
        ↓
Risk Scoring
        ↓
Request Blocked
        ↓
Security Event Logged
```

### Jailbreak Detection

Jailbreak-style requests are analyzed by the security middleware and blocked when detected.

```text
Jailbreak Attempt
        ↓
Jailbreak Detection
        ↓
HIGH Risk
        ↓
Request Blocked
        ↓
Security Event Logged
```

### PII Detection

Requests containing sensitive personal information are detected and blocked.

```text
User Input
    ↓
PII Detection
    ↓
Sensitive Information Found
    ↓
Request Blocked
    ↓
Security Event Logged
```

### Security Monitoring

All important security events are recorded and displayed through the dashboard.

```text
Security Event
      ↓
Security Logger
      ↓
Security Monitoring
      ↓
Security Dashboard
```

### Dashboard Features

- System status
- Security summary
- Threat overview
- Security analytics
- Risk-level statistics
- Recent security events
- Event filtering
- Event pagination
- Event details
- Attack-test results
- JSON event export
- CSV event export
- Security report download

---

## Attack Testing

The project includes automated security testing for different AI security threats.

### Attack Tests

- Prompt injection
- Jailbreak attempts
- PII detection
- Sensitive output detection
- RAG injection
- Unsafe tool requests
- Safe calculator execution
- Additional advanced security cases

Security tests are also executed automatically using **GitHub Actions**.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application and API |
| Ollama | Local AI model runtime |
| Qwen3 4B | Local language model |
| Flask-Limiter | Rate limiting |
| Pytest | Automated testing |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Dashboard functionality |
| Git | Version control |
| GitHub Actions | Automated security testing |

---

## Project Structure

```text
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
```

---

## Requirements

Before running the project, install:

- Python 3.14
- Ollama
- Git

### Supported Operating Systems

- Windows
- Linux
- macOS

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Rxnveer0x/AI-Security-Lab.git
```

```bash
cd AI-Security-Lab
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

Install **Ollama** and make sure it is running.

### Pull the AI Model

```bash
ollama pull qwen3:4b
```

### Verify the Model

```bash
ollama list
```

The model should appear in the list.

---

## Run the Application

Start the Flask application:

```bash
python -m app.main
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## Run Security Tests

### Complete Test Suite

Run all automated tests:

```bash
python -m pytest -v
```

### AI Attack Suite

Run the AI security attack tests:

```bash
python -m tests.ai_attack_suite
```

### Advanced Attack Tests

```bash
python -m tests.advanced_attack_tests
```

---

## GitHub Actions

The project includes a GitHub Actions workflow for automated security testing.

The workflow runs when:

- Code is pushed to the `master` branch
- A pull request is created for the `master` branch

### Workflow File

```text
.github/workflows/security-tests.yml
```

The workflow installs the project dependencies and runs the automated test suite.

---

## Security Reports

Security reports and attack-test results are stored in:

```text
data/reports/
```

The project can generate security reports containing information about detected security events and attack-test results.

---

## Security Event Monitoring

Security events are recorded with information such as:

- Timestamp
- Event type
- Message
- Risk level
- Security metadata

The dashboard provides tools for viewing and analyzing these events.

### Event Management

- Event filtering
- Event pagination
- Event details
- JSON export
- CSV export
- Security report generation

---

## Security Controls

The application implements security controls at multiple stages of the AI request lifecycle.

### Input Security

```text
User Input
    │
    ├── Input Validation
    ├── Prompt Injection Detection
    ├── Jailbreak Detection
    ├── PII Detection
    ├── Risk Scoring
    └── Rate Limiting
```

### RAG and Tool Security

```text
Request
   │
   ├── RAG Security
   │      ├── Document Processing
   │      ├── Document Retrieval
   │      └── RAG Injection Detection
   │
   └── Tool Security
          ├── Tool Routing
          ├── Input Validation
          └── Unsafe Tool Blocking
```

### Output Security

```text
AI Response
    │
    ├── Output Validation
    ├── PII Detection
    └── Sensitive Output Detection
```

---

## Project Goal

The goal of this project is to understand how security controls can be designed around AI applications and LLM-based systems.

The project focuses on defensive AI security concepts including:

- LLM security
- Prompt injection
- Jailbreak detection
- PII protection
- RAG security
- Tool security
- Output security
- Security monitoring
- Automated security testing

---

## Learning Focus

This project provides practical experience with:

- AI application security
- LLM security
- Secure AI architecture
- Prompt injection defense
- Jailbreak detection
- PII protection
- RAG security
- Tool security
- Output security
- Security monitoring
- Automated security testing
- Python security development
- Flask application security

---

## Author

**Ranveer Singh**

---

## GitHub

**Repository:**

https://github.com/Rxnveer0x/AI-Security-Lab

---

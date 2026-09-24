# AI Security Lab

A local AI security project built to understand how AI applications can be protected from common security threats.

The project started as a simple local AI chatbot and was gradually extended with security checks around the AI request and response flow.

---

## What is this project?

This project is a Flask-based local AI application using Ollama and Qwen3 4B.

Instead of sending requests directly to the AI model, the application checks them through different security layers first.

The main things I worked on are:

- Prompt injection detection
- Jailbreak detection
- PII detection
- Risk scoring
- Input validation
- Rate limiting
- RAG security
- Tool security
- Output security
- Security logging
- Security monitoring
- Automated security testing

The AI model runs locally through Ollama.

---

## How it works

The basic request flow is:

```text
User
  ↓
Flask API
  ↓
Input Security
  ↓
RAG Security / Tool Security
  ↓
Ollama / Qwen3 4B
  ↓
Output Security
  ↓
Logging & Monitoring
  ↓
Security Dashboard
```

The idea is to check the request before it reaches the model and also check the model's response before returning it to the user.

---

## Security Features

### Input Security

The application checks user input for different types of problems.

- Input validation
- Prompt injection detection
- Jailbreak detection
- PII detection
- Risk scoring
- Rate limiting

For example, a prompt-injection attempt can be blocked before it reaches the AI model.

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

### RAG Security

The project also includes basic security checks for retrieved documents.

It can:

- Load documents
- Process documents
- Retrieve relevant documents
- Check retrieved content for malicious instructions
- Block unsafe RAG content

```text
Document
   ↓
Document Processing
   ↓
Document Retrieval
   ↓
RAG Security Check
   ↓
Safe → Continue
Unsafe → Block
```

### Tool Security

The application has a calculator tool to demonstrate how AI tools can be controlled.

Tool requests go through validation before execution.

```text
User Request
     ↓
Tool Router
     ↓
Tool Validation
     ↓
Safe Tool Request?
   ↙          ↘
 Yes          No
  ↓            ↓
Execute       Block
```

The calculator only accepts allowed mathematical expressions instead of directly executing arbitrary input.

### Output Security

The AI response is also checked before it is returned.

The output security layer checks for:

- PII
- API keys
- AWS access keys
- Password-like values
- Other sensitive output patterns

```text
AI Response
     ↓
Output Validation
     ↓
PII Detection
     ↓
Sensitive Output Detection
     ↓
Response
```

---

## Security Dashboard

The project includes a web dashboard for viewing security activity.

It currently shows:

- System status
- Security summary
- Threat overview
- Security analytics
- Risk levels
- Recent security events
- Event filtering
- Event pagination
- Event details
- Attack-test results

There are also options to export events as JSON or CSV and generate a security report.

---

## Screenshots

### Security Dashboard

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="AI Security Dashboard" width="100%">
</p>

### Security Event Details

<p align="center">
  <img src="docs/screenshots/security-event-details.png" alt="Security Event Details" width="100%">
</p>

---

## Security Testing

I added automated tests for the main security components of the project.

The tests cover areas such as:

- Jailbreak detection
- PII detection
- Prompt injection and RAG security
- Risk scoring
- Output security
- Sensitive output detection
- Tool routing
- Tool security
- Calculator validation

The complete pytest suite currently has:

```text
44 passed in 2.44s
```

There are also separate attack-testing scripts for testing AI security cases.

### Run all tests

```bash
python -m pytest -v
```

### Run the AI attack suite

```bash
python -m tests.ai_attack_suite
```

### Run the advanced attack tests

```bash
python -m tests.advanced_attack_tests
```

---

## GitHub Actions

The project uses GitHub Actions to run the automated test suite.

The workflow is located at:

```text
.github/workflows/security-tests.yml
```

It runs when code is pushed to `master` or when a pull request is created for the `master` branch.

---

## Technology Used

| Technology | Used for |
|---|---|
| Python | Main programming language |
| Flask | API and web application |
| Ollama | Running the AI model locally |
| Qwen3 4B | Local AI model |
| Flask-Limiter | Rate limiting |
| Pytest | Testing |
| HTML / CSS / JavaScript | Security dashboard |
| Git | Version control |
| GitHub Actions | Automated testing |

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
│   ├── test_chat.py
│   ├── test_security.py
│   ├── test_jailbreak_detector.py
│   ├── test_output_security.py
│   ├── test_output_validator.py
│   ├── test_pii_detector.py
│   ├── test_rag_security.py
│   ├── test_risk_scorer.py
│   ├── test_tool_router.py
│   ├── test_tool_security.py
│   ├── test_tools.py
│   ├── ai_attack_suite.py
│   ├── advanced_attack_tests.py
│   └── attack_tests.py
│
├── data/
│   ├── documents/
│   └── reports/
│
├── docs/
│   ├── architecture.svg
│   └── screenshots/
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

## Setup

### Requirements

You need:

- Python 3.14
- Ollama
- Git

### Clone the project

```bash
git clone https://github.com/Rxnveer0x/AI-Security-Lab.git
cd AI-Security-Lab
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama

Install Ollama and make sure it is running.

Pull the model:

```bash
ollama pull qwen3:4b
```

Check that it is installed:

```bash
ollama list
```

You should see:

```text
qwen3:4b
```

---

## Run the Project

Start the Flask application:

```bash
python -m app.main
```

Then open:

```text
http://127.0.0.1:5000
```

---

## Reports

Security reports and attack-test results are stored in:

```text
data/reports/
```

The application also records security events with information such as:

- Timestamp
- Event type
- Message
- Risk level
- Metadata

These events are displayed in the dashboard.

---

## Why I Built This

I wanted to learn more about AI security instead of only building a normal chatbot.

While working on the project, I focused on what happens around an AI model:

```text
Input
  ↓
Security Checks
  ↓
AI Model
  ↓
Output Checks
  ↓
Logging
```

This helped me work with concepts such as prompt injection, jailbreaks, PII protection, RAG security, tool security, and LLM output validation.

---

## What I Learned

Through this project I practiced:

- Python
- Flask
- Working with local LLMs
- Prompt injection detection
- Jailbreak detection
- PII detection
- Risk scoring
- RAG security
- Tool validation
- Output security
- Security logging
- Building a security dashboard
- Writing automated tests
- Git and GitHub
- GitHub Actions

---

## Author

**Ranveer Singh**

GitHub:  
https://github.com/Rxnveer0x/AI-Security-Lab
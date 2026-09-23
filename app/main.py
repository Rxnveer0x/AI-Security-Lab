import json

from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.tool_router import route_tool_request
from app.ollama_client import ask_ollama

from security.document_retriever import retrieve_documents

from security.input_validator import validate_input
from security.prompt_detector import detect_prompt_injection
from security.jailbreak_detector import detect_jailbreak
from security.pii_detector import detect_pii
from security.risk_scorer import calculate_risk_score

from security.output_security import check_output
from security.output_validator import validate_output

from security.security_logger import log_security_event
from security.security_monitor import get_security_summary
from security.security_events import get_recent_events


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# RATE LIMITER
# ============================================================

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)


# ============================================================
# FRONTEND
# ============================================================

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ============================================================
# SECURITY SUMMARY API
# ============================================================

@app.route("/security-summary", methods=["GET"])
def security_summary():

    return jsonify(
        get_security_summary()
    )


# ============================================================
# ATTACK TEST REPORT API
# ============================================================

@app.route("/attack-test-report", methods=["GET"])
def attack_test_report():

    report_file = "data/reports/attack_test_report.json"

    try:

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)

        return jsonify(report), 200

    except FileNotFoundError:

        return jsonify({
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "tests": [],
            "error": "Attack test report not found."
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# CHAT API
# ============================================================

@app.route("/chat", methods=["POST"])
@limiter.limit("5 per minute")
def chat():

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        data = request.get_json(force=True)

    except Exception as error:

        print(
            "JSON ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "INVALID_JSON"
        )

        return jsonify({
            "response": "Invalid JSON data.",
            "status": "blocked"
        }), 400


    # --------------------------------------------------------
    # Validate Current Message
    # --------------------------------------------------------

    is_valid, validation_message = validate_input(
        data
    )

    if not is_valid:

        log_security_event(
            validation_message,
            "INPUT_BLOCKED"
        )

        return jsonify({
            "response": validation_message,
            "status": "blocked"
        }), 400


    user_input = data["message"].strip()


    # ========================================================
    # SECURITY: PROMPT INJECTION DETECTION
    # ========================================================

    try:

        injection_detected = detect_prompt_injection(
            user_input
        )

    except Exception as error:

        print(
            "PROMPT DETECTOR ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "DETECTOR_ERROR"
        )

        return jsonify({
            "response": "Security check failed.",
            "status": "error"
        }), 500


    if injection_detected:

        risk_result = calculate_risk_score(
            prompt_injection=True,
            pii_detected=[]
        )

        log_security_event(
            "Prompt injection attempt detected",
            "PROMPT_INJECTION",
            risk_level=risk_result["risk_level"],
            metadata={
                "risk_score": risk_result["score"],
                "category": "Prompt Injection"
            }
        )

        return jsonify({
            "response": "Request blocked by security controls.",
            "status": "blocked",
            "risk_score": risk_result["score"],
            "risk_level": risk_result["risk_level"]
        }), 403


    # ========================================================
    # SECURITY: JAILBREAK DETECTION
    # ========================================================

    try:

        jailbreak_detected = detect_jailbreak(
            user_input
        )

    except Exception as error:

        print(
            "JAILBREAK DETECTOR ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "JAILBREAK_DETECTOR_ERROR"
        )

        return jsonify({
            "response": "Security check failed.",
            "status": "error"
        }), 500


    if jailbreak_detected:

        log_security_event(
            "Jailbreak attempt detected",
            "JAILBREAK_DETECTED",
            risk_level="HIGH",
            metadata={
                "risk_score": 80,
                "category": "Jailbreak Detection"
            }
        )

        return jsonify({
            "response": (
                "Request blocked by security controls "
                "because a jailbreak attempt was detected."
            ),
            "status": "blocked",
            "risk_score": 80,
            "risk_level": "HIGH"
        }), 403


    # ========================================================
    # SECURITY: PII DETECTION
    # ========================================================

    try:

        pii_detected = detect_pii(
            user_input
        )

    except Exception as error:

        print(
            "PII DETECTOR ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "PII_DETECTOR_ERROR"
        )

        return jsonify({
            "response": "Security check failed.",
            "status": "error"
        }), 500


    # ========================================================
    # SECURITY: RISK SCORING
    # ========================================================

    risk_result = calculate_risk_score(
        prompt_injection=False,
        pii_detected=pii_detected
    )

    risk_score = risk_result["score"]
    risk_level = risk_result["risk_level"]


    # --------------------------------------------------------
    # Block PII
    # --------------------------------------------------------

    if pii_detected:

        log_security_event(
            "Sensitive information detected",
            "PII_DETECTED",
            risk_level=risk_level,
            metadata={
                "risk_score": risk_score,
                "pii_types": ", ".join(pii_detected),
                "category": "PII Protection"
            }
        )

        return jsonify({
            "response": (
                "Sensitive information detected. "
                "Please remove personal information "
                "and try again."
            ),
            "status": "blocked",
            "risk_score": risk_score,
            "risk_level": risk_level
        }), 400


    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    history = data.get(
        "history",
        []
    )

    if not isinstance(history, list):

        history = []


    # Keep only recent messages

    history = history[-20:]


    # --------------------------------------------------------
    # Validate History
    # --------------------------------------------------------

    clean_history = []

    for item in history:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role not in [
            "user",
            "assistant"
        ]:
            continue

        if not isinstance(content, str):
            continue

        content = content.strip()

        if not content:
            continue

        # Prevent extremely large history messages

        if len(content) > 4000:

            content = content[:4000]

        clean_history.append({
            "role": role,
            "content": content
        })


    # ========================================================
    # SECURE TOOL REQUEST
    # ========================================================

    try:

        tool_result = route_tool_request(
            user_input
        )

        if tool_result is not None:

            if tool_result.get("success"):

                result = tool_result.get(
                    "result"
                )

                log_security_event(
                    f"Tool: calculator | Result: {result}",
                    "TOOL_EXECUTED"
                )

                return jsonify({
                    "response": str(result),
                    "status": "success",
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "tool_used": "calculator"
                }), 200

            log_security_event(
                tool_result.get(
                    "error",
                    "Tool execution failed."
                ),
                "TOOL_EXECUTION_BLOCKED"
            )

            return jsonify({
                "response": tool_result.get(
                    "error",
                    "Tool execution failed."
                ),
                "status": "blocked",
                "risk_score": 80,
                "risk_level": "HIGH"
            }), 403

    except Exception as error:

        print(
            "TOOL ROUTER ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "TOOL_ROUTER_ERROR"
        )


    # ========================================================
    # RAG DOCUMENT RETRIEVAL
    # ========================================================

    try:

        retrieved_documents = retrieve_documents(
            user_input,
            top_k=3
        )

        rag_context_parts = []

        for document in retrieved_documents:

            rag_context_parts.append(
                f"Document: {document['name']}\n"
                f"{document['content']}"
            )

        rag_context = "\n\n".join(
            rag_context_parts
        )

    except Exception as error:

        print(
            "RAG RETRIEVAL ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "RAG_RETRIEVAL_ERROR"
        )

        rag_context = ""


    # ========================================================
    # ASK LOCAL AI
    # ========================================================

    try:

        ai_response = ask_ollama(
            user_input,
            clean_history,
            rag_context
        )

    except Exception as error:

        print(
            "OLLAMA ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "AI_ERROR"
        )

        return jsonify({
            "response": "AI service is currently unavailable.",
            "status": "error"
        }), 500


    # ========================================================
    # OUTPUT SECURITY
    # ========================================================

    # --------------------------------------------------------
    # Output Security: PII Detection
    # --------------------------------------------------------

    try:

        output_has_pii, output_pii = check_output(
            ai_response
        )

    except Exception as error:

        print(
            "OUTPUT SECURITY ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "OUTPUT_SECURITY_ERROR"
        )

        return jsonify({
            "response": "Output security check failed.",
            "status": "error"
        }), 500


    # --------------------------------------------------------
    # Block PII in AI Output
    # --------------------------------------------------------

    if output_has_pii:

        print(
            "OUTPUT PII BLOCKED:",
            output_pii
        )

        log_security_event(
            f"Output PII detected: {', '.join(output_pii)}",
            "OUTPUT_PII_DETECTED",
            risk_level="HIGH"
        )

        return jsonify({
            "response": (
                "The AI response was blocked "
                "by output security controls."
            ),
            "status": "blocked",
            "risk_score": 80,
            "risk_level": "HIGH",
            "output_findings": output_pii
        }), 403


    # --------------------------------------------------------
    # Output Security: Sensitive Information
    # --------------------------------------------------------

    try:

        output_safe, output_findings = validate_output(
            ai_response
        )

    except Exception as error:

        print(
            "OUTPUT VALIDATOR ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "OUTPUT_VALIDATOR_ERROR"
        )

        return jsonify({
            "response": "Output security check failed.",
            "status": "error"
        }), 500


    # --------------------------------------------------------
    # Block Sensitive Output
    # --------------------------------------------------------

    if not output_safe:

        print(
            "SENSITIVE OUTPUT BLOCKED:",
            output_findings
        )

        log_security_event(
            f"Sensitive output detected: "
            f"{', '.join(output_findings)}",
            "OUTPUT_BLOCKED",
            risk_level="HIGH"
        )

        return jsonify({
            "response": (
                "The AI response was blocked "
                "because sensitive information "
                "was detected."
            ),
            "status": "blocked",
            "risk_score": 80,
            "risk_level": "HIGH",
            "output_findings": output_findings
        }), 403


    # ========================================================
    # LOG SUCCESSFUL REQUEST
    # ========================================================

    log_security_event(
        "Request allowed",
        "ALLOWED",
        risk_level=risk_level,
        metadata={
            "risk_score": risk_score,
            "category": "Normal Request"
        }
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return jsonify({
        "response": ai_response,
        "status": "success",
        "risk_score": risk_score,
        "risk_level": risk_level
    }), 200


# ============================================================
# RATE LIMIT ERROR
# ============================================================

@app.errorhandler(429)
def handle_rate_limit(error):

    log_security_event(
        "Rate limit exceeded",
        "RATE_LIMITED",
        risk_level="MEDIUM",
        metadata={
            "source": "Flask-Limiter",
            "category": "Availability Protection",
            "limit": "5 per minute"
        }
    )

    return jsonify({
        "response": "Too many requests. Please try again later.",
        "status": "rate_limited",
        "risk_level": "MEDIUM",
        "security_category": "Availability Protection"
    }), 429


# ============================================================
# SECURITY EVENTS API
# ============================================================

@app.route("/security-events", methods=["GET"])
def security_events():

    events = get_recent_events(
        20
    )

    return jsonify({
        "events": events
    }), 200


# ============================================================
# SECURITY REPORT API
# ============================================================

@app.route("/security-report", methods=["GET"])
def security_report():

    try:

        from security.security_report import generate_security_report

        report_path = generate_security_report()

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            report = file.read()

        return jsonify({
            "status": "success",
            "report": report
        }), 200

    except Exception as error:

        print(
            "SECURITY REPORT ERROR:",
            repr(error)
        )

        log_security_event(
            str(error),
            "SECURITY_REPORT_ERROR"
        )

        return jsonify({
            "status": "error",
            "message": "Security report could not be generated."
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
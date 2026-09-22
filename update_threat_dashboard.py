from pathlib import Path

FILE = Path("app/templates/index.html")

html = FILE.read_text(encoding="utf-8")


# =========================================================
# 1. ADD THREAT OVERVIEW CSS
# =========================================================

css_marker = """
        /* =========================================================
           EVENT LIST
        ========================================================= */
"""

css_code = """
        /* =========================================================
           THREAT OVERVIEW
        ========================================================= */

        .threat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .threat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px;
        }

        .threat-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
        }

        .threat-name {
            color: var(--text-secondary);
            font-size: 9px;
            line-height: 1.3;
        }

        .threat-count {
            font-size: 16px;
            font-weight: 600;
        }

        .threat-indicator {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--text-muted);
        }

        .threat-card.active .threat-indicator {
            background: var(--red);
        }

        .threat-card.active .threat-count {
            color: var(--red);
        }

        .threat-card.warning .threat-indicator {
            background: var(--yellow);
        }

        .threat-card.warning .threat-count {
            color: var(--yellow);
        }

        .threat-card.safe .threat-indicator {
            background: var(--green);
        }

        .threat-card.safe .threat-count {
            color: var(--green);
        }

"""

if ".threat-grid {" not in html:

    if css_marker not in html:
        raise SystemExit("Threat CSS marker not found.")

    html = html.replace(
        css_marker,
        css_code + css_marker,
        1
    )


# =========================================================
# 2. ADD THREAT OVERVIEW HTML
# =========================================================

html_marker = """
            <!-- =================================================
                 RISK LEVELS
            ================================================== -->
"""

threat_html = """
            <!-- =================================================
                 THREAT OVERVIEW
            ================================================== -->

            <section class="dashboard-section">

                <div class="section-heading">
                    Threat Overview
                </div>

                <div class="threat-grid">

                    <div
                        class="threat-card"
                        id="threatPromptInjection"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                Prompt Injection
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatPromptInjectionCount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatJailbreak"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                Jailbreak Detection
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatJailbreakCount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatPII"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                PII Detection
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatPIICount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatRAG"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                RAG Injection
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatRAGCount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatBlocked"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                Input Blocked
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatBlockedCount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatRateLimit"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                Rate Limited
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatRateLimitCount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatOutput"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                Output Security
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatOutputCount"
                        >
                            -
                        </div>
                    </div>


                    <div
                        class="threat-card"
                        id="threatErrors"
                    >
                        <div class="threat-card-header">
                            <div class="threat-name">
                                AI Errors
                            </div>

                            <div class="threat-indicator"></div>
                        </div>

                        <div
                            class="threat-count"
                            id="threatErrorsCount"
                        >
                            -
                        </div>
                    </div>

                </div>

            </section>


"""

if 'id="threatPromptInjection"' not in html:

    if html_marker not in html:
        raise SystemExit("Threat HTML marker not found.")

    html = html.replace(
        html_marker,
        threat_html + html_marker,
        1
    )


# =========================================================
# 3. UPDATE SECURITY SUMMARY FUNCTION
# =========================================================

old_summary_end = """
    document.getElementById(
        "lowRisk"
    ).textContent =
        risks.LOW ?? 0;

}
"""

new_summary_end = """
    document.getElementById(
        "lowRisk"
    ).textContent =
        risks.LOW ?? 0;


    /* =====================================================
       THREAT OVERVIEW
    ===================================================== */

    updateThreatCard(
        "threatPromptInjection",
        "threatPromptInjectionCount",
        events.PROMPT_INJECTION ?? 0,
        "danger"
    );


    updateThreatCard(
        "threatJailbreak",
        "threatJailbreakCount",
        events.JAILBREAK_DETECTED ?? 0,
        "danger"
    );


    updateThreatCard(
        "threatPII",
        "threatPIICount",
        events.PII_DETECTED ?? 0,
        "warning"
    );


    updateThreatCard(
        "threatRAG",
        "threatRAGCount",
        events.RAG_INJECTION_BLOCKED ?? 0,
        "warning"
    );


    updateThreatCard(
        "threatBlocked",
        "threatBlockedCount",
        events.INPUT_BLOCKED ?? 0,
        "warning"
    );


    updateThreatCard(
        "threatRateLimit",
        "threatRateLimitCount",
        events.RATE_LIMITED ?? 0,
        "danger"
    );


    const outputSecurity =
        (events.OUTPUT_PII_DETECTED ?? 0) +
        (events.OUTPUT_BLOCKED ?? 0);


    updateThreatCard(
        "threatOutput",
        "threatOutputCount",
        outputSecurity,
        "warning"
    );


    updateThreatCard(
        "threatErrors",
        "threatErrorsCount",
        events.AI_ERROR ?? 0,
        "danger"
    );

}
"""

if "threatPromptInjectionCount" not in html:
    if old_summary_end not in html:
        raise SystemExit("Security summary ending not found.")

    html = html.replace(
        old_summary_end,
        new_summary_end,
        1
    )


# =========================================================
# 4. ADD THREAT CARD FUNCTION
# =========================================================

function_marker = """
/* ============================================================
   LOAD ATTACK TEST REPORT
============================================================ */
"""

threat_function = """
/* ============================================================
   UPDATE THREAT CARD
============================================================ */

function updateThreatCard(
    cardId,
    countId,
    count,
    severity
) {

    const card =
        document.getElementById(cardId);

    const countElement =
        document.getElementById(countId);

    if (!card || !countElement) {
        return;
    }

    countElement.textContent =
        count;


    card.classList.remove(
        "active",
        "warning",
        "safe"
    );


    if (count === 0) {

        card.classList.add(
            "safe"
        );

        return;
    }


    if (severity === "danger") {

        card.classList.add(
            "active"
        );

    }

    else {

        card.classList.add(
            "warning"
        );

    }

}


/* ============================================================
   LOAD ATTACK TEST REPORT
============================================================ */
"""

if "function updateThreatCard(" not in html:

    if function_marker not in html:
        raise SystemExit("Attack report marker not found.")

    html = html.replace(
        function_marker,
        threat_function,
        1
    )


# =========================================================
# 5. SAVE
# =========================================================

FILE.write_text(
    html,
    encoding="utf-8"
)

print()
print("=" * 60)
print("THREAT OVERVIEW UPDATE COMPLETE")
print("=" * 60)
print()
print("Added:")
print("- Prompt Injection")
print("- Jailbreak Detection")
print("- PII Detection")
print("- RAG Injection")
print("- Input Blocking")
print("- Rate Limiting")
print("- Output Security")
print("- AI Errors")
print()
print("File updated:")
print(FILE)
print()
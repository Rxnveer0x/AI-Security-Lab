from pathlib import Path

FILE = Path("app/templates/index.html")

html = FILE.read_text(encoding="utf-8")


# =========================================================
# 1. ANALYTICS CSS
# =========================================================

css_marker = """
        /* =========================================================
           EVENT LIST
        ========================================================= */
"""

css_code = """
        /* =========================================================
           SECURITY ANALYTICS
        ========================================================= */

        .analytics-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
        }

        .analytics-row {
            display: flex;
            align-items: center;
            gap: 9px;
            margin-bottom: 10px;
        }

        .analytics-row:last-child {
            margin-bottom: 0;
        }

        .analytics-label {
            width: 105px;
            flex-shrink: 0;
            color: var(--text-secondary);
            font-size: 9px;
        }

        .analytics-bar-container {
            flex: 1;
            height: 7px;
            background: var(--bg-input);
            border-radius: 10px;
            overflow: hidden;
        }

        .analytics-bar {
            height: 100%;
            width: 0%;
            border-radius: 10px;
            background: var(--blue);
            transition: width 0.35s ease;
        }

        .analytics-bar.danger {
            background: var(--red);
        }

        .analytics-bar.warning {
            background: var(--yellow);
        }

        .analytics-bar.safe {
            background: var(--green);
        }

        .analytics-value {
            width: 25px;
            text-align: right;
            color: var(--text);
            font-size: 9px;
            font-weight: 600;
        }

        .analytics-total {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 13px;
        }

        .analytics-total-label {
            color: var(--text-secondary);
            font-size: 10px;
        }

        .analytics-total-value {
            color: var(--text);
            font-size: 18px;
            font-weight: 600;
        }

"""

if ".analytics-card {" not in html:

    if css_marker not in html:
        raise SystemExit("Analytics CSS marker not found.")

    html = html.replace(
        css_marker,
        css_code + css_marker,
        1
    )


# =========================================================
# 2. ANALYTICS HTML
# =========================================================

html_marker = """
            <!-- =================================================
                 RISK LEVELS
            ================================================== -->
"""

analytics_html = """
            <!-- =================================================
                 SECURITY ANALYTICS
            ================================================== -->

            <section class="dashboard-section">

                <div class="section-heading">
                    Security Analytics
                </div>

                <div class="analytics-card">

                    <div class="analytics-total">

                        <div class="analytics-total-label">
                            Total Security Events
                        </div>

                        <div
                            class="analytics-total-value"
                            id="analyticsTotal"
                        >
                            -
                        </div>

                    </div>


                    <div class="analytics-row">

                        <div class="analytics-label">
                            Allowed
                        </div>

                        <div class="analytics-bar-container">
                            <div
                                class="analytics-bar safe"
                                id="analyticsAllowedBar"
                            ></div>
                        </div>

                        <div
                            class="analytics-value"
                            id="analyticsAllowed"
                        >
                            -
                        </div>

                    </div>


                    <div class="analytics-row">

                        <div class="analytics-label">
                            Prompt Injection
                        </div>

                        <div class="analytics-bar-container">
                            <div
                                class="analytics-bar danger"
                                id="analyticsPromptBar"
                            ></div>
                        </div>

                        <div
                            class="analytics-value"
                            id="analyticsPrompt"
                        >
                            -
                        </div>

                    </div>


                    <div class="analytics-row">

                        <div class="analytics-label">
                            PII Detected
                        </div>

                        <div class="analytics-bar-container">
                            <div
                                class="analytics-bar warning"
                                id="analyticsPIIBar"
                            ></div>
                        </div>

                        <div
                            class="analytics-value"
                            id="analyticsPII"
                        >
                            -
                        </div>

                    </div>


                    <div class="analytics-row">

                        <div class="analytics-label">
                            Input Blocked
                        </div>

                        <div class="analytics-bar-container">
                            <div
                                class="analytics-bar warning"
                                id="analyticsBlockedBar"
                            ></div>
                        </div>

                        <div
                            class="analytics-value"
                            id="analyticsBlocked"
                        >
                            -
                        </div>

                    </div>


                    <div class="analytics-row">

                        <div class="analytics-label">
                            Rate Limited
                        </div>

                        <div class="analytics-bar-container">
                            <div
                                class="analytics-bar danger"
                                id="analyticsRateBar"
                            ></div>
                        </div>

                        <div
                            class="analytics-value"
                            id="analyticsRate"
                        >
                            -
                        </div>

                    </div>


                    <div class="analytics-row">

                        <div class="analytics-label">
                            RAG Injection
                        </div>

                        <div class="analytics-bar-container">
                            <div
                                class="analytics-bar warning"
                                id="analyticsRAGBar"
                            ></div>
                        </div>

                        <div
                            class="analytics-value"
                            id="analyticsRAG"
                        >
                            -
                        </div>

                    </div>

                </div>

            </section>


"""

if 'id="analyticsTotal"' not in html:

    if html_marker not in html:
        raise SystemExit("Analytics HTML marker not found.")

    html = html.replace(
        html_marker,
        analytics_html + html_marker,
        1
    )


# =========================================================
# 3. UPDATE SUMMARY FUNCTION
# =========================================================

summary_marker = """
    document.getElementById(
        "lowRisk"
    ).textContent =
        risks.LOW ?? 0;
"""

analytics_call = """
    document.getElementById(
        "lowRisk"
    ).textContent =
        risks.LOW ?? 0;


    updateSecurityAnalytics(
        events,
        data.total_events ?? 0
    );
"""

if "updateSecurityAnalytics(" not in html:

    if summary_marker not in html:
        raise SystemExit("Summary marker not found.")

    html = html.replace(
        summary_marker,
        analytics_call,
        1
    )


# =========================================================
# 4. ADD ANALYTICS JAVASCRIPT
# =========================================================

function_marker = """
/* ============================================================
   LOAD ATTACK TEST REPORT
============================================================ */
"""

analytics_function = """
/* ============================================================
   SECURITY ANALYTICS
============================================================ */

function updateSecurityAnalytics(
    events,
    totalEvents
) {

    const total =
        Number(totalEvents) || 0;


    document.getElementById(
        "analyticsTotal"
    ).textContent =
        total;


    const allowed =
        Number(events.ALLOWED ?? 0);

    const promptInjection =
        Number(events.PROMPT_INJECTION ?? 0);

    const pii =
        Number(events.PII_DETECTED ?? 0);

    const blocked =
        Number(events.INPUT_BLOCKED ?? 0);

    const rateLimited =
        Number(events.RATE_LIMITED ?? 0);

    const rag =
        Number(events.RAG_INJECTION_BLOCKED ?? 0);


    setAnalyticsValue(
        "analyticsAllowed",
        "analyticsAllowedBar",
        allowed,
        total
    );


    setAnalyticsValue(
        "analyticsPrompt",
        "analyticsPromptBar",
        promptInjection,
        total
    );


    setAnalyticsValue(
        "analyticsPII",
        "analyticsPIIBar",
        pii,
        total
    );


    setAnalyticsValue(
        "analyticsBlocked",
        "analyticsBlockedBar",
        blocked,
        total
    );


    setAnalyticsValue(
        "analyticsRate",
        "analyticsRateBar",
        rateLimited,
        total
    );


    setAnalyticsValue(
        "analyticsRAG",
        "analyticsRAGBar",
        rag,
        total
    );

}


/* ============================================================
   SET ANALYTICS VALUE
============================================================ */

function setAnalyticsValue(
    valueId,
    barId,
    value,
    total
) {

    const valueElement =
        document.getElementById(
            valueId
        );

    const barElement =
        document.getElementById(
            barId
        );


    if (!valueElement || !barElement) {
        return;
    }


    valueElement.textContent =
        value;


    if (total <= 0) {

        barElement.style.width =
            "0%";

        return;

    }


    let percentage =
        (value / total) * 100;


    percentage =
        Math.min(
            Math.max(
                percentage,
                0
            ),
            100
        );


    barElement.style.width =
        percentage + "%";

}


/* ============================================================
   LOAD ATTACK TEST REPORT
============================================================ */
"""

if "function updateSecurityAnalytics(" not in html:

    if function_marker not in html:
        raise SystemExit(
            "Attack report function marker not found."
        )

    html = html.replace(
        function_marker,
        analytics_function,
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
print("SECURITY ANALYTICS UPDATE COMPLETE")
print("=" * 60)
print()
print("Added:")
print("- Security event distribution")
print("- Event percentage bars")
print("- Total event count")
print("- Allowed requests")
print("- Prompt injection")
print("- PII detection")
print("- Input blocking")
print("- Rate limiting")
print("- RAG injection")
print()
print("Updated:")
print(FILE)
print()
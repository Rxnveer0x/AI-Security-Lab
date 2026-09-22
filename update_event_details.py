from pathlib import Path
import re

HTML_FILE = Path("app/templates/index.html")

if not HTML_FILE.exists():
    raise FileNotFoundError(
        "app/templates/index.html was not found."
    )

html = HTML_FILE.read_text(
    encoding="utf-8"
)

MARKER = "SECURITY EVENT DETAILS UPGRADE"

if MARKER in html:
    print("Security Event Details upgrade is already installed.")
    raise SystemExit


# ============================================================
# BACKUP
# ============================================================

backup_file = Path(
    "app/templates/index_before_event_details.html"
)

if not backup_file.exists():
    backup_file.write_text(
        html,
        encoding="utf-8"
    )

print("Backup ready:")
print(backup_file)


# ============================================================
# 1. ADD CSS
# ============================================================

event_css = r"""
/* ============================================================
   SECURITY EVENT DETAILS UPGRADE
============================================================ */

.event-item {
    cursor: pointer;
    transition:
        border-color 0.18s ease,
        background 0.18s ease,
        transform 0.18s ease;
}

.event-item:hover {
    border-color: var(--blue);
    background: var(--bg-secondary);
    transform: translateY(-1px);
}

.event-item:focus {
    outline: 2px solid var(--blue);
    outline-offset: 2px;
}

.event-details-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.58);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 20px;
}

.event-details-overlay.visible {
    display: flex;
}

.event-details-modal {
    width: min(560px, 100%);
    max-height: 85vh;
    overflow-y: auto;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
}

.event-details-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 15px 16px;
    border-bottom: 1px solid var(--border-light);
}

.event-details-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 700;
}

.event-details-close {
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-size: 22px;
    cursor: pointer;
    line-height: 1;
    padding: 2px 5px;
}

.event-details-close:hover {
    color: var(--text);
}

.event-details-body {
    padding: 16px;
}

.event-detail-row {
    display: grid;
    grid-template-columns: 115px 1fr;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-light);
}

.event-detail-label {
    color: var(--text-secondary);
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.event-detail-value {
    color: var(--text);
    font-size: 11px;
    line-height: 1.5;
    word-break: break-word;
}

.event-detail-message {
    background: var(--bg-input);
    border: 1px solid var(--border-light);
    border-radius: 7px;
    padding: 10px;
    white-space: pre-wrap;
}

.event-detail-json {
    margin-top: 14px;
}

.event-detail-json-title {
    color: var(--text-secondary);
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 7px;
}

.event-detail-json-content {
    background: var(--bg-input);
    border: 1px solid var(--border-light);
    border-radius: 7px;
    padding: 10px;
    color: var(--text-secondary);
    font-family: monospace;
    font-size: 10px;
    line-height: 1.5;
    white-space: pre-wrap;
    overflow-x: auto;
}

.event-detail-risk-high {
    color: var(--red);
    font-weight: 700;
}

.event-detail-risk-medium {
    color: var(--yellow);
    font-weight: 700;
}

.event-detail-risk-low {
    color: var(--green);
    font-weight: 700;
}

@media (max-width: 600px) {

    .event-details-overlay {
        padding: 10px;
    }

    .event-details-modal {
        max-height: 90vh;
    }

    .event-detail-row {
        grid-template-columns: 90px 1fr;
    }

}

/* END SECURITY EVENT DETAILS UPGRADE */
"""


# Find the EVENT LIST CSS section.
event_list_pattern = re.compile(
    r"(\s*/\*\s*=+\s*\n"
    r"\s*EVENT LIST\s*\n"
    r"\s*=+\s*\*/)",
    re.IGNORECASE
)

match = event_list_pattern.search(html)

if not match:

    # Fallback: search for the plain text EVENT LIST.
    fallback = re.search(
        r"/\*[\s\S]{0,150}EVENT LIST[\s\S]{0,150}\*/",
        html,
        re.IGNORECASE
    )

    if not fallback:
        raise RuntimeError(
            "Could not find the EVENT LIST CSS section."
        )

    insert_position = fallback.start()

else:
    insert_position = match.start()


html = (
    html[:insert_position]
    + event_css
    + "\n"
    + html[insert_position:]
)


# ============================================================
# 2. ADD EVENT DETAILS MODAL
# ============================================================

modal_html = r"""
<!-- ============================================================
     SECURITY EVENT DETAILS MODAL
============================================================ -->

<div
    class="event-details-overlay"
    id="eventDetailsOverlay"
    onclick="handleEventDetailsOverlayClick(event)"
>

    <div
        class="event-details-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="eventDetailsTitle"
        onclick="event.stopPropagation()"
    >

        <div class="event-details-header">

            <div
                class="event-details-title"
                id="eventDetailsTitle"
            >
                Security Event Details
            </div>

            <button
                class="event-details-close"
                type="button"
                onclick="closeSecurityEventDetails()"
                aria-label="Close"
            >
                ×
            </button>

        </div>


        <div class="event-details-body">

            <div class="event-detail-row">

                <div class="event-detail-label">
                    Event
                </div>

                <div
                    class="event-detail-value"
                    id="detailEventType"
                >
                    -
                </div>

            </div>


            <div class="event-detail-row">

                <div class="event-detail-label">
                    Timestamp
                </div>

                <div
                    class="event-detail-value"
                    id="detailTimestamp"
                >
                    -
                </div>

            </div>


            <div class="event-detail-row">

                <div class="event-detail-label">
                    Risk
                </div>

                <div
                    class="event-detail-value"
                    id="detailRisk"
                >
                    Not available
                </div>

            </div>


            <div class="event-detail-row">

                <div class="event-detail-label">
                    Message
                </div>

                <div
                    class="event-detail-value event-detail-message"
                    id="detailMessage"
                >
                    -
                </div>

            </div>


            <div
                class="event-detail-json"
                id="detailMetadataSection"
            >

                <div class="event-detail-json-title">
                    Event Metadata
                </div>

                <div
                    class="event-detail-json-content"
                    id="detailMetadata"
                >
                    No additional metadata available.
                </div>

            </div>

        </div>

    </div>

</div>

<!-- END SECURITY EVENT DETAILS MODAL -->
"""


# Insert modal before the dashboard closes.
aside_position = html.find("</aside>")

if aside_position == -1:
    raise RuntimeError(
        "Could not find dashboard closing </aside>."
    )

html = (
    html[:aside_position]
    + modal_html
    + "\n\n"
    + html[aside_position:]
)


# ============================================================
# 3. MAKE SECURITY EVENTS CLICKABLE
# ============================================================

event_class_pattern = re.compile(
    r'(eventItem\.className\s*=\s*"event-item";)'
)

event_class_match = event_class_pattern.search(html)

if not event_class_match:
    raise RuntimeError(
        "Could not find eventItem class assignment."
    )


click_code = r'''

    eventItem.setAttribute(
        "tabindex",
        "0"
    );

    eventItem.setAttribute(
        "role",
        "button"
    );

    eventItem.setAttribute(
        "aria-label",
        "View security event details"
    );

    eventItem.addEventListener(
        "click",
        function () {
            showSecurityEventDetails(event);
        }
    );

    eventItem.addEventListener(
        "keydown",
        function (keyboardEvent) {

            if (
                keyboardEvent.key === "Enter" ||
                keyboardEvent.key === " "
            ) {

                keyboardEvent.preventDefault();

                showSecurityEventDetails(event);

            }

        }
    );'''

html = (
    html[:event_class_match.end()]
    + click_code
    + html[event_class_match.end():]
)


# ============================================================
# 4. ADD JAVASCRIPT
# ============================================================

event_js = r"""
/* ============================================================
   SECURITY EVENT DETAILS
============================================================ */

function showSecurityEventDetails(event) {

    const overlay =
        document.getElementById(
            "eventDetailsOverlay"
        );

    const typeElement =
        document.getElementById(
            "detailEventType"
        );

    const timestampElement =
        document.getElementById(
            "detailTimestamp"
        );

    const riskElement =
        document.getElementById(
            "detailRisk"
        );

    const messageElement =
        document.getElementById(
            "detailMessage"
        );

    const metadataElement =
        document.getElementById(
            "detailMetadata"
        );


    if (
        !overlay ||
        !typeElement ||
        !timestampElement ||
        !riskElement ||
        !messageElement ||
        !metadataElement
    ) {
        return;
    }


    const eventName =
        String(
            event?.event ||
            "UNKNOWN"
        );


    const timestamp =
        String(
            event?.timestamp ||
            "Not available"
        );


    const message =
        String(
            event?.message ||
            "No message available."
        );


    typeElement.textContent =
        eventName;

    timestampElement.textContent =
        timestamp;

    messageElement.textContent =
        message;


    let riskValue =
        event?.risk_level ??
        event?.risk ??
        event?.riskLevel ??
        null;


    let riskScore =
        event?.risk_score ??
        event?.riskScore ??
        null;


    riskElement.className =
        "event-detail-value";


    if (
        riskValue === null &&
        riskScore === null
    ) {

        riskElement.textContent =
            "Not available";

    }

    else {

        let riskText = "";

        if (riskValue !== null) {

            riskText =
                String(riskValue);

        }


        if (riskScore !== null) {

            if (riskText) {
                riskText += " | ";
            }

            riskText +=
                "Score: " +
                String(riskScore);

        }


        riskElement.textContent =
            riskText;


        const normalizedRisk =
            String(
                riskValue || ""
            ).toUpperCase();


        if (
            normalizedRisk === "HIGH"
        ) {

            riskElement.classList.add(
                "event-detail-risk-high"
            );

        }

        else if (
            normalizedRisk === "MEDIUM"
        ) {

            riskElement.classList.add(
                "event-detail-risk-medium"
            );

        }

        else if (
            normalizedRisk === "LOW"
        ) {

            riskElement.classList.add(
                "event-detail-risk-low"
            );

        }

    }


    const metadata = {};


    Object.keys(
        event || {}
    ).forEach(
        function (key) {

            if (
                key !== "event" &&
                key !== "timestamp" &&
                key !== "message" &&
                key !== "risk_level" &&
                key !== "risk" &&
                key !== "riskLevel" &&
                key !== "risk_score" &&
                key !== "riskScore"
            ) {

                metadata[key] =
                    event[key];

            }

        }
    );


    if (
        Object.keys(metadata).length === 0
    ) {

        metadataElement.textContent =
            "No additional metadata available.";

    }

    else {

        try {

            metadataElement.textContent =
                JSON.stringify(
                    metadata,
                    null,
                    2
                );

        }

        catch (error) {

            metadataElement.textContent =
                "Metadata could not be displayed.";

        }

    }


    overlay.classList.add(
        "visible"
    );


    document.body.style.overflow =
        "hidden";

}


function closeSecurityEventDetails() {

    const overlay =
        document.getElementById(
            "eventDetailsOverlay"
        );


    if (!overlay) {
        return;
    }


    overlay.classList.remove(
        "visible"
    );


    document.body.style.overflow =
        "";

}


function handleEventDetailsOverlayClick(
    event
) {

    if (
        event.target &&
        event.target.id ===
        "eventDetailsOverlay"
    ) {

        closeSecurityEventDetails();

    }

}


document.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Escape"
        ) {

            closeSecurityEventDetails();

        }

    }
);

/* END SECURITY EVENT DETAILS */
"""


# Put JavaScript before the existing automatic refresh.
automatic_refresh_marker = (
    "/* AUTOMATIC SECURITY DASHBOARD REFRESH */"
)

if automatic_refresh_marker in html:

    html = html.replace(
        automatic_refresh_marker,
        event_js
        + "\n\n"
        + automatic_refresh_marker,
        1
    )

else:

    # Fallback: insert before </script>
    script_position = html.rfind(
        "</script>"
    )

    if script_position == -1:
        raise RuntimeError(
            "Could not find JavaScript closing tag."
        )

    html = (
        html[:script_position]
        + event_js
        + "\n\n"
        + html[script_position:]
    )


# ============================================================
# 5. SAVE
# ============================================================

HTML_FILE.write_text(
    html,
    encoding="utf-8"
)


print()
print("==============================================")
print("SECURITY EVENT DETAILS UPGRADE COMPLETE")
print("==============================================")
print()
print("Updated:")
print("app/templates/index.html")
print()
print("Backup:")
print("app/templates/index_before_event_details.html")
print()
print("Security events are now clickable.")
print("Press Enter or Space on a selected event.")
print("Press Escape to close the details window.")
print()
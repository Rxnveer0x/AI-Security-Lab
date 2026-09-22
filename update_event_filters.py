from pathlib import Path
import re

HTML_FILE = Path("app/templates/index.html")

if not HTML_FILE.exists():
    raise FileNotFoundError(
        "app/templates/index.html was not found."
    )

html = HTML_FILE.read_text(encoding="utf-8")

if "SECURITY EVENT FILTERING" in html:
    print("Security Event Filtering is already installed.")
    raise SystemExit


# ============================================================
# 1. BACKUP
# ============================================================

backup_file = Path(
    "app/templates/index_before_event_filters.html"
)

if not backup_file.exists():
    backup_file.write_text(
        html,
        encoding="utf-8"
    )

print("Backup ready:")
print(backup_file)


# ============================================================
# 2. ADD FILTER CSS
# ============================================================

filter_css = r"""
/* ============================================================
   SECURITY EVENT FILTERING
============================================================ */

.event-filter-container {
    display: flex;
    gap: 7px;
    margin-bottom: 9px;
}

.event-filter-select,
.event-filter-search {
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-size: 10px;
    padding: 7px 8px;
    outline: none;
}

.event-filter-select {
    width: 125px;
    flex-shrink: 0;
}

.event-filter-search {
    flex: 1;
    min-width: 0;
}

.event-filter-select:focus,
.event-filter-search:focus {
    border-color: var(--blue);
}

.event-filter-search::placeholder {
    color: var(--text-muted);
}

.event-filter-status {
    color: var(--text-muted);
    font-size: 9px;
    margin-bottom: 8px;
}

.event-filter-empty {
    text-align: center;
    color: var(--text-muted);
    font-size: 10px;
    padding: 18px 5px;
}

/* END SECURITY EVENT FILTERING */
"""


# Insert CSS before the existing EVENT LIST CSS.
event_list_css_pattern = re.compile(
    r"/\*\s*=+\s*\n"
    r"\s*EVENT LIST\s*\n"
    r"\s*=+\s*\*/",
    re.IGNORECASE
)

css_match = event_list_css_pattern.search(html)

if not css_match:

    css_match = re.search(
        r"/\*[\s\S]{0,150}EVENT LIST[\s\S]{0,150}\*/",
        html,
        re.IGNORECASE
    )

if not css_match:
    raise RuntimeError(
        "Could not find the existing EVENT LIST CSS section."
    )

html = (
    html[:css_match.start()]
    + filter_css
    + "\n"
    + html[css_match.start():]
)


# ============================================================
# 3. ADD FILTER CONTROLS TO EXISTING EVENT SECTION
# ============================================================

filter_html = r"""
<div
    class="event-filter-container"
    id="eventFilterContainer"
>

    <select
        class="event-filter-select"
        id="eventTypeFilter"
        onchange="applySecurityEventFilters()"
        aria-label="Filter security events"
    >

        <option value="ALL">
            All Events
        </option>

        <option value="ALLOWED">
            Allowed
        </option>

        <option value="PROMPT_INJECTION">
            Prompt Injection
        </option>

        <option value="JAILBREAK_DETECTED">
            Jailbreak
        </option>

        <option value="PII_DETECTED">
            PII Detected
        </option>

        <option value="INPUT_BLOCKED">
            Input Blocked
        </option>

        <option value="RATE_LIMITED">
            Rate Limited
        </option>

        <option value="RAG_INJECTION_BLOCKED">
            RAG Injection
        </option>

        <option value="OUTPUT_PII_DETECTED">
            Output PII
        </option>

        <option value="OUTPUT_BLOCKED">
            Output Blocked
        </option>

        <option value="AI_ERROR">
            AI Error
        </option>

    </select>


    <input
        type="text"
        class="event-filter-search"
        id="eventSearchInput"
        placeholder="Search events..."
        oninput="applySecurityEventFilters()"
        autocomplete="off"
    >

</div>


<div
    class="event-filter-status"
    id="eventFilterStatus"
>
    Showing all events
</div>
"""


recent_events_pattern = re.compile(
    r'(<div\s+class="section-heading">\s*'
    r'Recent Security Events\s*'
    r'</div>)',
    re.IGNORECASE
)

recent_match = recent_events_pattern.search(html)

if not recent_match:
    raise RuntimeError(
        "Could not find the existing Recent Security Events heading."
    )

insert_position = recent_match.end()

html = (
    html[:insert_position]
    + "\n\n"
    + filter_html
    + html[insert_position:]
)


# ============================================================
# 4. MODIFY LOAD SECURITY EVENTS
# ============================================================

old_events_section = r"""
    const reversedEvents =
        [...events].reverse();


    reversedEvents.forEach(
        function (event) {

            createSecurityEventElement(
                event,
                eventList
            );

        }
    );
"""

new_events_section = r"""
    /*
       Store the backend events locally so the
       existing event list can be filtered
       without another server request.
    */

    securityEventsData =
        [...events].reverse();

    renderFilteredSecurityEvents();
"""

if old_events_section not in html:

    # More tolerant fallback.
    old_events_pattern = re.compile(
        r'\s*const reversedEvents\s*=\s*'
        r'\[\.\.\.events\]\.reverse\(\);\s*'
        r'reversedEvents\.forEach\(\s*'
        r'function\s*\(event\)\s*\{\s*'
        r'createSecurityEventElement\(\s*'
        r'event,\s*'
        r'eventList\s*'
        r'\);\s*'
        r'\}\s*'
        r'\);',
        re.DOTALL
    )

    old_match = old_events_pattern.search(html)

    if not old_match:
        raise RuntimeError(
            "Could not find the existing security event rendering code."
        )

    html = (
        html[:old_match.start()]
        + new_events_section
        + html[old_match.end():]
    )

else:

    html = html.replace(
        old_events_section,
        new_events_section,
        1
    )


# ============================================================
# 5. ADD FILTER STATE + FUNCTIONS
# ============================================================

filter_js = r"""
/* ============================================================
   SECURITY EVENT FILTERING
============================================================ */

let securityEventsData = [];


function applySecurityEventFilters() {

    renderFilteredSecurityEvents();

}


function renderFilteredSecurityEvents() {

    const eventList =
        document.getElementById(
            "eventList"
        );

    const filter =
        document.getElementById(
            "eventTypeFilter"
        );

    const search =
        document.getElementById(
            "eventSearchInput"
        );

    const status =
        document.getElementById(
            "eventFilterStatus"
        );


    if (
        !eventList ||
        !filter ||
        !search ||
        !status
    ) {
        return;
    }


    const selectedType =
        filter.value || "ALL";


    const searchText =
        search.value
            .trim()
            .toLowerCase();


    const filteredEvents =
        securityEventsData.filter(
            function (event) {

                const eventType =
                    String(
                        event?.event ||
                        "UNKNOWN"
                    );


                const eventMessage =
                    String(
                        event?.message ||
                        ""
                    );


                const typeMatches =
                    selectedType === "ALL" ||
                    eventType === selectedType;


                const searchMatches =
                    !searchText ||
                    eventType
                        .toLowerCase()
                        .includes(searchText) ||
                    eventMessage
                        .toLowerCase()
                        .includes(searchText);


                return (
                    typeMatches &&
                    searchMatches
                );

            }
        );


    eventList.innerHTML = "";


    if (
        filteredEvents.length === 0
    ) {

        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "event-filter-empty";

        empty.textContent =
            "No matching security events.";

        eventList.appendChild(
            empty
        );


        status.textContent =
            "No matching events";

        return;

    }


    filteredEvents.forEach(
        function (event) {

            createSecurityEventElement(
                event,
                eventList
            );

        }
    );


    const total =
        securityEventsData.length;


    const shown =
        filteredEvents.length;


    if (
        selectedType === "ALL" &&
        searchText === ""
    ) {

        status.textContent =
            "Showing all " +
            total +
            " events";

    }

    else {

        status.textContent =
            "Showing " +
            shown +
            " of " +
            total +
            " events";

    }

}

/* END SECURITY EVENT FILTERING */
"""


# Insert before the existing loadSecurityEvents function.
load_events_marker = (
    "/* ============================================================\n"
    "   LOAD SECURITY EVENTS"
)

position = html.find(
    load_events_marker
)

if position == -1:
    raise RuntimeError(
        "Could not find LOAD SECURITY EVENTS JavaScript section."
    )

html = (
    html[:position]
    + filter_js
    + "\n\n"
    + html[position:]
)


# ============================================================
# 6. SAVE
# ============================================================

HTML_FILE.write_text(
    html,
    encoding="utf-8"
)


print()
print("==============================================")
print("SECURITY EVENT FILTERING INSTALLED")
print("==============================================")
print()
print("Modified existing:")
print("Recent Security Events")
print()
print("Added:")
print("- Event type filter")
print("- Event search")
print("- Matching event count")
print()
print("No existing security section was recreated.")
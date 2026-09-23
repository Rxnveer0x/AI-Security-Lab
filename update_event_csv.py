from pathlib import Path
import shutil

HTML_FILE = Path("app/templates/index.html")
BACKUP_FILE = Path("app/templates/index_before_event_csv.html")

if not HTML_FILE.exists():
    print("ERROR: index.html not found.")
    raise SystemExit(1)

# Create backup
shutil.copy2(HTML_FILE, BACKUP_FILE)
print(f"Backup created: {BACKUP_FILE}")

html = HTML_FILE.read_text(encoding="utf-8")

# ---------------------------------------------------------
# 1. Add CSV button CSS
# ---------------------------------------------------------

css_marker = ".event-export-button"

if ".event-export-csv-button" not in html:
    css_block = """
.event-export-csv-button {
    margin-left: 8px;
}
"""

    style_end = html.find("</style>")

    if style_end == -1:
        print("ERROR: Could not find </style>.")
        raise SystemExit(1)

    html = html[:style_end] + css_block + html[style_end:]

# ---------------------------------------------------------
# 2. Add CSV export button
# ---------------------------------------------------------

if "id=\"exportCsvButton\"" not in html:

    json_button_marker = '<button class="event-export-button" id="exportEventsButton"'

    marker_position = html.find(json_button_marker)

    if marker_position != -1:

        button_end = html.find("</button>", marker_position)

        if button_end != -1:
            button_end += len("</button>")

            csv_button = """
<button class="event-export-button event-export-csv-button" id="exportCsvButton">
    Export CSV
</button>
"""

            html = (
                html[:button_end]
                + csv_button
                + html[button_end:]
            )

        else:
            print("ERROR: Could not find JSON export button ending.")
            raise SystemExit(1)

    else:
        # Fallback: insert before event list
        event_list_position = html.find('id="eventList"')

        if event_list_position == -1:
            print("ERROR: Could not find eventList.")
            raise SystemExit(1)

        container_start = html.rfind("<", 0, event_list_position)

        csv_button = """
<div class="event-export-container">
    <button class="event-export-button" id="exportCsvButton">
        Export CSV
    </button>
</div>
"""

        html = (
            html[:container_start]
            + csv_button
            + html[container_start:]
        )

# ---------------------------------------------------------
# 3. Add CSV export JavaScript
# ---------------------------------------------------------

if "function exportSecurityEventsCSV()" not in html:

    csv_function = r"""
<script>
function exportSecurityEventsCSV() {
    if (!Array.isArray(securityEventsData) || securityEventsData.length === 0) {
        alert("No security events available to export.");
        return;
    }

    const headers = [
        "Event",
        "Timestamp",
        "Risk Level",
        "Message"
    ];

    function escapeCSV(value) {
        const text = value === null || value === undefined
            ? ""
            : String(value);

        return '"' + text.replace(/"/g, '""') + '"';
    }

    const rows = securityEventsData.map(function(event) {
        return [
            escapeCSV(event.event),
            escapeCSV(event.timestamp),
            escapeCSV(event.risk_level || event.risk || ""),
            escapeCSV(event.message)
        ].join(",");
    });

    const csvContent = [
        headers.map(escapeCSV).join(","),
        ...rows
    ].join("\\r\\n");

    const blob = new Blob(
        [csvContent],
        { type: "text/csv;charset=utf-8;" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "security_events.csv";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}
</script>
"""

    script_end = html.rfind("</body>")

    if script_end == -1:
        print("ERROR: Could not find </body>.")
        raise SystemExit(1)

    html = html[:script_end] + csv_function + html[script_end:]

# ---------------------------------------------------------
# 4. Attach button event
# ---------------------------------------------------------

if "exportCsvButton" in html and "addEventListener(\"click\", exportSecurityEventsCSV)" not in html:

    listener_script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    const csvButton = document.getElementById("exportCsvButton");

    if (csvButton) {
        csvButton.addEventListener("click", exportSecurityEventsCSV);
    }
});
</script>
"""

    script_end = html.rfind("</body>")

    if script_end == -1:
        print("ERROR: Could not find </body>.")
        raise SystemExit(1)

    html = html[:script_end] + listener_script + html[script_end:]

# ---------------------------------------------------------
# 5. Save
# ---------------------------------------------------------

HTML_FILE.write_text(html, encoding="utf-8")

print("SUCCESS: CSV export added.")
print("File updated:", HTML_FILE)
print("Backup:", BACKUP_FILE)
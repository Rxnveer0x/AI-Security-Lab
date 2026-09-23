from pathlib import Path
import shutil

HTML_FILE = Path("app/templates/index.html")
BACKUP_FILE = Path("app/templates/index_before_security_report_button.html")

if not HTML_FILE.exists():
    print("ERROR: index.html not found.")
    raise SystemExit(1)

# Create backup
shutil.copy2(HTML_FILE, BACKUP_FILE)
print(f"Backup created: {BACKUP_FILE}")

html = HTML_FILE.read_text(encoding="utf-8")

# ---------------------------------------------------------
# 1. Add button CSS
# ---------------------------------------------------------

if ".security-report-button" not in html:

    css_block = """
.security-report-button {
    margin-left: 8px;
}
"""

    style_end = html.find("</style>")

    if style_end == -1:
        print("ERROR: Could not find </style>.")
        raise SystemExit(1)

    html = (
        html[:style_end]
        + css_block
        + html[style_end:]
    )

# ---------------------------------------------------------
# 2. Add Download Security Report button
# ---------------------------------------------------------

if 'id="downloadSecurityReportButton"' not in html:

    csv_marker = 'id="exportCsvButton"'

    csv_position = html.find(csv_marker)

    if csv_position != -1:

        button_start = html.rfind("<button", 0, csv_position)
        button_end = html.find("</button>", csv_position)

        if button_start == -1 or button_end == -1:
            print("ERROR: Could not locate CSV button.")
            raise SystemExit(1)

        button_end += len("</button>")

        report_button = """
<button
    class="event-export-button security-report-button"
    id="downloadSecurityReportButton">
    Download Security Report
</button>
"""

        html = (
            html[:button_end]
            + report_button
            + html[button_end:]
        )

    else:
        print("ERROR: Could not find Export CSV button.")
        raise SystemExit(1)

# ---------------------------------------------------------
# 3. Add JavaScript function
# ---------------------------------------------------------

if "function downloadSecurityReport()" not in html:

    report_function = r"""
<script>
function downloadSecurityReport() {
    window.location.href = "/security-report";
}
</script>
"""

    body_end = html.rfind("</body>")

    if body_end == -1:
        print("ERROR: Could not find </body>.")
        raise SystemExit(1)

    html = (
        html[:body_end]
        + report_function
        + html[body_end:]
    )

# ---------------------------------------------------------
# 4. Attach button event
# ---------------------------------------------------------

if (
    'id="downloadSecurityReportButton"' in html
    and "downloadSecurityReportButton" in html
    and "addEventListener(\"click\", downloadSecurityReport)" not in html
):

    listener_script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    const reportButton = document.getElementById(
        "downloadSecurityReportButton"
    );

    if (reportButton) {
        reportButton.addEventListener(
            "click",
            downloadSecurityReport
        );
    }
});
</script>
"""

    body_end = html.rfind("</body>")

    if body_end == -1:
        print("ERROR: Could not find </body>.")
        raise SystemExit(1)

    html = (
        html[:body_end]
        + listener_script
        + html[body_end:]
    )

# ---------------------------------------------------------
# 5. Save
# ---------------------------------------------------------

HTML_FILE.write_text(html, encoding="utf-8")

print("SUCCESS: Security Report button added.")
print("Updated:", HTML_FILE)
print("Backup:", BACKUP_FILE)

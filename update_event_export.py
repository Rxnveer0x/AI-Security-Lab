from pathlib import Path
import shutil


HTML_FILE = Path("app/templates/index.html")
BACKUP_FILE = Path(
    "app/templates/index_before_event_export.html"
)


def main():

    if not HTML_FILE.exists():
        print("ERROR: app/templates/index.html not found.")
        return

    html = HTML_FILE.read_text(
        encoding="utf-8"
    )

    # ---------------------------------------------------------
    # Create backup
    # ---------------------------------------------------------

    shutil.copy2(
        HTML_FILE,
        BACKUP_FILE
    )

    print(
        f"Backup created: {BACKUP_FILE}"
    )

    # ---------------------------------------------------------
    # 1. Add export button CSS
    # ---------------------------------------------------------

    export_css = """

        /* =====================================================
           EVENT EXPORT
        ===================================================== */

        .event-export-container {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 8px;
        }

        .event-export-button {
            background: var(--bg-card);
            color: var(--text-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 9px;
            cursor: pointer;
            transition: 0.2s ease;
        }

        .event-export-button:hover {
            color: var(--text);
            border-color: var(--text-muted);
        }

"""

    if "EVENT EXPORT" not in html:

        if "</style>" not in html:
            print("ERROR: Could not find </style>.")
            return

        html = html.replace(
            "</style>",
            export_css + "\n</style>",
            1
        )

    # ---------------------------------------------------------
    # 2. Add export button to existing event section
    # ---------------------------------------------------------

    export_html = """
<div class="event-export-container">

    <button
        type="button"
        class="event-export-button"
        id="exportSecurityEventsButton"
    >
        Export Events
    </button>

</div>
"""

    if 'id="exportSecurityEventsButton"' not in html:

        event_list_marker = 'id="eventList"'

        position = html.find(
            event_list_marker
        )

        if position == -1:
            print(
                'ERROR: Could not find existing eventList.'
            )
            return

        # Find the beginning of the containing
        # div for eventList.
        container_start = html.rfind(
            "<div",
            0,
            position
        )

        if container_start == -1:
            print(
                "ERROR: Could not locate eventList container."
            )
            return

        html = (
            html[:container_start]
            + export_html
            + html[container_start:]
        )

    # ---------------------------------------------------------
    # 3. Add JavaScript export function
    # ---------------------------------------------------------

    export_js = r"""

/* ============================================================
   SECURITY EVENT EXPORT
============================================================ */

function exportSecurityEvents() {

    if (
        typeof securityEventsData ===
        "undefined"
    ) {

        alert(
            "No security events available."
        );

        return;

    }


    if (
        !Array.isArray(
            securityEventsData
        ) ||
        securityEventsData.length === 0
    ) {

        alert(
            "No security events available."
        );

        return;

    }


    const exportData = {

        exported_at:
            new Date().toISOString(),

        total_events:
            securityEventsData.length,

        events:
            securityEventsData

    };


    const jsonData =
        JSON.stringify(
            exportData,
            null,
            2
        );


    const blob =
        new Blob(
            [jsonData],
            {
                type:
                    "application/json"
            }
        );


    const url =
        URL.createObjectURL(
            blob
        );


    const link =
        document.createElement(
            "a"
        );


    link.href = url;

    link.download =
        "security_events_" +
        new Date()
            .toISOString()
            .replace(
                /[:.]/g,
                "-"
            ) +
        ".json";


    document.body.appendChild(
        link
    );


    link.click();


    document.body.removeChild(
        link
    );


    URL.revokeObjectURL(
        url
    );

}


/*
   Connect export button.
*/

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const button =
            document.getElementById(
                "exportSecurityEventsButton"
            );


        if (button) {

            button.addEventListener(
                "click",
                exportSecurityEvents
            );

        }

    }
);

"""

    if "SECURITY EVENT EXPORT" not in html:

        script_end = html.rfind(
            "</script>"
        )

        if script_end == -1:
            print(
                "ERROR: Could not find </script>."
            )
            return

        html = (
            html[:script_end]
            + export_js
            + "\n"
            + html[script_end:]
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    HTML_FILE.write_text(
        html,
        encoding="utf-8"
    )

    print()
    print(
        "SUCCESS: Event export added."
    )
    print()
    print(
        "Updated:"
    )
    print(
        "app/templates/index.html"
    )
    print()
    print(
        "Backup:"
    )
    print(
        "app/templates/index_before_event_export.html"
    )


if __name__ == "__main__":
    main()
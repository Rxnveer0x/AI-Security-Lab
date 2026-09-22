from pathlib import Path
import shutil


HTML_FILE = Path("app/templates/index.html")
BACKUP_FILE = Path(
    "app/templates/index_before_event_pagination.html"
)


def replace_once(text, old, new, description):
    if old not in text:
        print(f"ERROR: Could not find {description}.")
        return None

    return text.replace(old, new, 1)


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
    # 1. Add pagination CSS
    # ---------------------------------------------------------

    pagination_css = r"""

        /* =====================================================
           EVENT PAGINATION
        ===================================================== */

        .event-pagination {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid var(--border);
        }

        .event-pagination button {
            background: var(--bg-card);
            color: var(--text-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 9px;
            cursor: pointer;
        }

        .event-pagination button:hover:not(:disabled) {
            color: var(--text);
            border-color: var(--text-muted);
        }

        .event-pagination button:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .event-pagination-info {
            color: var(--text-muted);
            font-size: 9px;
            min-width: 65px;
            text-align: center;
        }

"""

    if "EVENT PAGINATION" not in html:

        if "</style>" not in html:
            print("ERROR: Could not find </style>.")
            return

        html = html.replace(
            "</style>",
            pagination_css + "\n</style>",
            1
        )

    # ---------------------------------------------------------
    # 2. Add pagination controls to existing event section
    # ---------------------------------------------------------

    pagination_html = r"""
<div class="event-pagination" id="eventPagination">

    <button
        type="button"
        id="eventPreviousButton"
    >
        Previous
    </button>

    <div
        class="event-pagination-info"
        id="eventPaginationInfo"
    >
        Page 1 of 1
    </div>

    <button
        type="button"
        id="eventNextButton"
    >
        Next
    </button>

</div>
"""

    if 'id="eventPagination"' not in html:

        # Find the existing event list element.
        event_list_start = html.find(
            'id="eventList"'
        )

        if event_list_start == -1:
            print(
                'ERROR: Could not find existing id="eventList".'
            )
            print(
                "No changes were saved."
            )
            return

        # Find the nearest closing div after eventList.
        closing_div = html.find(
            "</div>",
            event_list_start
        )

        if closing_div == -1:
            print(
                "ERROR: Could not find eventList closing tag."
            )
            print(
                "No changes were saved."
            )
            return

        closing_div += len("</div>")

        html = (
            html[:closing_div]
            + pagination_html
            + html[closing_div:]
        )

    # ---------------------------------------------------------
    # 3. Add pagination JavaScript
    # ---------------------------------------------------------

    pagination_js = r"""

/* ============================================================
   EVENT PAGINATION
============================================================ */

let currentEventPage = 1;

const EVENTS_PER_PAGE = 10;


/*
   Get events currently available
   to the dashboard.
*/

function getCurrentEventData() {

    if (
        typeof securityEventsData !==
        "undefined"
    ) {
        return securityEventsData;
    }

    return [];

}


/*
   Render current event page.
*/

function renderEventPagination() {

    const eventList =
        document.getElementById(
            "eventList"
        );

    const pagination =
        document.getElementById(
            "eventPagination"
        );

    const previousButton =
        document.getElementById(
            "eventPreviousButton"
        );

    const nextButton =
        document.getElementById(
            "eventNextButton"
        );

    const paginationInfo =
        document.getElementById(
            "eventPaginationInfo"
        );


    if (
        !eventList ||
        !pagination ||
        !previousButton ||
        !nextButton ||
        !paginationInfo
    ) {
        return;
    }


    const events =
        getCurrentEventData();


    const totalEvents =
        events.length;


    const totalPages =
        Math.max(
            1,
            Math.ceil(
                totalEvents /
                EVENTS_PER_PAGE
            )
        );


    if (
        currentEventPage >
        totalPages
    ) {
        currentEventPage =
            totalPages;
    }


    if (
        currentEventPage < 1
    ) {
        currentEventPage = 1;
    }


    const startIndex =
        (
            currentEventPage - 1
        ) *
        EVENTS_PER_PAGE;


    const endIndex =
        startIndex +
        EVENTS_PER_PAGE;


    const visibleEvents =
        events.slice(
            startIndex,
            endIndex
        );


    eventList.innerHTML = "";


    if (
        visibleEvents.length === 0
    ) {

        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "no-events";

        empty.textContent =
            "No security events found.";

        eventList.appendChild(
            empty
        );

    }

    else {

        visibleEvents.forEach(
            function(event) {

                createSecurityEventElement(
                    event,
                    eventList
                );

            }
        );

    }


    paginationInfo.textContent =
        "Page " +
        currentEventPage +
        " of " +
        totalPages;


    previousButton.disabled =
        currentEventPage <= 1;


    nextButton.disabled =
        currentEventPage >= totalPages;


    if (
        totalEvents <=
        EVENTS_PER_PAGE
    ) {

        pagination.style.display =
            "none";

    }

    else {

        pagination.style.display =
            "flex";

    }

}


/*
   Change page.
*/

function changeEventPage(
    direction
) {

    currentEventPage +=
        direction;

    renderEventPagination();

}


/*
   Previous button.
*/

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const previousButton =
            document.getElementById(
                "eventPreviousButton"
            );

        const nextButton =
            document.getElementById(
                "eventNextButton"
            );


        if (previousButton) {

            previousButton.addEventListener(
                "click",
                function() {

                    changeEventPage(-1);

                }
            );

        }


        if (nextButton) {

            nextButton.addEventListener(
                "click",
                function() {

                    changeEventPage(1);

                }
            );

        }

    }
);

"""

    if "EVENT PAGINATION" not in html:

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
            + pagination_js
            + "\n"
            + html[script_end:]
        )

    # ---------------------------------------------------------
    # 4. Modify existing event renderer
    # ---------------------------------------------------------

    marker = """
    const reversedEvents =
        [...events].reverse();
"""

    replacement = """
    const reversedEvents =
        [...events].reverse();

    securityEventsData =
        reversedEvents;

    currentEventPage = 1;

    renderEventPagination();

    return;
"""

    if (
        marker in html and
        "securityEventsData =\n        reversedEvents;" not in html
    ):

        html = html.replace(
            marker,
            marker + replacement,
            1
        )

    # ---------------------------------------------------------
    # Save file
    # ---------------------------------------------------------

    HTML_FILE.write_text(
        html,
        encoding="utf-8"
    )

    print()
    print(
        "SUCCESS: Event pagination added."
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
        "app/templates/index_before_event_pagination.html"
    )
    print()
    print(
        "Events per page: 10"
    )


if __name__ == "__main__":
    main()
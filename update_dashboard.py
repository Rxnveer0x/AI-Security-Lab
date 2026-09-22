from pathlib import Path

FILE = Path("app/templates/index.html")

html = FILE.read_text(encoding="utf-8")

# ---------------------------------------------------------
# 1. Add dashboard status CSS
# ---------------------------------------------------------

css_marker = """
        .dashboard-content {
            padding: 16px;
        }
"""

css_insert = """
        .dashboard-content {
            padding: 16px;
        }

        /* =========================================================
           SECURITY STATUS
        ========================================================= */

        .security-status {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 11px;
            margin-bottom: 18px;
        }

        .security-status-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .security-status-title {
            color: var(--text-secondary);
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            font-weight: 600;
        }

        .security-status-value {
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--green);
            font-size: 11px;
            font-weight: 600;
        }

        .security-status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--green);
        }

        .security-status-value.warning {
            color: var(--yellow);
        }

        .security-status-value.warning
        .security-status-dot {
            background: var(--yellow);
        }

        .security-status-value.error {
            color: var(--red);
        }

        .security-status-value.error
        .security-status-dot {
            background: var(--red);
        }

        .security-status-time {
            margin-top: 7px;
            color: var(--text-muted);
            font-size: 9px;
        }

        .attack-status {
            margin-top: 8px;
            color: var(--text-secondary);
            font-size: 9px;
        }

        .attack-status strong {
            color: var(--text);
        }
"""

if css_marker not in html:
    raise SystemExit("CSS marker not found.")

if ".security-status {" not in html:
    html = html.replace(css_marker, css_insert, 1)


# ---------------------------------------------------------
# 2. Add Security Status panel
# ---------------------------------------------------------

html_marker = """
        <!-- DASHBOARD CONTENT -->

        <div class="dashboard-content">
"""

html_insert = """
        <!-- DASHBOARD CONTENT -->

        <div class="dashboard-content">

            <!-- =================================================
                 SECURITY STATUS
            ================================================== -->

            <section class="security-status">

                <div class="security-status-header">

                    <div class="security-status-title">
                        System Status
                    </div>

                    <div
                        class="security-status-value"
                        id="securityStatus"
                    >
                        <span class="security-status-dot"></span>
                        <span id="securityStatusText">
                            OPERATIONAL
                        </span>
                    </div>

                </div>

                <div
                    class="security-status-time"
                    id="securityLastUpdated"
                >
                    Last updated: Waiting for data...
                </div>

                <div
                    class="attack-status"
                    id="attackStatus"
                >
                    Attack tests: <strong>Checking...</strong>
                </div>

            </section>
"""

if html_marker not in html:
    raise SystemExit("Dashboard content marker not found.")

if 'id="securityStatus"' not in html:
    html = html.replace(html_marker, html_insert, 1)


# ---------------------------------------------------------
# 3. Update dashboard refresh function
# ---------------------------------------------------------

old_refresh = """async function refreshSecurityDashboard() {

    const eventList =
        document.getElementById(
            "eventList"
        );


    eventList.innerHTML = `

        <div class="dashboard-loading">
            Refreshing security data...
        </div>

    `;


    try {

       await Promise.all([
    loadSecuritySummary(),
    loadSecurityEvents(),
    loadAttackTestReport()
]);
    }

    catch (error) {

        console.error(
            "Dashboard refresh error:",
            error
        );


        eventList.innerHTML = `

            <div class="no-events">
                Unable to load security data.
            </div>

        `;

    }

}
"""

new_refresh = """async function refreshSecurityDashboard() {

    const eventList =
        document.getElementById(
            "eventList"
        );

    try {

        await Promise.all([
            loadSecuritySummary(),
            loadSecurityEvents(),
            loadAttackTestReport()
        ]);

        updateSecurityStatus("OPERATIONAL");

        const now =
            new Date();

        document.getElementById(
            "securityLastUpdated"
        ).textContent =
            "Last updated: " +
            now.toLocaleTimeString();

    }

    catch (error) {

        console.error(
            "Dashboard refresh error:",
            error
        );

        updateSecurityStatus("ERROR");

        eventList.innerHTML = `

            <div class="no-events">
                Unable to load security data.
            </div>

        `;

    }

}
"""

if old_refresh not in html:
    raise SystemExit("Refresh function not found.")

html = html.replace(old_refresh, new_refresh, 1)


# ---------------------------------------------------------
# 4. Add security status function
# ---------------------------------------------------------

status_marker = """
/* ============================================================
   LOAD SECURITY SUMMARY
============================================================ */
"""

status_function = """/* ============================================================
   SECURITY STATUS
============================================================ */

function updateSecurityStatus(status) {

    const statusElement =
        document.getElementById(
            "securityStatus"
        );

    const statusText =
        document.getElementById(
            "securityStatusText"
        );

    if (!statusElement || !statusText) {
        return;
    }

    statusElement.classList.remove(
        "warning",
        "error"
    );

    if (status === "ERROR") {

        statusElement.classList.add(
            "error"
        );

        statusText.textContent =
            "ERROR";

        return;
    }

    if (status === "WARNING") {

        statusElement.classList.add(
            "warning"
        );

        statusText.textContent =
            "WARNING";

        return;
    }

    statusText.textContent =
        "OPERATIONAL";
}


/* ============================================================
   LOAD SECURITY SUMMARY
============================================================ */
"""

if "function updateSecurityStatus(status)" not in html:
    html = html.replace(
        status_marker,
        status_function,
        1
    )


# ---------------------------------------------------------
# 5. Update attack-test status
# ---------------------------------------------------------

attack_success_marker = """
        document.getElementById(
            "attackTestsFailed"
        ).textContent =
            data.failed ?? 0;

    } catch (error) {
"""

attack_success_replacement = """
        document.getElementById(
            "attackTestsFailed"
        ).textContent =
            data.failed ?? 0;

        const attackStatus =
            document.getElementById(
                "attackStatus"
            );

        if (attackStatus) {

            if ((data.failed ?? 0) === 0) {

                attackStatus.innerHTML =
                    "Attack tests: <strong>ALL PASSED</strong>";

            } else {

                attackStatus.innerHTML =
                    "Attack tests: <strong>" +
                    data.failed +
                    " FAILED</strong>";

                updateSecurityStatus("WARNING");
            }
        }

    } catch (error) {
"""

if attack_success_marker not in html:
    raise SystemExit("Attack-test section not found.")

html = html.replace(
    attack_success_marker,
    attack_success_replacement,
    1
)


# ---------------------------------------------------------
# 6. Add automatic dashboard refresh
# ---------------------------------------------------------

auto_refresh_marker = """
/* ============================================================
   END
============================================================ */
"""

auto_refresh_code = """
/* ============================================================
   AUTOMATIC SECURITY DASHBOARD REFRESH
============================================================ */

setInterval(
    function () {

        if (
            securityDashboard.classList.contains(
                "visible"
            )
        ) {

            refreshSecurityDashboard();

        }

    },
    15000
);


/* ============================================================
   END
============================================================ */
"""

if "AUTOMATIC SECURITY DASHBOARD REFRESH" not in html:
    html = html.replace(
        auto_refresh_marker,
        auto_refresh_code,
        1
    )


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

FILE.write_text(
    html,
    encoding="utf-8"
)

print()
print("=" * 60)
print("DASHBOARD UPDATE COMPLETE")
print("=" * 60)
print()
print("Updated:")
print("- Security status")
print("- Last updated time")
print("- Attack test status")
print("- Automatic 15-second refresh")
print()
print("File:")
print(FILE)
print()
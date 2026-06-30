import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI DevOps Incident Assistant",
    page_icon="AI",
    layout="wide"
)

st.title("AI DevOps Incident Assistant")
st.success("GitHub Actions demo: this text was added locally and pushed through CI/CD.")
st.write("Practical demo: AI-assisted DevOps incident analysis using logs and server health.")

st.divider()

sample_log = """2026-06-30 09:15:21 INFO Application started successfully
2026-06-30 09:18:44 WARN High response time detected on /login
2026-06-30 09:20:03 ERROR Database connection timeout for user login service
2026-06-30 09:20:05 ERROR Failed to connect to PostgreSQL database at db-prod:5432
2026-06-30 09:21:10 ERROR Login service returned HTTP 503
2026-06-30 09:22:40 WARN Retry attempt failed for database connection
"""

st.subheader("1. Application / Server Logs")

logs = st.text_area(
    "Paste logs here:",
    value=sample_log,
    height=250
)

st.subheader("2. Server Health Checks")

col1, col2, col3 = st.columns(3)

with col1:
    disk_usage = st.slider("Disk Usage %", 0, 100, 72)

with col2:
    memory_usage = st.slider("Memory Usage %", 0, 100, 81)

with col3:
    cpu_usage = st.slider("CPU Usage %", 0, 100, 64)

service_status = st.selectbox(
    "Application Service Status",
    ["running", "failed", "unknown"]
)

st.divider()

def analyze_incident(logs, cpu_usage, memory_usage, disk_usage, service_status):
    logs_lower = logs.lower()

    error_count = logs_lower.count("error")
    warning_count = logs_lower.count("warn")
    timeout_count = logs_lower.count("timeout")
    failed_count = logs_lower.count("failed")

    db_issue = "database" in logs_lower or "postgresql" in logs_lower or "postgres" in logs_lower
    http_503 = "503" in logs_lower
    timeout_issue = "timeout" in logs_lower
    login_issue = "login" in logs_lower

    severity = "Low"

    if service_status == "failed" or http_503 or error_count >= 2:
        severity = "High"
    elif memory_usage > 80 or cpu_usage > 80 or disk_usage > 85:
        severity = "Medium"

    if db_issue and timeout_issue:
        summary = "The application is experiencing login failures due to database connection timeout."
        root_cause = "The most likely root cause is that the application cannot connect to the PostgreSQL database on port 5432."
    elif http_503:
        summary = "The application is returning HTTP 503 service unavailable errors."
        root_cause = "The possible root cause is that the backend service is unavailable, overloaded, or unable to reach a required dependency."
    elif service_status == "failed":
        summary = "The application service appears to be failed."
        root_cause = "The possible root cause is service crash, configuration error, or dependency failure."
    elif error_count > 0:
        summary = "Errors were found in the application logs."
        root_cause = "The exact root cause needs further investigation from logs and service status."
    else:
        summary = "No major application error was detected from the provided logs."
        root_cause = "System appears mostly healthy based on current input."

    impact = "Users may not be able to log in or access the application properly." if login_issue or http_503 else "Application performance or availability may be affected."

    commands = []

    if db_issue:
        commands.extend([
            "ping db-prod",
            "nc -vz db-prod 5432",
            "telnet db-prod 5432",
            "systemctl status postgresql",
            "journalctl -u postgresql -n 100"
        ])

    if service_status in ["failed", "unknown"] or http_503:
        commands.extend([
            "systemctl status application-service",
            "journalctl -u application-service -n 100",
            "tail -100 /opt/app/logs/app.log"
        ])

    if cpu_usage > 80:
        commands.append("top")
        commands.append("ps aux --sort=-%cpu | head -10")

    if memory_usage > 80:
        commands.append("free -m")
        commands.append("ps aux --sort=-%mem | head -10")

    if disk_usage > 85:
        commands.append("df -h")
        commands.append("du -sh /var/log/* | sort -h")

    if not commands:
        commands = [
            "tail -100 /opt/app/logs/app.log",
            "systemctl status application-service",
            "df -h",
            "free -m"
        ]

    ticket_update = f"""
Initial investigation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

Severity: {severity}

Issue Summary:
{summary}

Possible Root Cause:
{root_cause}

Impact:
{impact}

Current Server Health:
CPU Usage: {cpu_usage}%
Memory Usage: {memory_usage}%
Disk Usage: {disk_usage}%
Service Status: {service_status}

Next Action:
DevOps team should verify database connectivity, application service status, and recent error logs.
"""

    preventive_action = """
Preventive Actions:
1. Add monitoring alerts for database connection failures.
2. Create alert for HTTP 503 errors.
3. Monitor CPU, memory, and disk usage.
4. Keep application logs centralized in tools like Splunk, Datadog, CloudWatch, or ELK.
5. Use AI to summarize repeated incidents and reduce manual troubleshooting time.
"""

    return {
        "severity": severity,
        "summary": summary,
        "root_cause": root_cause,
        "impact": impact,
        "commands": commands,
        "ticket_update": ticket_update,
        "preventive_action": preventive_action,
        "error_count": error_count,
        "warning_count": warning_count,
        "timeout_count": timeout_count,
        "failed_count": failed_count
    }

if st.button("Analyze Incident"):
    result = analyze_incident(logs, cpu_usage, memory_usage, disk_usage, service_status)

    st.subheader("3. AI DevOps Analysis Result")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Severity", result["severity"])
    col2.metric("Errors", result["error_count"])
    col3.metric("Warnings", result["warning_count"])
    col4.metric("Timeouts", result["timeout_count"])

    if result["severity"] == "High":
        st.error("High severity incident detected.")
    elif result["severity"] == "Medium":
        st.warning("Medium severity issue detected.")
    else:
        st.success("Low severity / no major issue detected.")

    st.subheader("Issue Summary")
    st.write(result["summary"])

    st.subheader("Possible Root Cause")
    st.write(result["root_cause"])

    st.subheader("User / Business Impact")
    st.write(result["impact"])

    st.subheader("Recommended DevOps Commands")
    for command in result["commands"]:
        st.code(command, language="bash")

    st.subheader("Suggested Ticket Update")
    st.text_area("Copy this update into Jira / ServiceNow / Email:", result["ticket_update"], height=280)

    st.subheader("Preventive Action")
    st.write(result["preventive_action"])

    st.divider()

    st.subheader("How this shows AI with DevOps")
    st.write("""
This demo shows how AI can support DevOps by reading logs, checking server health,
detecting possible issues, suggesting troubleshooting commands, and preparing ticket updates.
The engineer still verifies the issue, but AI helps reduce manual log reading and speeds up incident response.
""")
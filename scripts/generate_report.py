from datetime import datetime
from pathlib import Path

report = f"""
# AI DevOps Incident Assistant - Automation Report

Generated at: {datetime.now()}

## What GitHub Actions Did

1. Downloaded the latest code from GitHub
2. Installed Python
3. Installed required packages from requirements.txt
4. Checked app.py for Python errors
5. Generated this report automatically

## Purpose

This shows how DevOps automation works.
When a developer pushes code, GitHub Actions can automatically test, build, scan, or deploy the application.

## AI + DevOps Use Case

This project demonstrates how AI can help DevOps engineers analyze logs, find possible root causes, suggest troubleshooting commands, and prepare ticket updates.
"""

Path("automation_report.md").write_text(report)

print("Automation report generated successfully.")
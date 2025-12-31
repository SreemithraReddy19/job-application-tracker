# Job Application Tracker (CLI)

A simple, no-nonsense **command-line tool** to track job applications using **Python and CSV storage**.

This project is intentionally minimal. It focuses on reliability, clarity, and execution — not UI polish or over-engineering.

---

## Problem

Job hunting quickly turns messy:

- Applications scattered across emails, notes, and spreadsheets
- No single source of truth
- Hard to answer basic questions like:
  - “How many roles have I applied to?”
  - “How many interviews do I currently have?”

This tool solves that by keeping everything in **one CSV file** and interacting with it through a **clean CLI**.

---

## Features

- Add new job applications
- List and filter applications
- Update application status and notes
- View summary statistics
- Prevent duplicate applications (company + role)
- CSV-based storage (portable, transparent, version-controllable)
- Clear error handling and logging (no stack traces for normal errors)

---

## Tech Stack

- Python 3
- `argparse` for CLI parsing
- `pandas` for CSV manipulation
- Python standard library logging

---

## Project Structure

```text
job-tracker/
├── src/
│   ├── main.py        # CLI entry point
│   ├── commands.py    # Command implementations
│   ├── storage.py     # CSV I/O logic
│   └── utils.py       # Validation, constants, logging
├── data/
│   ├── applications.csv
│   └── applications_sample.csv
├── output/
│   └── job_tracker.log
├── requirements.txt
└── README.md

# Job Application Tracker (CLI)

A simple, no‑nonsense **command‑line tool** to track job applications using **Python and CSV storage**. Built to prove execution, not impress with over‑engineering.

This project is intentionally minimal: no UI, no database, no web frameworks. Just a reliable CLI that lets you track applications, update statuses, and see progress at a glance.

---

## Problem

Job hunting quickly turns messy:

* Applications spread across emails, notes, and spreadsheets
* No single source of truth
* Hard to answer basic questions like *"How many roles did I apply to?"* or *"How many interviews do I have?"*

This tool solves that by keeping everything in **one CSV file** and interacting with it through a **clean CLI**.

---

## Features

* Add new job applications
* List and filter applications
* Update application status and notes
* View summary statistics
* CSV‑based storage (portable, transparent, version‑controllable)
* Clear error handling and logging

---

## Tech Stack

* Python 3
* `argparse` for CLI parsing
* `pandas` for CSV manipulation
* Standard library logging

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
│   └── applications.csv
├── output/
│   └── job_tracker.log
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/SreemithraReddy19/job-application-tracker.git
cd job-application-tracker
```

2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Ensure the CSV file exists

```csv
company,role,location,date_applied,status,source,notes
```

---

## Usage

All commands are run from the project root:

```bash
python src/main.py <command> [options]
```

### Add a job application

```bash
python src/main.py add --company "Google" --role "SWE"
```

Defaults:

* `status` → `applied`
* `date_applied` → today

---

### List applications

List all applications:

```bash
python src/main.py list
```

Filter by status:

```bash
python src/main.py list --status interview
```

Filter by company:

```bash
python src/main.py list --company Google
```

---

### Update an application

Update status:

```bash
python src/main.py update --company "Google" --role "SWE" --status interview
```

Update notes:

```bash
python src/main.py update --company "Google" --role "SWE" --notes "HR screen completed"
```

If no matching application is found, the command exits cleanly with a clear message.

---

### Summary statistics

```bash
python src/main.py summary
```

Example output:

```text
Summary
--------------------
Total applications: 3

By status:
  applied: 1
  interview: 2

By source:
  LinkedIn: 2
  Referral: 1
```

---

## Logging

* Logs are written to `output/job_tracker.log`
* User‑facing errors do **not** print stack traces
* Unexpected failures are logged for debugging

---

## Design Decisions

* **CSV over database**: transparent, portable, and easy to inspect
* **No UI**: this is a tooling project, not a product
* **Explicit commands**: predictable, scriptable, and testable

---

## Limitations

* No duplicate detection
* Case‑sensitive matching for company and role
* No authentication or multi‑user support

These are deliberate trade‑offs to keep the project focused.

---

## License

MIT License

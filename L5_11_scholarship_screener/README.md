# Lab 5: Static Code Analysis — Student Scholarship Eligibility Screener

## Overview

This project demonstrates static code analysis using **Pylint, Bandit, and Flake8** to improve the quality, security, style, and maintainability of a Python scholarship eligibility screener.

The program calculates a merit score based on GPA and extracurricular credits, checks family income against an eligibility limit, and saves applicant results to `scholarships.json`.

## Program Functionality

- Calculates merit scores using the formula `GPA × 10 + extracurricular credits × 2`.
- Checks scholarship eligibility against a merit-score cutoff and family-income limit.
- Validates applicant GPA, extracurricular credits, and income.
- Displays the eligible applicants in a shortlist.
- Saves and loads applicant results using JSON.

## Static Analysis Tools

| Tool | Purpose |
|---|---|
| **Pylint** | Detects code-quality problems, naming issues, missing documentation, and potential programming errors. |
| **Bandit** | Identifies potentially insecure Python coding patterns. |
| **Flake8** | Checks Python formatting and PEP 8 style violations. |

## Issues Identified and Fixed

The original program contained several security, reliability, correctness, and style issues.

- **Unsafe `eval()` usage:** Replaced dynamic evaluation with a fixed merit-score calculation.
- **Mutable default argument:** Replaced `logs=[]` with `logs=None` and initialized the list inside the function.
- **Broad exception handling:** Replaced the bare exception handler with specific exception handling.
- **Invalid applicant data:** Added validation for GPA, credits, and income.
- **Unsafe file handling:** Used context managers and explicit UTF-8 encoding.
- **Unused imports:** Removed unnecessary imports.
- **Naming and formatting violations:** Applied `snake_case`, improved formatting, and corrected Boolean comparisons.
- **Missing documentation:** Added module and function docstrings.

The cleaned implementation preserves the scholarship-screening workflow while rejecting invalid applicant data.

## Running the Project

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install the analysis tools

```bash
pip install pylint bandit flake8
```

### 3. Run the program

```bash
python scholarship_system.py
```

The program evaluates the sample applicants, rejects invalid data, displays the shortlist, and saves the results to `scholarships.json`.

### 4. Run static analysis

```bash
pylint scholarship_system.py
bandit -r scholarship_system.py
flake8 scholarship_system.py
```

### 5. Generate analysis reports

Before-fix reports:

```bash
pylint scholarship_system.py > pylint_report.txt
bandit -r scholarship_system.py > bandit_report.txt
flake8 scholarship_system.py > flake8_report.txt
```

After-fix reports:

```bash
pylint scholarship_system.py > pylint_report_after.txt
bandit -r scholarship_system.py > bandit_report_after.txt 2>&1
flake8 scholarship_system.py > flake8_report_after.txt
```

## Final Analysis Results

| Tool | Final result |
|---|---|
| Pylint | **10.00/10** |
| Bandit | No issues identified |
| Flake8 | No errors reported |

The final program was also executed to verify that invalid applicant data is rejected and eligible applicants are shortlisted.

## Project Files

| File | Description |
|---|---|
| `sch

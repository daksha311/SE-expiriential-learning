# L6_L7_11 — Amusement Park Ride Access

## Lab 6: Code and Branch Coverage Analysis

### About the Project

This project focuses on testing the Amusement Park Ride Access application using **code coverage** and **branch coverage** techniques.

The application manages theme park ride admissions based on rider height, age groups, medical restrictions, and ride requirements. It also monitors safety restraint latch sensors.

The objective of Lab 6 is to develop test cases that exercise the application's statements and decision branches and measure the achieved coverage.

### Files and Deliverables

| File | Description |
|---|---|
| `amusement_park_ride_access.py` | Original application module under test. |
| `test_amusement_park.py` | Starter test file provided for the lab. |
| `CodeCoverageTest_dakshasg_application.py` | Test cases developed to achieve code coverage. |
| `BranchCoverageTest_dakshasg_application.py` | Test cases developed to achieve branch coverage. |
| `CodeCoverage_Screenshot.png` | Screenshot showing the code coverage results. |
| `BranchCoverage_Screenshot.png` | Screenshot showing the branch coverage results. |

### Coverage Results

The following results were achieved for the application module:

| Coverage Type | Coverage Achieved | Required Coverage |
|---|---:|---:|
| Code Coverage | 100% | 90% |
| Branch Coverage | 100% | 90% |

Both coverage results exceed the minimum requirement of 90%.

### How to Run the Tests

**Prerequisites**

Install the required testing and coverage packages:

```bash
pip install pytest coverage
```

**1. Run Code Coverage Tests**

```bash
coverage erase
coverage run -m pytest CodeCoverageTest_dakshasg_application.py
coverage report -m
```

**2. Run Branch Coverage Tests**

```bash
coverage erase
coverage run --branch -m pytest BranchCoverageTest_dakshasg_application.py
coverage report -m
```

The `--branch` option enables branch coverage measurement.

### Screenshots

The screenshots below show the achieved coverage results:

- **Code Coverage:** `CodeCoverage_Screenshot.png`
- **Branch Coverage:** `BranchCoverage_Screenshot.png`

### Notes

- The original application file was not modified.
- Separate test files were created for code coverage and branch coverage.
- All tests passed successfully.
- The work for Lab 6 is maintained in this folder. Lab 7 will be added to the repository later.

---

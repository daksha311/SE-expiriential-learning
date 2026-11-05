
"""Screen applicants for scholarship eligibility."""

import json

# Global state
results = {}
INCOME_LIMIT = 800000
CUTOFF = 85


def calculate_merit_score(gpa, extracurricular_credits):
    """Calculate merit using GPA and extracurricular credits."""
    return gpa * 10 + extracurricular_credits * 2


def evaluate_applicant(student_id, test_scores, logs=None):
    """Evaluate an applicant and record their merit score."""
    if logs is None:
        logs = []

    gpa = test_scores.get("gpa")
    extracurricular_credits = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)

    if (
        isinstance(gpa, bool)
        or not isinstance(gpa, (int, float))
        or not 0 <= gpa <= 10
    ):
        raise ValueError("GPA must be between 0 and 10.")

    if (
        isinstance(extracurricular_credits, bool)
        or not isinstance(extracurricular_credits, int)
        or extracurricular_credits < 0
    ):
        raise ValueError("Credits must be a non-negative integer.")

    if (
        isinstance(income, bool)
        or not isinstance(income, (int, float))
        or income < 0
    ):
        raise ValueError("Income must be a non-negative number.")

    score = calculate_merit_score(gpa, extracurricular_credits)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {
        "score": score,
        "eligible": eligible,
    }

    logs.append(f"{student_id} scored {score}")
    return eligible


def persist_results(file="scholarships.json"):
    """Save scholarship results to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, indent=4)


def load_results(file="scholarships.json"):
    """Load saved scholarship results from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_results = json.load(input_file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as error:
        raise ValueError(
            "The results file contains invalid JSON."
        ) from error

    if not isinstance(loaded_results, dict):
        raise ValueError("The results file must contain a JSON object.")

    return loaded_results


def print_shortlist():
    """Print shortlisted applicants and their scores."""
    print("Shortlisted applicants:")

    for student_id, applicant in results.items():
        if applicant["eligible"]:
            print(f"  {student_id} score = {applicant['score']}")


def main():
    """Run the scholarship screening workflow."""
    applicants = {
        "U001": {"gpa": 9.1, "credits": 4, "income": 450000},
        "U002": {"gpa": 7.2, "credits": 1, "income": 300000},
        "U003": {"gpa": 12.5, "credits": -3, "income": -1},
        "U004": {"gpa": 6.5},
        "U005": {"gpa": 8.4, "credits": 3, "income": 600000},
    }

    logs = []

    for student_id, test_scores in applicants.items():
        try:
            evaluate_applicant(student_id, test_scores, logs)
        except (KeyError, ValueError) as error:
            print(f"Skipping {student_id}: {error}")

    persist_results()
    loaded_results = load_results()
    results.update(loaded_results)
    print_shortlist()


if __name__ == "__main__":
    main()

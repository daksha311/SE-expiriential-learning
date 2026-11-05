# Lab 5 — Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe `eval()` | Security — Medium | 12 | Executes a dynamically supplied Python expression and can allow arbitrary code execution. | Replace `eval()` with a fixed merit-score calculation. |
| Bare exception with `pass` | Security / Reliability — Low | 37–38 | Suppresses all exceptions and hides file-reading and JSON-parsing failures. | Catch specific exceptions and handle them explicitly. |
| Mutable default argument | Bug / Quality | 14 | `logs=[]` reuses the same list across function calls that omit the argument. | Use `logs=None` and initialize a fresh list inside the function. |
| Invalid applicant data | Logic / Validation | 49–52 | U003 has GPA 12.5, negative credits and negative income, yet qualifies for the shortlist. | Validate GPA, credits and income before computing eligibility. |
| Unsafe file handling | Reliability / Quality | 29, 36 | Files are opened without context managers or explicit encodings. | Use `with open(...)` and specify the encoding. |
| Unused imports | Code quality / Style | 2–3 | `math` and `sys` are imported but never used. | Remove unused imports. |
| Incorrect function naming | Style | 40 | `printShortlist()` does not follow `snake_case`. | Rename it to `print_shortlist()`. |
| Boolean comparison | Style | 43 | Comparing a value to `True` explicitly is unnecessary. | Use `if applicant["eligible"]:`. |
| Missing docstrings | Code quality | Multiple | The module and functions lack explanatory documentation. | Add a module docstring and function docstrings. |
| Formatting violations | Style | Multiple | Flake8 reports blank-line violations and other PEP 8 issues. | Apply consistent Python formatting. |


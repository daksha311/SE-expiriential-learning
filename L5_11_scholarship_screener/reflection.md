# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, poor coding practices and style violations early in development. This improves code quality and maintainability.

### 2. What differences did you observe between Pylint, Bandit and Flake8?

Pylint focuses on code quality, naming, documentation and possible programming errors. Bandit focuses on security risks, such as unsafe use of `eval()`. Flake8 checks Python style and formatting, including whitespace and line-length violations. Using all three provides complementary checks.

### 3. Which issues did you find, and how did you fix them?

I identified unsafe use of `eval()`, a mutable default argument, broad exception handling, insufficient input validation, unsafe file-handling practices and style issues. I replaced dynamic evaluation with a fixed merit formula, initialized lists safely, handled specific exceptions, validated applicant data and used context managers for file operations.

### 4. How did static analysis improve your program, and what are its limitations?

Static analysis helped me identify security and maintainability problems before relying on the program's output. After making changes, I reran the tools to verify improvements. However, static analysis cannot identify every logical error or guarantee correct behavior for every input. Manual review and testing are also necessary.

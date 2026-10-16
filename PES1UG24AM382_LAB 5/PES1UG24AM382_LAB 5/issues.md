# Lab 5: Static Code Analysis — Issue Report

## Objective
To improve the quality, security, and readability of the wildlife sightings program using Pylint, Bandit, and Flake8.

## Issues Identified and Fixes

| No. | Issue | Tool | Severity / Type | Fix Applied |
|---|---|---|---|---|
| 1 | SQL query constructed using string formatting | Bandit B608 | Medium | Replaced string formatting with parameterized SQL queries using placeholders. |
| 2 | Weak MD5 hashing algorithm | Bandit B324 | High | Replaced MD5 with SHA-256 for the short observer identifier. |
| 3 | Use of assert for a runtime check | Bandit B101 | Low | Replaced assert with an explicit conditional and ValueError. |
| 4 | Mutable default argument `extras={}` | Code review / Pylint | Correctness | Changed the default to `None` and initialized a new dictionary when needed. |
| 5 | Function names do not follow Python naming conventions | Pylint | Code quality | Renamed functions using snake_case. |
| 6 | Lines exceeding the recommended length | Flake8 E501 | Style | Split long statements across multiple lines. |
| 7 | Ambiguous variable name `l` | Flake8 E741 | Style | Replaced it with `least_common`. |
| 8 | Missing whitespace around an operator | Flake8 E225 | Style | Corrected spacing around operators. |
| 9 | Empty database not handled by `rarest()` | Code review | Robustness | Added a check to return `None` when there are no sightings. |

## Verification Results

- Pylint before fixes: 3.46/10.
- Pylint after fixes: 10.00/10.
- Bandit after fixes: No issues identified.
- Flake8 after fixes: No violations reported.
- Program execution: Successful.

## Conclusion
Static analysis helped identify security risks, correctness problems, and style violations. The corrected program uses parameterized SQL, improved hashing, safer argument defaults, clearer naming, and consistent formatting. All three analysis tools were rerun to verify the improvements.
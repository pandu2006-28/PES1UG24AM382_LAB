# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis?
Static code analysis examines source code without executing the program to identify potential bugs, security vulnerabilities, and coding-standard violations.

### 2. What did Pylint, Bandit, and Flake8 identify?
Bandit identified unsafe SQL query construction, the use of MD5, and an assert statement. Flake8 identified long lines, an ambiguous variable name, and missing whitespace. Pylint provided an overall code-quality assessment and helped identify improvements.

### 3. How did the fixes improve the program?
Parameterized SQL queries reduced SQL injection risk. Replacing MD5, removing the mutable default argument, improving naming, and correcting formatting made the program safer and easier to maintain.

### 4. Why is static analysis important?
Static analysis helps developers detect problems early, improve code readability, reduce security risks, and maintain consistent coding standards before deploying software.
# **VS Code Linters Configuration**

This document explains how to set up and use **isort**, **black**, **flake8**, **pylint**, and **mypy** in a Python project with **pre-commit** hooks for consistent code quality.

---

## **1. Install Linters**

Use the following command to install the required linters and tools:

```bash
pip install isort black flake8 pylint mypy pre-commit
```

## **2. Verify Linter Execution**

When you commit changes to your repository, pre-commit will automatically:

- Sort imports with `isort`.
- Format code with `black`.
- Lint code with `flake8` and `pylint`.
- Check types with `mypy`.

## **3. Install Types for Mypy**

Install missing types required for `mypy` to work correctly:

```bash
mypy --install-types
```

## **4. Configure `pyproject.toml` for Linters**

Add the following configuration to your `pyproject.toml` file:

```toml
[tool.black]
line-length = 88  # Max line length as per PEP 8
target-version = ["py39"]  # Target Python version
skip-string-normalization = false  # Keep original string format

[tool.isort]
profile = "black"  # Align with Black's formatting
line_length = 88
combine_as_imports = true  # Combine "as" imports
known_third_party = ["numpy", "pandas"]  # Third-party libraries
default_section = "THIRDPARTY"

[tool.flake8]
max-line-length = 88
ignore = ["E203", "W503"]  # Rules conflicting with Black
exclude = [".git", "__pycache__", "venv", "build", "dist"]

[tool.mypy]
python_version = "3.9"
ignore_missing_imports = true
strict_optional = true
warn_unused_ignores = true
check_untyped_defs = true
disallow_untyped_calls = true

[tool.pylint]
disable = [
    "C0103",  # Invalid-name (e.g., snake_case violations)
    "C0114",  # Missing module docstring
    "C0115",  # Missing class docstring
    "C0116",  # Missing function docstring
    "E1101"   # Ignore no-member errors
]
max-line-length = 88
good-names = ["i", "j", "k", "id", "df"]  # Allow short variable names
ignored-modules = ["numpy", "pandas"]
ignored-classes = ["DataFrame"]
jobs = 4  # Parallel linting
```

## **4. Pre-commit Hook Setup**

### **Step 1: Install Pre-commit**

Install pre-commit as a development dependency:

```bash
pip install pre-commit
```

---

### **Step 2: Add `.pre-commit-config.yaml`**

Create a `.pre-commit-config.yaml` file in your project root directory with the following configuration:

```yaml
repos:
  - repo: local
    hooks:
      # isort - Import sorting
      - id: isort
        name: isort (local)
        entry: .venv/Scripts/isort.exe
        language: system
        types: [python]
        files: ^src/.*\.py$  # Only check Python files in src folder

      # black - Code formatter
      - id: black
        name: black (local)
        entry: .venv/Scripts/black.exe
        language: system
        types: [python]
        files: ^src/.*\.py$  # Only check Python files in src folder

      # flake8 - Code linting
      - id: flake8
        name: flake8 (local)
        entry: .venv/Scripts/flake8.exe
        language: system
        types: [python]
        files: ^src/.*\.py$  # Only check Python files in src folder

      # pylint - Code quality checker
      - id: pylint
        name: pylint (local)
        entry: .venv/Scripts/pylint.exe
        language: system
        types: [python]
        files: ^src/.*\.py$  # Only check Python files in src folder

      # mypy - Static type checker
      - id: mypy
        name: mypy (local)
        entry: .venv/Scripts/mypy.exe
        language: system
        types: [python]
        files: ^src/.*\.py$  # Only check Python files in src folder
```

---

### **Step 3: Install Pre-commit**

Run the following command to install pre-commit hooks:

```bash
pre-commit install
```

---

### **Step 4: Refresh Pre-commit Hooks**

Ensure that all pre-commit hooks are up-to-date:

```bash
pre-commit install --install-hooks
```

---

## **5. Run Pre-commit Manually**

To run the pre-commit hooks manually on all files, use:

```bash
pre-commit run --all-files
```

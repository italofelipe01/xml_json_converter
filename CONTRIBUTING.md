# Contributing to XML to JSON Converter

Thank you for your interest in contributing to XML to JSON Converter! We welcome contributions from the community to help improve this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create a new issue on GitHub describing the problem. Include as much detail as possible:

*   Steps to reproduce the issue.
*   Expected behavior.
*   Actual behavior.
*   Screenshots (if applicable).
*   Sample XML file causing the issue.

### Suggesting Enhancements

If you have an idea for a new feature or improvement, please open an issue to discuss it. We appreciate your feedback!

### Pull Requests

1.  **Fork the repository** to your own GitHub account.
2.  **Clone the repository** to your local machine.
3.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b my-feature-branch
    ```
4.  **Make your changes** and commit them with clear, descriptive commit messages.
5.  **Run tests** to ensure your changes don't break existing functionality:
    ```bash
    python -m unittest discover tests
    ```
6.  **Push your branch** to your forked repository.
7.  **Submit a Pull Request** to the main repository.

## Coding Standards

*   Follow PEP 8 guidelines for Python code.
*   Write docstrings for classes and functions.
*   Add unit tests for new features or bug fixes.
*   Use type hinting where appropriate.

## Development Setup

1.  Install dependencies:
    ```bash
    pip install -e .[dev]
    ```
2.  Run tests:
    ```bash
    pytest
    ```

Thank you for your contribution!

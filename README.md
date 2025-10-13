# Adeept RaspTank-V4 Smart Car Kit for Raspberry Pi

[![CI](https://github.com/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-repo/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Adeept RaspTank is an open source intelligent robotics product for artificial intelligence, robotics enthusiasts and students. This product is based on the Raspberry Pi motherboard using the python language and is compatible with the following Raspberry Pi models: 3B,3B+,4,5, etc.

## Resources Links

[RobotName]: Adeept RaspTank-V4 \
[Item Code]: ADR013-V4 \
[Official Raspberry Pi website]: https://www.raspberrypi.org/downloads/    \
[Official website]:  https://www.adeept.com/     \
[GitHub]: https://github.com/adeept/adeept_rasptank2/     


## Getting Support or Providing Advice

Adeept provides free and responsive product and technical support, including but not limited to:   
* Product quality issues 
* Product use and build issues
* Questions regarding the technology employed in our products for learning and education
* Your input and opinions are always welcome

We also encourage your ideas and suggestions for new products and product improvements
For any of the above, you may send us an email to:     \
Technical support: support@adeept.com      \
Customer Service: service@adeept.com


## About Adeept

Adeept was founded in 2015 and is a company dedicated to open source hardware and STEM education services. The Adeept technical team continuously develops new technologies, uses excellent products as technology and service carriers, and provides comprehensive tutorials and after-sales technical support to help users combine learning with entertainment. The main products include various learning kits and robots for Arduino, Raspberry Pi, ESP32 and BBC micro:bit.    \
Adeept is committed to assist customers in their education of robotics, programming and electronic circuits so that they may transform their creative ideas into prototypes and new and innovative products. To this end, our services include but are not limited to:   
* Educational and Entertaining Project Kits for Robots, Smart Cars and Drones
* Educational Kits to Learn Robotic Software Systems for Arduino, Raspberry Pi and micro: bit
* Electronic Component Assortments, Electronic Modules and Specialized Tools
* Product Development and Customization Services


## Copyright

Adeept brand and logo are copyright of Shenzhen Adeept Technology Co., Ltd. and cannot be used without written permission.

## Getting Started

This guide covers setting up your development environment to contribute to the project.

### Prerequisites
- **Python 3.11** (to match the CI environment)
- **Git** for version control
- A **virtual environment** (recommended)

### Setup Instructions

1.  **Create and activate a virtual environment:**
    ```cmd
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Windows (Git bash)
    python -m venv .venv
    .venv/Scripts/activate

    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```cmd
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

3.  **Install Playwright browsers (for E2E tests):**
    ```cmd
    python -m playwright install
    ```

## Project Structure

Here is a brief overview of the key directories in this project:

-   `.github/workflows/`: CI/CD pipeline configurations.
-   `bdd/`: Behavior-Driven Development (BDD) tests, including feature files and step definitions.
-   `controller_web/`: Standalone web UI for controlling the robot.
-   `documentation/`: Project documentation, including requirements and user stories.
-   `scripts/`: Helper and automation scripts (e.g., local CI runner, mock server).
-   `src/`: Core Python source code for the robot's logic and hardware control.
-   `tests/`: Unit and integration tests.

## Development and Testing

You can run the same checks locally that our GitHub Actions CI runs.

### Run All CI Checks

To run all checks (formatting, linting, tests, and dependency audit) locally, use:
```cmd
python -m scripts.ci all
```

### Run Individual Checks

-   **Format check (Black):**
    ```cmd
    python -m scripts.ci format
    ```
-   **Lint (Pylint):**
    ```cmd
    python -m scripts.ci lint
    ```
-   **Unit Tests (Pytest):**
    ```cmd
    python -m scripts.ci test
    ```
-   **BDD Tests (Pytest-BDD):**
    ```cmd
    python -m scripts.ci bdd
    ```
-   **Vulnerability Audit (pip-audit):**
    ```cmd
    python -m scripts.ci audit
    ```

## Project Requirements

For a concise, product‑oriented overview of what the RaspTank should do and how it should behave, see REQUIREMENTS.md.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to the project, including the curated working set policy and code style standards.

## Troubleshooting

### Common Issues

- **MSVC Build Tools Error on Windows**: If you encounter "Microsoft Visual C++ 14.0 or greater is required," install Microsoft C++ Build Tools or use conda for prebuilt packages.
- **Playwright Browser Installation**: Run `python -m playwright install` after setting up your environment.
- **BDD Tests Failing**: Ensure `pytest-bdd` is installed and step definitions are correctly imported.

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page for known problems.
- Contact support at support@adeept.com for product-specific questions.

## High‑Level Requirements

Authoritative requirements content is maintained in documentation/requirements.md.

- For the complete set of current high‑level requirements, see: documentation/requirements.md
- For how to author, update, and verify requirements, see: documentation/project_structure.md (section "Requirements Rules").

Change management:
- Propose edits via pull request, following the Requirements Rules (IDs, verification methods, traceability, and lifecycle states).
- Keep links between User Stories (documentation/user_stories.md), Requirements (documentation/requirements.md), code (src/**), and tests (tests/**) up to date.

# Adeept RaspTank-V4 Smart Car Kit for Raspberry Pi
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


## Project Requirements

For a concise, product‑oriented overview of what the RaspTank should do and how it should behave, see REQUIREMENTS.md.


## Project policy: curated working set and .junie

This repository uses a strict default‑deny .gitignore to keep day‑to‑day work focused. By default only these areas are tracked and expected to change:
- src/**
- tests/**
- scripts/**
- .github/**
- controller_web/**
- .junie/**

All other top‑level content is ignored unless explicitly whitelisted. If you need to add a new top‑level area, propose it via PR and update both the root .gitignore and .junie/config.yaml.

About .junie:
- .junie/config.yaml — machine‑readable policy with allowed paths, tracked root files, and guardrails (code style, linting hints, security notes). Tooling and CI scripts can read this to honor the curated set.
- .junie/rules.md — human‑readable guidelines covering directory policy, code quality, testing/CI, security, and change management.

Typical tasks:
- Extend curated areas: edit .gitignore (un‑ignore the folder) and add the pattern to allowed_paths in .junie/config.yaml; document the new area in this README.
- Update guidelines: modify .junie/rules.md (and config.yaml if needed) in a dedicated PR.

Note: Coverage and other generated artifacts (coverage.xml, htmlcov/, junit.xml) are ignored by default; CI produces and uploads its own artifacts.


## Run the full CI locally

You can run the same checks locally that our GitHub Actions CI runs (format, lint, tests with coverage, and dependency audit).

Prerequisites:
- Python 3.13 (to match CI) or a compatible Python 3.x
- Git
- A virtual environment is strongly recommended

Create and activate a virtual environment

Windows (cmd.exe):
```cmd
python -m venv .venv
.venv\Scripts\activate
```

Windows (git Bash):
```cmd
python -m venv .venv
.venv/Scripts/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
# If execution of scripts is restricted, run this once in the shell (requires admin for persistent changes):
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

macOS / Linux (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade pip and install dependencies and developer tools

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black pylint pytest pytest-cov pip-audit
```

Install Playwright browser binaries (required for E2E tests):

```cmd
python -m playwright install
```

Run all CI steps locally

```cmd
python -m scripts.ci all
```

Run individual CI steps

- Format check (Black):
```cmd
python -m scripts.ci format
```

- Lint (Pylint):
```cmd
python -m scripts.ci lint
```

- Tests + coverage (Pytest):
```cmd
python -m scripts.ci test
```

- BDD tests (Pytest-BDD):
```cmd
python -m scripts.ci bdd
```

- Vulnerability audit (pip-audit):
```cmd
python -m scripts.ci audit
```

Notes and troubleshooting

- If any tool is missing, the script will tell you what to install.
- The audit step uses `pip-audit` and checks `requirements.txt` when present, otherwise the current environment.

Common install issue: "Microsoft Visual C++ 14.0 or greater is required"

- Some packages (for example `greenlet`) include C extensions and pip may try to compile them from source on Windows. If you see the MSVC error when running `pip install`, you have two main options:
  1) Install Microsoft C++ Build Tools (recommended if you build other native extensions):
     - https://visualstudio.microsoft.com/visual-cpp-build-tools/
  2) Use conda / conda-forge to install a prebuilt binary (often much easier):
```cmd
conda create -n rasptank -y python=3.11
conda activate rasptank
conda install -c conda-forge greenlet
```
  - Alternatively, create the full conda env from `environment-e2e.yml` which pins conda-forge binaries:
```cmd
conda env create -f environment-e2e.yml -n rasptank-e2e
conda activate rasptank-e2e
```

- If you prefer to stay with pip and your Python version has a compatible wheel for `greenlet`, `pip install -r requirements.txt` should succeed; if not, either install Build Tools or use conda as above.

After running tests

- `junit.xml` and `coverage.xml` are written to the repository root (configured via pyproject.toml), matching the CI artifacts.

# Mock backend for manual UI testing

A simple websocket mock server is provided to test the standalone controller web UI without hardware.

How to run:
- Install dependency (locally only): `pip install websockets`
- Start the server: `python -m scripts.mock_server` (listens on ws://0.0.0.0:8889)
- Open controller_web/index.html in your browser (e.g., double-click or serve statically)
- In the Connection section, set Host to `127.0.0.1` and Port to `8889`, then click Connect.
- Use the buttons and controls; responses are shown in the page log and in the server console.

Notes:
- The mock server implements the same credential handshake: it expects `admin:123456` as the first message.
- The server logs commands and replies with JSON objects that resemble the real backend responses.

# High‑Level Requirements

Authoritative requirements content is maintained in documentation/requirements.md.

- For the complete set of current high‑level requirements, see: documentation/requirements.md
- For how to author, update, and verify requirements, see: documentation/project_structure.md (section "Requirements Rules").

Change management:
- Propose edits via pull request, following the Requirements Rules (IDs, verification methods, traceability, and lifecycle states).
- Keep links between User Stories (documentation/user_stories.md), Requirements (documentation/requirements.md), code (src/**), and tests (tests/**) up to date.

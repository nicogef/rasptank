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


## Run the full CI locally

You can run the same checks locally that our GitHub Actions CI runs (format, lint, tests with coverage, and dependency audit).

Prerequisites:
- Python 3.13 (to match CI) or a compatible Python 3.x
- A virtual environment is recommended
- Install dependencies and dev tools:
  - pip install -r requirements.txt
  - pip install black pylint pytest pytest-cov pip-audit

Run all CI steps:
- python -m scripts.ci all

Run individual steps:
- Format check (Black): python -m scripts.ci format
- Lint (Pylint):       python -m scripts.ci lint
- Tests + coverage:    python -m scripts.ci test
- Vulnerability audit: python -m scripts.ci audit

Outputs (after running tests):
- junit.xml and coverage.xml are written to the repository root (configured via pyproject.toml), same as the CI artifacts.

Notes:
- If any tool is missing, the script will let you know what to install.
- The audit step uses pip-audit and checks requirements.txt when present, otherwise the current environment.


## Mock backend for manual UI testing

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

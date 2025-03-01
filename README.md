# Otus Graduation Project

This repository contains test automation for the Otus Graduation Project. It includes both backend and frontend test
scenarios that can be executed locally or remotely using Selenoid.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running Tests](#running-tests)
    - [Local Execution](#local-execution)
        - [Frontend Tests](#frontend-tests)
        - [Backend Tests](#backend-tests)
    - [Remote Execution with Selenoid](#remote-execution-with-selenoid)
5. [Test Markers](#test-markers)
6. [Troubleshooting](#troubleshooting)
7. [License](#license)

## Overview

The tests in this project are organized into two main categories:

- **Backend Tests:** API tests that verify the application's backend functionality.
- **Frontend Tests:** UI tests executed using Selenium WebDriver.

Tests can be run:

- **Locally:** Directly on your machine.
- **Remotely:** Using Selenoid, a tool for managing Selenium WebDriver instances in Docker containers.

## Prerequisites

Before running the tests, ensure you have the following:

- **Python 3.x:** Installed on your machine.
- **Dependencies:** Required packages such as `pytest`, `selenium`, etc. (see [requirements.txt](requirements.txt)).
- **Application:** The application must be running and accessible via the specified base URL.
- **Selenoid (Optional):** For remote test execution, ensure Selenoid is set up and running. More information is
  available on the [Selenoid website](https://aerokube.com/selenoid/latest/).

## Installation

1. **Clone the repository:**

```bash
   git clone <repository_url>
```

2. Navigate to the project directory:

```bash
cd OtusGraduationProject
```

3. Install dependencies:

```bash
pip install -r requirements.txt.txt
```

## Running Tests

### Local Execution

#### Frontend Tests

To run frontend tests locally, execute the following command:

```bash
pytest src/tests/frontend/pages/test_login.py
```

#### Backend Tests

To run backend tests locally, execute the following command:

```bash
pytest src/tests/backend/reqres/test_reqres_register_api.py
```

#### Remote Execution with Selenoid

To run tests remotely using Selenoid, execute the command below:

```bash
pytest src/tests/frontend/pages/test_login.py  --remote --selenium_url http://localhost:4444/wd/hub
```

Parameters:
• --selenium_url: The URL of your Selenoid hub.
• --remote: A flag indicating that tests should run in a remote environment.

##  Test Markers

To better organize your tests, custom markers are used:
• @pytest.mark.positive: Marks tests that verify expected (successful) behavior.
• @pytest.mark.negative: Marks tests that verify error handling or negative scenarios.

To document these markers, add the following section to your pytest.ini:

```ini
[pytest]
markers =
    positive: marks tests that verify the expected (successful) behavior under normal conditions.
    negative: marks tests that verify the system handles error conditions or invalid inputs gracefully.
```

## Troubleshooting

If you encounter issues while running tests, please verify the following:
• The application is accessible via the specified base URL.
• All dependencies are correctly installed.
• Selenoid is running and accessible (if executing remote tests).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
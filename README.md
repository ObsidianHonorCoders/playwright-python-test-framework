# GlobeSend Transfer QA Automation

A portfolio-sized Python and Playwright example that tests a fictional, local international transfer quotation and draft interface. It makes no real transfers and is not affiliated with any money-transfer provider.

## Architecture

`app/` serves the standalone HTML/JavaScript demo using Python's standard-library HTTP server. `tests/` contains pytest UI tests; `tests/pages/` encapsulates browser interactions in a Page Object Model, and `tests/data/` holds deterministic business values. This keeps the SUT separate from its automation and avoids external services and dependencies.

```text
app/server.py                 Local static application server
app/index.html                Responsive simulated quote and draft UI
tests/pages/transfer_page.py  Page Object
tests/data/quotes.py          Business test values
tests/test_transfer.py        Positive, negative, boundary, regression UI tests
pytest.ini                    Browser, base URL, timeout, failure diagnostics
.github/workflows/tests.yml   GitHub Actions workflow
pyenv/requirements.txt        Python test dependencies
pyenv/setup_venv.bat          Windows environment and browser setup
reports/                      Local generated reports (ignored by Git)
```

## Technology

Python 3.10+, pytest, Playwright for Python, pytest-playwright, pytest-html, and GitHub Actions. Chromium is the supported test browser. No secrets, real personal/payment data, external APIs, or paid services are used.

## Implemented scope and business rules

The form accepts USD as the source and offers MXN/EUR as destinations; only USD-to-MXN is supported. It displays the hardcoded simulated rate of 17.00 MXN per USD and a fixed 3.00 USD fee. Amounts from 1.00 through 5,000.00 USD inclusive are valid. Empty, non-numeric, non-positive, below-minimum, above-maximum, missing-currency, and unsupported-pair input displays an accessible validation message and cannot create a draft. Decimal input is accepted and displayed to two decimal places using JavaScript `toFixed`-style rounding for recipient values. A valid submission generates a demo-only unique reference in the browser; it is not persisted.

Expected example for 100.00 USD: rate `1 USD = 17.00 MXN`, fee `3.00 USD`, recipient `1700.00 MXN`, total `103.00 USD`.

The tests cover quote calculations, a successful draft/reference, empty/zero/negative/non-numeric/too-small/too-large values, missing fields, unsupported pairs, minimum/maximum boundaries, decimal rounding, updated quotes in one session, and rejection without false success.

## Requirements and limitations

Functional: quote a supported pair, show deterministic rate/fee/recipient/total, validate inputs, and show a draft confirmation. Non-functional: responsive accessible labels and feedback, reproducible local execution, and failure screenshots/traces.

This is a demo, not a production-ready or financially secure application. Draft references are ephemeral; no persistence, user accounts, authentication, payment processing, transfer execution, localization, or live exchange rates are implemented. Future improvements could add broader currency-pair coverage, API-backed test fixtures, accessibility scans, and cross-browser CI.

## Setup (Windows PowerShell)

```powershell
.\pyenv\setup_venv.bat
```

The batch file creates `.venv/` at the project root, installs dependencies from `pyenv/requirements.txt`, and installs Chromium. To activate the environment manually afterward:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the app in one terminal:

```powershell
python -m app.server
```

The app is available at `http://127.0.0.1:8000`. In another activated terminal, run:

```powershell
python -m pytest
```

For HTML and JUnit reports:

```powershell
New-Item -ItemType Directory -Force reports | Out-Null
python -m pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml
```

Open `reports/report.html` in a browser; JUnit output is at `reports/junit.xml`. Failed-test screenshots and retained Playwright traces are written under `test-results/` by pytest-playwright. These generated files are excluded from Git. To change the app URL, set pytest-playwright's `--base-url` option.

## CI

GitHub Actions installs Python dependencies and Chromium, starts the local app with a readiness check, runs the same UI suite and report commands, and uploads reports and failure artifacts even when the tests fail. It requires no secrets.

## Example execution

```text
python -m pytest
.............                                                    [100%]
```

Output is illustrative; test results depend on the local environment. The CI job and report command provide the authoritative execution result.

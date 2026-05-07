# Testomat.io UI Test Automation

End-to-end UI test suite for [Testomat.io](https://app.testomat.io) built with **Playwright** and **pytest**.

## Tech Stack

| Tool                             | Version | Purpose              |
|----------------------------------|---------|----------------------|
| Python                           | 3.13+   | Runtime              |
| [uv](https://docs.astral.sh/uv/) | latest  | Package manager      |
| pytest                           | 8.4.1   | Test framework       |
| playwright                       | 1.58.0  | Browser automation   |
| pytest-playwright                | 0.7.2   | Playwright fixtures  |
| faker                            | 40.11.0 | Test data generation |
| ruff                             | 0.9+    | Linter & formatter   |

---

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Install Playwright browsers

```bash
uv run playwright install chromium
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
BASE_URL=https://testomat.io/
BASE_APP_URL=https://app.testomat.io/
EMAIL=your_email@example.com
PASSWORD=your_password
```

> **Note:** Never commit `.env` to version control.

---

## Running Tests

```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/web/login_page_test.py

# Run a specific test
uv run pytest tests/web/login_page_test.py::test_login_with_valid_creds

# Run in headless mode (no browser window)
uv run pytest --headless

# Run with verbose output
uv run pytest -v
```

Tests run against `https://app.testomat.io` in **Chrome** by default. Video recordings are saved to the
`test_result/videos/` directory.

---

## Project Structure

```
testomat_tests/
├── .env                          # Environment variables (not committed)
├── pyproject.toml                # Project config, dependencies, ruff settings
├── uv.lock                       # Locked dependencies for reproducible installs
│
├── src/
│   └── web/
│       ├── application.py        # Application facade — single entry point for all pages
│       ├── pages/                # Page Objects
│       │   ├── home_page.py
│       │   ├── login_page.py
│       │   ├── projects_page.py
│       │   ├── project_page.py
│       │   └── new_projects_page.py
│       └── components/           # Reusable UI components
│           ├── project_card.py
│           ├── project_page_header.py
│           └── side_bar.py
│
├── tests/
│   ├── conftest.py               # Registers fixture plugins
│   ├── fixtures/                 # Fixture definitions
│   │   ├── app.py                # App, auth, and page fixtures
│   │   ├── config.py             # Config/credentials fixture
│   │   ├── cookie_helper.py      # Cookie utility and helper fixture
│   │   └── playwright.py         # Browser launch and context overrides
│   └── web/
│       ├── cookies_test.py
│       ├── login_page_test.py
│       ├── project_creation_test.py
│       └── project_page_test.py
│
└── test_result/                  # Auto-generated (gitignored)
    ├── report.html
    └── videos/
```

---

## Architecture

### Page Object Model (POM)

Each page/component wraps Playwright's `Page` and exposes domain-level methods. All methods return `Self` to support
fluent chaining:

```
app.login_page.open().is_loaded().login_user(email, password)
```

### Application Facade

`src/web/application.py` is a single entry point that holds instances of all pages:

```
app.home_page
app.login_page
app.projects_page
app.new_projects_page
app.project_page
```

Tests only interact with `app` — never with raw Playwright objects.

### Fixtures (`tests/fixtures/`)

| Fixture          | Scope    | Description                                                  |
|------------------|----------|--------------------------------------------------------------|
| `configs`        | session  | Loads credentials and URLs from `.env`                       |
| `app`            | function | Unauthenticated `Application` instance                       |
| `storage_state`  | session  | Logs in via UI once and saves auth state to file             |
| `auth_context`   | session  | Browser context pre-loaded with saved auth state             |
| `logged_app`     | function | `Application` wrapped in the authenticated context           |
| `shared_app`     | function | Shared page per module; clears browser state after each test |
| `module_context` | module   | Shared browser context per module                            |
| `module_page`    | module   | Shared page per module                                       |
| `cookies`        | function | `CookieHelper` instance for cookie manipulation              |
| `login`          | function | Logs in a user within a test via UI                          |

---

## Test Coverage

| Area                 | What's tested                                                                            |
|----------------------|------------------------------------------------------------------------------------------|
| **Login**            | Valid credentials, invalid credentials, empty fields, unregistered email, invalid format |
| **Projects list**    | Page loads, search by name, switch company, grid/table view toggle                       |
| **Project creation** | Create Classical / BDD projects, verify name and navigation                              |
| **Project page**     | Page loads, sidebar navigation, project name verification                                |
| **Cookies**          | Add feature flag cookie, delete cookie, verify presence and value                        |

---

## Code Quality

```bash
# Check for lint issues
uv run ruff check src/

# Auto-fix fixable issues
uv run ruff check --fix src/

# Format code
uv run ruff format src/
```

Ruff is configured with `E`, `W`, and `N` rules (errors, warnings, naming conventions) and a 120-character line length.

---

## Browser Configuration

Set in `tests/fixtures/playwright.py` via Playwright fixture overrides:

| Setting         | Value                     |
|-----------------|---------------------------|
| Browser         | Chrome                    |
| Mode            | Headed (visible window)   |
| Base URL        | `https://app.testomat.io` |
| Viewport        | Full screen               |
| Locale          | `uk-UA`                   |
| Timezone        | `Europe/Kyiv`             |
| Video recording | `test_result/videos/`     |
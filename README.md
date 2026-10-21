# Employee Events Dashboard

A small FastHTML dashboard for exploring employee and team event history,
notes, and model-predicted recruitment risk. The project includes a reusable
`employee_events` Python package and a bundled SQLite database.

## Requirements

Use Python 3.10.10 (the version used by the GitHub Actions workflows). From the
repository root, install the pinned dependencies and the local package:

```bash
python -m pip install -r requirements.txt
```

## Run the dashboard

Start the web app from the repository root:

```bash
python report/dashboard.py
```

Open the local URL printed by FastHTML. Select an employee or team to view
cumulative positive and negative event counts, predicted recruitment risk, and
associated notes.

## Python package and database

The `employee_events` package is installed from `python-package/` by the root
requirements file. It provides `Employee`, `Team`, and `QueryBase` classes for
querying `python-package/employee_events/employee_events.db`. The database is
included in the package distribution.

Build a source distribution with:

```bash
python python-package/setup.py sdist
```

This creates a `.tar.gz` file in `python-package/dist/`.

## Tests

Run the database and package tests from the repository root:

```bash
python -m pytest
```

GitHub Actions runs the test suite on pushes and pull requests to `main`.

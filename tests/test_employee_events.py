import pytest
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_path():
    return project_root / "python-package" / "employee_events" / "employee_events.db"


def test_db_exists(db_path):
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect

    connection = connect(db_path)
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [name for (name,) in name_tuples]


def test_employee_table_exists(table_names):
    assert "employee" in table_names


def test_team_table_exists(table_names):
    assert "team" in table_names


def test_employee_events_table_exists(table_names):
    assert "employee_events" in table_names


def test_package_queries_return_data():
    from employee_events import Employee, Team

    employees = Employee()
    teams = Team()

    assert len(employees.names()) == 25
    assert len(teams.names()) == 5
    assert employees.username(1)
    assert teams.username(1)


def test_dashboard_queries_return_model_data():
    from employee_events import Employee, Team

    employee = Employee()
    team = Team()

    assert {"event_date", "positive_events", "negative_events"} <= set(
        employee.event_counts(1).columns
    )
    assert {"note_date", "note"} <= set(employee.notes(1).columns)
    assert list(employee.model_data(1).columns) == [
        "positive_events",
        "negative_events",
    ]
    assert len(team.model_data(1)) > 0

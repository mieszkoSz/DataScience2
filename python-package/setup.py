from pathlib import Path

from setuptools import find_packages, setup


package_root = Path(__file__).resolve().parent
requirements = [
    requirement.strip()
    for requirement in (package_root / "employee_events" / "requirements.txt")
    .read_text(encoding="utf-8")
    .splitlines()
    if requirement.strip()
]

setup(
    name="employee_events",
    version="0.1.0",
    description="SQL query API for the employee events dashboard",
    packages=find_packages(),
    package_data={"employee_events": ["employee_events.db"]},
    include_package_data=True,
    install_requires=requirements,
)

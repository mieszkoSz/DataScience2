from .query_base import QueryBase
from .sql_execution import query


class Employee(QueryBase):
    name = "employee"

    @query
    def names(self):
        return """
            SELECT first_name || ' ' || last_name AS employee_name,
                   employee_id
            FROM employee
            ORDER BY employee_id
        """

    @query
    def username(self, entity_id):
        entity_id = int(entity_id)
        return f"""
            SELECT first_name || ' ' || last_name AS employee_name
            FROM employee
            WHERE employee_id = {entity_id}
        """

    def model_data(self, entity_id):
        entity_id = int(entity_id)
        return self.pandas_query(f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee
            JOIN employee_events USING(employee_id)
            WHERE employee.employee_id = {entity_id}
        """)

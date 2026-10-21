from .sql_execution import QueryMixin


class QueryBase(QueryMixin):
    name = ""

    def names(self):
        return []

    def event_counts(self, entity_id):
        entity_id = int(entity_id)
        sql_query = f"""
            SELECT event_date,
                   SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee_events
            JOIN {self.name}
              ON employee_events.{self.name}_id = {self.name}.{self.name}_id
            WHERE {self.name}.{self.name}_id = {entity_id}
            GROUP BY event_date
            ORDER BY event_date
        """
        return self.pandas_query(sql_query)

    def notes(self, entity_id):
        entity_id = int(entity_id)
        sql_query = f"""
            SELECT notes.note_date, notes.note
            FROM notes
            JOIN {self.name}
              ON notes.{self.name}_id = {self.name}.{self.name}_id
            WHERE {self.name}.{self.name}_id = {entity_id}
            ORDER BY notes.note_date
        """
        return self.pandas_query(sql_query)

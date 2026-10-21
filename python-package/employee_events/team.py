from .query_base import QueryBase
from .sql_execution import query


class Team(QueryBase):
    name = "team"

    @query
    def names(self):
        return """
            SELECT team_name, team_id
            FROM team
            ORDER BY team_id
        """

    @query
    def username(self, entity_id):
        entity_id = int(entity_id)
        return f"""
            SELECT team_name
            FROM team
            WHERE team_id = {entity_id}
        """

    def model_data(self, entity_id):
        entity_id = int(entity_id)
        return self.pandas_query(f"""
            SELECT positive_events, negative_events
            FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM team
                JOIN employee_events USING(team_id)
                WHERE team.team_id = {entity_id}
                GROUP BY employee_id
            )
        """)

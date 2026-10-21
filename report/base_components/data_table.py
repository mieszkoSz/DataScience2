from .base_component import BaseComponent
from fasthtml.common import Table, Tr, Th, Td


class DataTable(BaseComponent):
    def build_component(self, entity_id, model):
        data = self.component_data(entity_id, model)
        header = Tr(*(Th(str(column)) for column in data.columns))
        rows = [
            Tr(*(Td(str(value)) for value in row))
            for row in data.itertuples(index=False, name=None)
        ]
        return Table(header, *rows)

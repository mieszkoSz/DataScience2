from fasthtml.common import *
from starlette.exceptions import HTTPException

from base_components import (
    BaseComponent,
    DataTable,
    Dropdown,
    MatplotlibViz,
    Radio,
)
from combined_components import CombinedComponent, FormGroup
from employee_events import Employee, QueryBase, Team
from utils import load_model
import matplotlib.pyplot as plt


class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name.title()
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model: QueryBase):
        return model.names()


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(model.name.title())


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        data = model.event_counts(entity_id).fillna(0)
        data = data.set_index('event_date').sort_index().cumsum()
        data.columns = ['Positive', 'Negative']

        fig, ax = plt.subplots(figsize=(10, 4))
        data.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title('Cumulative Employee Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Events')
        fig.tight_layout()
        return fig


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        probabilities = self.predictor.predict_proba(data)[:, 1]
        prediction = probabilities.mean() if model.name == 'team' else probabilities[0]

        fig, ax = plt.subplots(figsize=(8, 2))
        ax.barh([''], [prediction])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        fig.tight_layout()
        return fig


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"
    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
            hx_swap="outerHTML",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app, rt = fast_app()
report = Report()


@rt("/")
def home():
    return report(1, Employee())


@rt("/employee/{employee_id}")
def employee_report(employee_id: int):
    model = Employee()
    if not model.username(employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return report(employee_id, model)


@rt("/team/{team_id}")
def team_report(team_id: int):
    model = Team()
    if not model.username(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
    return report(team_id, model)


@rt('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    if r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())
    raise ValueError("Unsupported profile type")


@rt('/update_data', methods=['POST'])
async def update_data(r):
    data = await r.form()
    profile_type = data.get('profile_type')
    entity_id = data.get('user-selection')
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{entity_id}", status_code=303)
    if profile_type == 'Team':
        return RedirectResponse(f"/team/{entity_id}", status_code=303)
    raise ValueError("Unsupported profile type")


if __name__ == "__main__":
    serve()

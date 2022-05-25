import plotly.graph_objects as go
from dash import dcc, dash_table
from pytemplate import fktemplate


def graph_as_staticplot(figure: go.Figure, config: dict = None) -> dcc.Graph:
    config = {"staticPlot": True} if config is None else config
    return dcc.Graph(figure=figure, config=config)


def create_table_layout(
    dataframe,
    idtable,
    filename=None,
    filedate=None,
    editable: list | bool = False,
    deletable=True,
    renamable=False,
):
    from collections.abc import Iterable

    new_dataframe = dataframe.rename_axis("DATE").reset_index()
    new_dataframe.DATE = new_dataframe.DATE.dt.date

    editable = (
        editable
        if isinstance(editable, Iterable)
        else [editable] * len(new_dataframe.columns)
    )

    table = dash_table.DataTable(
        id=idtable,
        columns=[
            {
                "name": i,
                "id": i,
                "deletable": deletable,
                "renamable": renamable,
                "editable": edit_col,
            }
            for i, edit_col in zip(new_dataframe.columns, editable)
        ],
        data=new_dataframe.to_dict("records"),
        page_size=20,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"font-family": fktemplate.layout.font.family},
        style_header={"font-size": 20, "textAlign": "center", "font-weight": "bold"},
    )
    return table

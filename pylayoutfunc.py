"""Functions to create layout components for Dash apps."""

from collections.abc import Iterable
from dash import dcc, dash_table
import plotly.graph_objects as go
from pytemplate import fktemplate


def graph_as_staticplot(figure: go.Figure, config: dict = None) -> dcc.Graph:
    """
    Converts a plotly figure into a static plot using dcc.Graph.

    Parameters:
        figure (go.Figure): The plotly figure to be converted.
        config (dict, optional): Additional configuration options for the dcc.Graph component.

    Returns:
        dcc.Graph: The converted static plot as a dcc.Graph component.
    """
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
    """
    Create a table layout using Dash DataTable.

    Args:
        dataframe (pandas.DataFrame): The input dataframe to be displayed in the table.
        idtable (str): The ID of the DataTable component.
        filename (str, optional): The filename associated with the table.
            Defaults to None.
        filedate (str, optional): The file date associated with the table.
            Defaults to None.
        editable (list or bool, optional): Specifies the editability of columns.
            If a list is provided, it should have the same length
            as the number of columns in the dataframe. Defaults to False.
        deletable (bool, optional): Specifies whether rows can be deleted. Defaults to True.
        renamable (bool, optional): Specifies whether columns can be renamed. Defaults to False.

    Returns:
        dash_table.DataTable: The created DataTable component.

    """
    _, _ = filename, filedate

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

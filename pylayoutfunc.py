import plotly.graph_objects as go
from dash import dcc


def graph_as_staticplot(figure: go.Figure, config: dict = None) -> dcc.Graph:
    config = {"staticPlot": True} if config is None else config
    return dcc.Graph(figure=figure, config=config)

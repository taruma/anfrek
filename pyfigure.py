"""MODULE FOR GENERATE FIGURE RELATED"""
import plotly.graph_objects as go
from pyconfig import appConfig
from plotly.subplots import make_subplots
import numpy as np
import pytemplate


def generate_watermark(n: int = 1) -> dict:
    """GENERATE DICT WATERMARK FOR SUBPLOTS"""

    n = "" if n == 1 else n
    return dict(
        source=appConfig.TEMPLATE.WATERMARK_SOURCE,
        xref=f"x{n} domain",
        yref=f"y{n} domain",
        x=0.5,
        y=0.5,
        sizex=0.5,
        sizey=0.5,
        xanchor="center",
        yanchor="middle",
        name="watermark",
        layer="below",
        opacity=0.2,
    )


def figure_empty(
    text: str = "", size: int = 40, margin_all: int = 0, height: int = 450
) -> go.Figure:
    """GENERATE FIGURE EMPTY"""

    data = [{"x": [], "y": []}]

    layout = go.Layout(
        title={"text": "", "x": 0.5},
        xaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        margin=dict(t=0, l=margin_all, r=margin_all, b=0),
        annotations=[
            dict(
                name="text",
                text=f"<i>{text}</i>",
                opacity=0.3,
                font_size=size,
                xref="x domain",
                yref="y domain",
                x=0.5,
                y=0.05,
                showarrow=False,
            )
        ],
        height=height,
    )

    return go.Figure(data, layout)


def figure_scatter(dataframe):

    ROWS = 2

    fig = make_subplots(rows=ROWS, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    fig.layout.images = [generate_watermark(n) for n in range(2, ROWS + 1)]

    new_x = np.arange(dataframe.index.size) + 1
    new_y = dataframe.iloc[:, 0]

    data1 = go.Bar(
        x=new_x,
        y=new_y,
        name=dataframe.columns[0],
        showlegend=False,
        # marker_line_width=0,
    )

    data2 = go.Scatter(
        x=new_x,
        y=new_y,
        name=dataframe.columns[0],
        mode="markers",
        showlegend=False,
        marker_size=12,
    )

    data3 = go.Scatter(
        x=new_x,
        y=new_y,
        name=dataframe.columns[0],
        mode="markers+lines",
        showlegend=False,
        hoverinfo="skip",
        line_width=1,
        line_dash="dashdot",
        marker_size=8,
    )

    fig.add_traces(data1, rows=1, cols=1)
    fig.add_traces(data3, rows=1, cols=1)
    fig.add_traces(data2, rows=2, cols=1)
    fig.update_layout(hovermode="x", margin=dict(t=0), bargap=0, dragmode="zoom")
    UPDATE_XAXES = {
        "ticktext": dataframe.index.strftime("%Y"),
        "tickvals": new_x,
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 1,
    }
    UPDATE_YAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 1,
        "fixedrange": True,
        # 'title': '<b>Rainfall (mm)</b>'
    }

    def update_axis(fig, update, n, axis: str = "x"):
        n = "" if n == 1 else n
        fig.update(layout={f"{axis}axis{n}": update})

    for n_row in range(1, ROWS + 1):
        for axis, update in zip(["x", "y"], [UPDATE_XAXES, UPDATE_YAXES]):
            update_axis(fig, update, n_row, axis)

    fig.add_hline(new_y.mean())

    return fig

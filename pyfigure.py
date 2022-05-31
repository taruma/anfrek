"""MODULE FOR GENERATE FIGURE RELATED"""
import plotly.graph_objects as go
from pyconfig import appConfig
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
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


def figure_tabledata(dataframe):

    ROWS = 2

    fig = make_subplots(
        rows=ROWS,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.8, 0.2],
    )

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

    sizeref = 2.0 * dataframe.max().max() / (12**2)

    data2 = go.Scatter(
        x=new_x,
        y=[dataframe.columns[0]] * dataframe.index.size,
        marker_size=new_y.fillna(0),
        marker_sizeref=sizeref,
        marker_line_width=0,
        name=dataframe.columns[0],
        mode="markers",
        showlegend=False,
        hovertemplate="%{customdata:.2f}<extra></extra>",
        customdata=new_y.fillna(0),
        # marker_size=12,
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

    return fig


def figure_statout(dataframe: pd.DataFrame) -> go.Figure:

    COLS = 2
    ROWS = 1

    new_x = dataframe.index.strftime("%Y")
    new_y = dataframe.iloc[:, 0]

    fig = make_subplots(
        rows=ROWS,
        cols=COLS,
        shared_yaxes=True,
        column_widths=[0.8, 0.2],
        horizontal_spacing=0.03,
    )

    fig.layout.images = [generate_watermark(n) for n in range(2, COLS + 1)]

    data_scatter = go.Scatter(
        x=new_x,
        y=new_y,
        mode="markers+lines",
        showlegend=False,
        line_width=1,
        line_dash="dashdot",
        marker_size=8,
        hovertemplate="%{y}<extra></extra>",
    )

    data_boxplot = go.Box(
        y=new_y,
        boxpoints="all",
        jitter=0.3,
        pointpos=-1.5,
        showlegend=False,
        boxmean="sd",
        name=dataframe.columns[0],
    )

    fig.add_trace(data_scatter, row=1, col=1)
    fig.add_trace(data_boxplot, row=1, col=2)

    mean = new_y.mean()
    std = new_y.std()
    meanplus = mean + std
    meanminus = mean - std

    from hidrokit.contrib.taruma import hk151

    lower_bound, upper_bound = hk151.calc_boundary(
        new_y.replace(0, np.nan).dropna().to_frame()
    )

    fig.add_hline(y=mean, row=1, col=1, line_width=2, line_dash="dashdot")
    fig.add_hline(y=meanplus, row=1, col=1, line_width=1, line_dash="longdash")
    fig.add_hline(y=meanminus, row=1, col=1, line_width=1, line_dash="longdash")
    fig.add_hline(y=upper_bound, row=1, col=1, line_width=2, line_dash="dot")
    fig.add_hline(y=lower_bound, row=1, col=1, line_width=2, line_dash="dot")

    fig.add_annotation(
        text=f"<i><b>upper bound: {upper_bound:.3f}</b></i>",
        showarrow=False,
        x=0,
        xref="x domain",
        xanchor="left",
        y=upper_bound,
        yref="y",
        yanchor="bottom",
    )
    fig.add_annotation(
        text=f"<i><b>lower bound: {lower_bound:.3f}</b></i>",
        showarrow=False,
        x=0,
        xref="x domain",
        xanchor="left",
        y=lower_bound,
        yref="y",
        yanchor="top",
    )

    fig.add_annotation(
        text=f"<b>mean: {mean:.3f}</b>",
        showarrow=False,
        x=0,
        xref="x domain",
        y=mean,
        yref="y",
        yanchor="bottom",
    )
    fig.add_annotation(
        text=f"<b>standard deviation: +-{std:.3f}</b>",
        showarrow=False,
        x=1,
        xref="x domain",
        xanchor="right",
        y=mean,
        yref="y",
        yanchor="bottom",
    )

    fig.add_annotation(
        text=f"<b>mean+std: {meanplus:.3f}</b>",
        showarrow=False,
        x=1,
        xref="x domain",
        xanchor="right",
        y=meanplus,
        yref="y",
        yanchor="bottom",
    )

    fig.add_annotation(
        text=f"<b>mean-std: {meanminus:.3f}</b>",
        showarrow=False,
        x=1,
        xref="x domain",
        xanchor="right",
        y=meanminus,
        yref="y",
        yanchor="bottom",
    )

    fig.update_layout(
        hovermode="x",
        dragmode="zoom",
        margin=dict(t=0),
    )

    return fig


def figure_distribution(dataframe: pd.DataFrame) -> go.Figure:

    ROWS = 1
    COLS = 5

    series = dataframe.iloc[:, 0]

    fig = make_subplots(
        rows=ROWS,
        cols=COLS,
        shared_yaxes=True,
        horizontal_spacing=0.02,
        subplot_titles=[
            "Parameter",
            "Normal",
            "Log Normal",
            "Gumbel",
            "Log Pearson III",
        ],
    )

    fig.layout.images = [generate_watermark(n) for n in range(2, COLS + 1)]

    from hidrokit.contrib.taruma import hk158

    Cv, Cs, Ck = hk158.calc_coef(series)

    data_bar = go.Bar(
        x="Cv Cs Ck".split(),
        y=[Cv, Cs, Ck],
        showlegend=False,
    )

    fig.add_traces(data_bar, rows=1, cols=1)
    fig.add_traces(data_bar, rows=1, cols=2)
    fig.add_traces(data_bar, rows=1, cols=3)
    fig.add_traces(data_bar, rows=1, cols=4)
    fig.add_traces(data_bar, rows=1, cols=5)

    fig.update_layout(
        hovermode="x",
        dragmode="zoom",
        margin=dict(t=50),
    )

    return fig

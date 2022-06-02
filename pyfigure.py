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
        horizontal_spacing=0.04,
        subplot_titles=[
            f"<b>{par}</b>"
            for par in [
                "Parameter",
                "Normal",
                "Log Normal",
                "Gumbel",
                "Log Pearson III",
            ]
        ],
    )

    fig.layout.images = [generate_watermark(n) for n in range(2, COLS + 1)]

    from hidrokit.contrib.taruma import hk158

    Cv, Cs, Ck = hk158.calc_coef(series)

    data_bar = go.Bar(
        x="$C_v$ $C_s$ $C_k$".split(),
        y=[Cv, Cs, Ck],
        showlegend=False,
        hovertemplate="%{y}<extra></extra>",
        text=[Cv, Cs, Ck],
        texttemplate="<b>%{text:.5f}</b>",
        textposition="outside",
    )

    fig.add_traces(data_bar, rows=1, cols=1)

    poshl_par = {"row": 1, "col": 1}

    fig.add_hline(Cv, line_width=2, line_dash="solid", **poshl_par)
    fig.add_hline(Cs, line_width=2, line_dash="solid", **poshl_par)
    fig.add_hline(Ck, line_width=2, line_dash="solid", **poshl_par)

    # NORMAL

    x_normal = r"$C_s \approx 0$,$C_k \approx 3$".split(",")

    data_normal = go.Scatter(
        x=x_normal,
        y=[0, 3],
        showlegend=False,
        hoverinfo="skip",
        mode="markers",
        marker_size=15,
    )

    marker_normal = go.Scatter(
        x=x_normal,
        y=[Cs, Ck],
        showlegend=False,
        hoverinfo="skip",
        mode="markers",
        marker_symbol="x-dot",
        marker_size=15,
        marker_line_width=[1] * 2,
        marker_line_color=[pytemplate._FONT_COLOR_TUPLE] * 2,
    )

    postr_normal = {"rows": 1, "cols": 2}
    poshl_normal = {"row": 1, "col": 2, "layer": "below"}

    fig.add_traces(data_normal, **postr_normal)
    fig.add_traces(marker_normal, **postr_normal)
    fig.add_hline(0, line_width=1, line_dash="dashdot", **poshl_normal)
    fig.add_hline(3, line_width=1, line_dash="dashdot", **poshl_normal)
    fig.add_hline(Cs, line_width=2, line_dash="solid", **poshl_normal)
    fig.add_hline(Ck, line_width=2, line_dash="solid", **poshl_normal)

    fig.add_annotation(
        text=f"<b>$C_s = {Cs:.5f}$</b>",
        showarrow=False,
        x=0.5,
        xref="x2 domain",
        xanchor="center",
        y=Cs,
        yref="y2",
        yanchor="bottom",
        yshift=3,
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    fig.add_annotation(
        text=f"<b>$C_k = {Ck:.5f}$</b>",
        showarrow=False,
        x=0.5,
        xref="x2 domain",
        xanchor="center",
        y=Ck,
        yref="y2",
        yanchor="bottom",
        yshift=3,
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    # LOG NORMAL

    x_lognormal = r"$C_s \approx 3$,$C_s \gt 0$,$C_s \approx 3C_v$".split(",")

    data_lognormal = go.Scatter(
        x=x_lognormal,
        y=[3, np.nan, 3 * Cv],
        showlegend=False,
        hoverinfo="skip",
        mode="markers",
        marker_size=15,
    )

    marker_lognormal = go.Scatter(
        x=x_lognormal,
        y=[Cs, Cs, Cs],
        showlegend=False,
        hoverinfo="skip",
        mode="markers",
        marker_symbol="x-dot",
        marker_size=15,
        marker_line_width=[1] * 3,
        marker_line_color=[pytemplate._FONT_COLOR_TUPLE] * 3,
    )

    postr_lognormal = {"rows": 1, "cols": 3}
    poshl_lognormal = {"row": 1, "col": 3, "layer": "below"}

    fig.add_traces(data_lognormal, **postr_lognormal)
    fig.add_traces(marker_lognormal, **postr_lognormal)
    fig.add_vline(x_lognormal[1], line_width=1, line_dash="dashdot", **poshl_lognormal)
    fig.add_hline(3, line_width=1, line_dash="dashdot", **poshl_lognormal)
    fig.add_hline(3 * Cv, line_width=1, line_dash="dashdot", **poshl_lognormal)
    fig.add_hline(Cs, line_width=2, line_dash="solid", **poshl_lognormal)

    fig.add_annotation(
        text=f"<b>$C_s = {Cs:.5f}$</b>",
        showarrow=False,
        x=0.5,
        xref="x3 domain",
        xanchor="center",
        y=Cs,
        yref="y3",
        yanchor="bottom",
        yshift=3,
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    # GUMBEL

    x_gumbel = r"$C_s \approx 1.1396$,$C_k \approx 5.4002$".split(",")

    data_gumbel = go.Scatter(
        x=x_gumbel,
        y=[1.1396, 5.4002],
        showlegend=False,
        hoverinfo="skip",
        mode="markers",
        marker_size=15,
    )

    marker_gumbel = go.Scatter(
        x=x_gumbel,
        y=[Cs, Ck],
        showlegend=False,
        hoverinfo="skip",
        mode="markers",
        marker_symbol="x-dot",
        marker_size=15,
        marker_line_width=[1] * 2,
        marker_line_color=[pytemplate._FONT_COLOR_TUPLE] * 2,
    )

    postr_gumbel = {"rows": 1, "cols": 4}
    poshl_gumbel = {"row": 1, "col": 4, "layer": "below"}

    fig.add_traces(data_gumbel, **postr_gumbel)
    fig.add_traces(marker_gumbel, **postr_gumbel)
    fig.add_hline(1.1396, line_width=1, line_dash="dashdot", **poshl_gumbel)
    fig.add_hline(5.4002, line_width=1, line_dash="dashdot", **poshl_gumbel)
    fig.add_hline(Cs, line_width=2, line_dash="solid", **poshl_gumbel)
    fig.add_hline(Ck, line_width=2, line_dash="solid", **poshl_gumbel)

    fig.add_annotation(
        text=f"<b>$C_s = {Cs:.5f}$</b>",
        showarrow=False,
        x=0.5,
        xref="x4 domain",
        xanchor="center",
        y=Cs,
        yref="y4",
        yanchor="bottom",
        yshift=3,
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    fig.add_annotation(
        text=f"<b>$C_k = {Ck:.5f}$</b>",
        showarrow=False,
        x=0.5,
        xref="x4 domain",
        xanchor="center",
        y=Ck,
        yref="y4",
        yanchor="bottom",
        yshift=3,
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    # LOG PEARSON III

    fig.add_traces([{"x": [], "y": []}], rows=1, cols=5)

    xaxis5 = {
        "title": "",
        "showgrid": False,
        "showticklabels": False,
        "zeroline": False,
    }
    yaxis5 = {
        "title": "",
        "showgrid": False,
        "showticklabels": False,
        "zeroline": False,
    }
    fig.update_layout(xaxis5=xaxis5, yaxis5=yaxis5)
    fig.add_shape(
        type="rect",
        x0=0.1,
        y0=0.1,
        x1=0.9,
        y1=0.9,
        xref="x5 domain",
        yref="y5 domain",
        fillcolor=pytemplate._FONT_COLOR_RGB_ALPHA,
    )
    fig.add_annotation(
        text=r"$\text{No Criteria}$",
        showarrow=False,
        x=0.5,
        xref="x5 domain",
        xanchor="center",
        y=0,
        yref="y5 domain",
        yanchor="top",
        yshift=-3,
    )

    fig.update_layout(
        hovermode="closest",
        dragmode="zoom",
        margin=dict(t=30),
        uniformtext_minsize=16,
        uniformtext_mode="hide",
    )

    fig.update_xaxes(tickfont_size=13)

    return fig


def figure_freq(
    dataframe: pd.DataFrame,
    return_period: list[int],
    src_normal: str,
    src_lognormal: str,
    src_gumbel: str,
    src_logpearson3: str,
) -> go.Figure:
    from hidrokit.contrib.taruma import anfrek
    from itertools import cycle, islice

    ROWS = 2
    COLS = 1

    dataframe = dataframe.iloc[:, 0].replace(0, np.nan).dropna().to_frame()

    fig = make_subplots(
        rows=ROWS,
        cols=COLS,
        shared_xaxes=True,
        vertical_spacing=0.04,
    )

    fig.layout.images = [generate_watermark(n) for n in range(2, ROWS + 1)]

    x_all = np.arange(1, len(return_period) + 1)

    y_normal = (
        anfrek.freq_normal(dataframe, return_period=return_period, source=src_normal)
        .to_numpy()
        .flatten()
    )
    y_lognormal = (
        anfrek.freq_lognormal(
            dataframe, return_period=return_period, source=src_lognormal
        )
        .to_numpy()
        .flatten()
    )
    y_gumbel = (
        anfrek.freq_gumbel(dataframe, return_period=return_period, source=src_gumbel)
        .to_numpy()
        .flatten()
    )
    y_logpearson3 = (
        anfrek.freq_logpearson3(
            dataframe, return_period=return_period, source=src_logpearson3
        )
        .to_numpy()
        .flatten()
    )

    col_y = [y_normal, y_lognormal, y_gumbel, y_logpearson3]
    col_title = "Normal,Log Normal,Gumbel,Log Pearson III".split(",")
    col_symbol = "circle-dot square-dot diamond-dot cross-dot".split()

    data_line = [
        go.Scatter(
            x=x_all,
            y=y,
            name=title,
            mode="markers+lines",
            legendgroup=title,
            legendgrouptitle_text=f"<b>{title}</b>",
            legendgrouptitle_font_size=pytemplate._LEGEND_FONT_SIZE,
            marker_size=12,
            marker_symbol=symbol,
        )
        for y, title, symbol in zip(col_y, col_title, col_symbol)
    ]

    fig.add_traces(data_line, rows=1, cols=1)

    data_bar = [
        go.Bar(x=x_all, y=y, name=title, legendgroup=title)
        for y, title in zip(col_y, col_title)
    ]

    fig.add_traces(data_bar, rows=2, cols=1)

    fig.update_layout(
        hovermode="x",
        dragmode="zoom",
        barmode="group",
        bargap=0.1,
        margin=dict(t=0),
        legend_groupclick="togglegroup",
    )

    UPDATE_XAXES = {
        "ticktext": return_period,
        "tickvals": x_all,
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 1,
        "tickprefix": "<b><i>",
        "ticksuffix": "</b></i>",
    }
    UPDATE_YAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 1,
    }

    def update_axis(fig, update, n, axis: str = "x"):
        n = "" if n == 1 else n
        fig.update(layout={f"{axis}axis{n}": update})

    for n_row in range(1, ROWS + 1):
        for axis, update in zip(["x", "y"], [UPDATE_XAXES, UPDATE_YAXES]):
            update_axis(fig, update, n_row, axis)

    fig.update_layout(xaxis2_title="Return Period")

    fig.update_xaxes(tickfont_size=20)

    colorway_list = pytemplate.fktemplate.layout.colorway
    colors = list(islice(cycle(colorway_list), 4))

    for data, color in zip(fig.data, colors * 2):
        data.marker.color = color

    return fig

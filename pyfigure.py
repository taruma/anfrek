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
        "gridcolor": pytemplate.FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 1,
    }
    UPDATE_YAXES = {
        "gridcolor": pytemplate.FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
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
        text=f"<b>standard deviation: &plusmn;{std:.3f}</b>",
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
        marker_line_color=[pytemplate.FONT_COLOR_TUPLE] * 2,
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
        marker_line_color=[pytemplate.FONT_COLOR_TUPLE] * 3,
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

    fig.add_annotation(
        text=f"${3 * Cv:.2f}$",
        showarrow=False,
        x=1,
        xref="x3 domain",
        xanchor="left",
        y=3 * Cv,
        yref="y3",
        yanchor="middle",
        yshift=0,
        xshift=5,
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
        marker_line_color=[pytemplate.FONT_COLOR_TUPLE] * 2,
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
        fillcolor=pytemplate.FONT_COLOR_RGB_ALPHA,
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
        "gridcolor": pytemplate.FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 1,
        "tickprefix": "<b><i>",
        "ticksuffix": "</b></i>",
    }
    UPDATE_YAXES = {
        "gridcolor": pytemplate.FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
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


def figure_fit_viz(
    dataframe: pd.DataFrame,
    alpha: float,
    src_ks: str,
    src_chisquare: str,
    src_normal: str,
    src_lognormal: str,
    src_gumbel: str,
    src_logpearson3: str,
) -> go.Figure:
    from hidrokit.contrib.taruma import hk140, hk141
    from hidrokit.contrib.taruma import anfrek

    series = dataframe.iloc[:, 0].replace(0, np.nan).dropna()
    dataframe = series.to_frame()

    ROWS = 2
    COLS = 5

    pad_vertical = 0.2 / COLS / 2

    fig = make_subplots(
        rows=ROWS,
        cols=COLS,
        specs=[
            [{"rowspan": 2, "r": pad_vertical}, {}, {}, {}, {}],
            [None, {}, {}, {}, {}],
        ],
        shared_yaxes=True,
        vertical_spacing=0.15,
        horizontal_spacing=0.2 / COLS / 2,
    )

    fig.layout.images = [generate_watermark(n) for n in range(2, (ROWS * COLS))]

    # RANK (1,1)

    bar_x = series.sort_values(ascending=False)
    bar_y = [f"$R_{{{rank}}}$" for rank in range(1, series.size + 1)][::-1]

    bar_rank = go.Bar(
        x=bar_x,
        y=bar_y,
        orientation="h",
        showlegend=False,
        hovertemplate="<b>R<sub>%{customdata}</sub></b>: <i>%{x}</i><extra></extra>",
        customdata=np.arange(1, series.size + 1)[::-1],
    )

    fig.add_trace(bar_rank, row=1, col=1)

    fig.update_layout(
        yaxis={
            "spikethickness": 1,
            "showspikes": True,
            "spikemode": "across",
            "spikedash": "solid",
            "spikesnap": "cursor",
        },
        xaxis={
            "spikethickness": 1,
            "showspikes": True,
            "spikemode": "across",
            "spikedash": "solid",
            "spikesnap": "cursor",
        },
    )

    # KOLMOGOROV-SMIRNOV (CDF)

    ks_normal = hk140.kstest(
        dataframe,
        dist="normal",
        source_dist=src_normal,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )
    ks_lognormal = hk140.kstest(
        dataframe,
        dist="lognormal",
        source_dist=src_lognormal,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )
    ks_gumbel = hk140.kstest(
        dataframe,
        dist="gumbel",
        source_dist=src_gumbel,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )
    ks_logpearson3 = hk140.kstest(
        dataframe,
        dist="logpearson3",
        source_dist=src_logpearson3,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )

    def ks_cdf(ksdf: pd.DataFrame, dist: str) -> list[go.Scatter]:

        x = ksdf.x
        p_w = ksdf.p_w
        p_d = ksdf.p_d
        no = ksdf.no

        return [
            go.Scatter(
                x=x,
                y=p_w,
                mode="markers+lines",
                showlegend=False,
                name="Prob Weibull",
                line_shape="hvh",
                line_color=pytemplate.fktemplate.layout.colorway[0],
                marker_size=8,
                marker_line_width=2,
                marker_line_color=pytemplate.fktemplate.layout.colorway[0],
                marker_symbol="x-thin",
                marker_opacity=0.3,
                hovertemplate="R<sub>%{customdata}</sub>: <b>%{x}</b><br>prob=<b>%{y:.2f}</b>",
                customdata=no,
            ),
            go.Scatter(
                x=x,
                y=p_d,
                mode="markers+lines",
                showlegend=False,
                name=f"Prob {dist}",
                line_shape="spline",
                line_color=pytemplate.fktemplate.layout.colorway[1],
                marker_size=8,
                marker_line_width=2,
                marker_line_color=pytemplate.fktemplate.layout.colorway[1],
                marker_symbol="x-thin",
                marker_opacity=0.3,
                hovertemplate="R<sub>%{customdata}</sub>: <b>%{x}</b><br>prob=<b>%{y:.2f}</b>",
                customdata=no,
            ),
        ]

    # NORMAL

    cdf_normal = ks_cdf(ks_normal, "Normal")
    [fig.add_trace(_graph, row=1, col=2) for _graph in cdf_normal]

    # LOGNORMAL
    cdf_lognormal = ks_cdf(ks_lognormal, "Log Normal")
    [fig.add_trace(_graph, row=1, col=3) for _graph in cdf_lognormal]

    # GUMBEL
    cdf_gumbel = ks_cdf(ks_gumbel, "Gumbel")
    [fig.add_trace(_graph, row=1, col=4) for _graph in cdf_gumbel]

    # LOGPEARSON3
    cdf_logpearson3 = ks_cdf(ks_logpearson3, "Log Pearson III")
    [fig.add_trace(_graph, row=1, col=5) for _graph in cdf_logpearson3]

    # CHI-SQUARE (CLASS)

    # ADD STRIP

    strip = go.Box(
        y=series,
        showlegend=False,
        # alignmentgroup=True,
        boxpoints="all",
        hoverinfo="skip",
        line_color="rgba(255,255,255,0)",
        fillcolor="rgba(255,255,255,0)",
        marker_color=pytemplate.fktemplate.layout.colorway[0],
        marker_symbol="diamond-wide",
        pointpos=0,
        jitter=0.3,
    )

    [fig.add_trace(strip, row=2, col=_col) for _col in range(2, 6)]

    # CLASS SEPARATION

    n_class = hk141._calc_k(series.size)

    # NORMAL

    def create_class_sep(n_class, func_freq, series, func_source):
        # SOURCE: hidrokit.contrib.taruma.hk141 (v0.4.0)
        prob_list = np.linspace(0, 1, n_class + 1)[::-1]
        prob_seq = prob_list[1:-1]

        T = 1 / prob_seq
        val_x = (
            func_freq(series.to_frame(), return_period=T, source=func_source)
            .to_numpy()
            .flatten()
        )

        # Chi Square Table
        seq_x = np.concatenate([[series.min()], val_x, [series.max()]])
        return seq_x

    def shape_class_sep(seperator: np.ndarray, n: int, series: pd.Series):
        # COLOR
        from itertools import cycle, islice

        colorway = pytemplate.fktemplate.layout.colorway
        color = list(islice(cycle(colorway), seperator.size))

        counter = []
        sep_classes = []
        for i, fillcolor in zip(range(1, seperator.size), color):
            fig.add_shape(
                type="rect",
                x0=0,
                y0=seperator[i - 1],
                x1=1,
                y1=seperator[i],
                xref=f"x{n} domain",
                yref=f"y{n}",
                fillcolor=fillcolor,
                opacity=0.2,
                line_width=1,
            )
            left = -np.inf if i == 1 else seperator[i - 1]
            right = np.inf if i == seperator.size - 1 else seperator[i]
            if i == 1:
                _text = f"C<sub>{i}</sub>: <i>x</i> &#8804; {seperator[i]:.3f}"
            elif i == (seperator.size - 1):
                _text = f"C<sub>{i}</sub>: <i>x</i> &gt; {seperator[i-1]:.3f}"
            else:
                _text = f"C<sub>{i}</sub>: {seperator[i-1]:.3f} &lt; <i>x</i> &#8804; {seperator[i]:.3f}"
            counter.append(series.between(left, right, inclusive="right").sum())
            sep_classes.append(_text)

        # print(counter)

        counter_text = "<br>".join(
            [
                f"C<sub>{group}</sub>: <b>{count}</b>"
                for group, count in enumerate(counter, 1)
            ][::-1]
        )
        counter_classes = "<br>".join(sep_classes[::-1])

        fig.add_annotation(
            text=counter_text,
            showarrow=False,
            x=0.02,
            xref=f"x{n} domain",
            xanchor="left",
            y=0.5,
            yref=f"y{n} domain",
            yanchor="middle",
            yshift=2,
            align="left",
            bordercolor=pytemplate.fktemplate.layout.font.color,
            bgcolor=pytemplate.fktemplate.layout.paper_bgcolor,
            borderwidth=1,
            hovertext=counter_classes,
        )

    sep_normal = create_class_sep(n_class, anfrek.freq_normal, series, src_normal)
    shape_class_sep(sep_normal, 6, series)
    sep_lognormal = create_class_sep(
        n_class, anfrek.freq_lognormal, series, src_lognormal
    )
    shape_class_sep(sep_lognormal, 7, series)
    sep_gumbel = create_class_sep(n_class, anfrek.freq_gumbel, series, src_gumbel)
    shape_class_sep(sep_gumbel, 8, series)
    sep_logpearson3 = create_class_sep(
        n_class, anfrek.freq_logpearson3, series, src_logpearson3
    )
    shape_class_sep(sep_logpearson3, 9, series)

    fig.add_annotation(
        text=f"$\\text{{Rank}}(n={{{series.size}}})$",
        showarrow=False,
        x=0,
        xref="x domain",
        xanchor="left",
        y=1,
        yref="y domain",
        yanchor="bottom",
        yshift=2,
    )

    fig.add_annotation(
        text=r"$\text{Kolmogorov-Smirnov (CDF)}$",
        showarrow=False,
        x=0,
        xref="x2 domain",
        xanchor="left",
        y=1,
        yref="y2 domain",
        yanchor="bottom",
        yshift=2,
    )

    fig.add_annotation(
        text=f"$\\text{{Chi-Square ({n_class} Classes)}}$",
        showarrow=False,
        x=0,
        xref="x6 domain",
        xanchor="left",
        y=1,
        yref="y6 domain",
        yanchor="bottom",
        yshift=2,
    )

    fig.update_layout(
        hovermode="closest",
        dragmode="zoom",
        margin=dict(t=30),
    )

    DIST = "Normal,Log Normal,Gumbel,Log Pearson III".split(",")

    UPDATE_YAXIS_KS = {
        "range": [0, 1],
        "spikethickness": 1,
        "showspikes": True,
        "spikemode": "across",
        "spikedash": "solid",
    }
    UPDATE_XAXIS_KS = {
        "showticklabels": False,
        "spikethickness": 1,
        "showspikes": True,
        "spikemode": "across",
        "spikedash": "solid",
    }

    for n, dist in zip(range(2, 6), DIST):
        fig.update(layout={f"yaxis{n}": UPDATE_YAXIS_KS})
        fig.update(layout={f"xaxis{n}": UPDATE_XAXIS_KS})
        fig.add_annotation(
            text=f"$\\text{{{dist}}}$",
            showarrow=False,
            x=0.5,
            xref=f"x{n} domain",
            xanchor="center",
            y=0,
            yref=f"y{n} domain",
            yanchor="top",
            yshift=-4,
        )

    UPDATE_YAXIS_CHI = {"range": [min(series), max(series)]}
    UPDATE_XAXIS_CHI = {"showticklabels": False, "fixedrange": True}

    for n, dist in zip(range(6, 10), DIST):
        fig.update(layout={f"yaxis{n}": UPDATE_YAXIS_CHI})
        fig.update(layout={f"xaxis{n}": UPDATE_XAXIS_CHI})
        fig.add_annotation(
            text=f"$\\text{{{dist}}}$",
            showarrow=False,
            x=0.5,
            xref=f"x{n} domain",
            xanchor="center",
            y=0,
            yref=f"y{n} domain",
            yanchor="top",
            yshift=-4,
        )

    return fig


def figure_fit_result(
    dataframe: pd.DataFrame,
    alpha: float,
    src_ks: str,
    src_chisquare: str,
    src_normal: str,
    src_lognormal: str,
    src_gumbel: str,
    src_logpearson3: str,
) -> go.Figure:
    from hidrokit.contrib.taruma import hk140, hk141

    series = dataframe.iloc[:, 0].replace(0, np.nan).dropna()
    dataframe = series.to_frame()

    ROWS = 2
    COLS = 5

    fig = make_subplots(
        rows=ROWS,
        cols=COLS,
        shared_yaxes=True,
        specs=[
            [{}, {}, {}, {}, {}],
            [
                {},
                {"secondary_y": True},
                {"secondary_y": True},
                {"secondary_y": True},
                {"secondary_y": True},
            ],
        ],
        vertical_spacing=0.17,
        horizontal_spacing=0.2 / COLS,
    )

    fig.layout.images = [generate_watermark(n) for n in range(2, (ROWS * COLS))]

    # KSTEST

    # CRITICAL

    dcr = hk140.calc_dcr(alpha, series.size, source=src_ks)

    bar_dcr = go.Bar(
        x=["Delta Critical"],
        y=[dcr],
        showlegend=False,
        name="Delta Critical",
        width=[0.5],
        text=[dcr],
        texttemplate="<b>%{text:.5f}</b>",
        textposition="auto",
        hoverinfo="skip",
    )

    fig.add_trace(bar_dcr, row=1, col=1)

    # DELTA DISTRIB

    ks_normal = hk140.kstest(
        dataframe,
        dist="normal",
        source_dist=src_normal,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )
    ks_lognormal = hk140.kstest(
        dataframe,
        dist="lognormal",
        source_dist=src_lognormal,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )
    ks_gumbel = hk140.kstest(
        dataframe,
        dist="gumbel",
        source_dist=src_gumbel,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )
    ks_logpearson3 = hk140.kstest(
        dataframe,
        dist="logpearson3",
        source_dist=src_logpearson3,
        alpha=alpha,
        source_dcr=src_ks,
        show_stat=False,
    )

    # PLOT

    def delta_ks(ksdf: pd.DataFrame):

        d = ksdf.d
        no = ksdf.no
        base_color = pytemplate.fktemplate.layout.colorway[0]
        next_color = pytemplate.fktemplate.layout.colorway[1]

        d_max = d.max()
        mask = d == d_max
        marker_size = mask.replace(False, 8).replace(True, 12)
        marker_symbol = mask.replace(False, "x-thin").replace(True, "x-dot")
        marker_opacity = mask.replace(False, 0.3).replace(True, 0.8)
        marker_opacity_bar = mask.replace(False, 0.2).replace(True, 0.5)
        marker_line_color = mask.replace(False, base_color).replace(True, next_color)
        customdata = no.copy()
        customdata[mask] = "max"

        return [
            go.Bar(
                x=no,
                y=d,
                showlegend=False,
                marker_line_width=0,
                marker_color=marker_line_color,
                marker_opacity=marker_opacity_bar,
                hoverinfo="skip",
            ),
            go.Scatter(
                x=no,
                y=d,
                mode="markers+lines",
                showlegend=False,
                line_shape="spline",
                line_color=base_color,
                marker_size=marker_size,
                marker_line_width=2,
                marker_line_color=marker_line_color,
                marker_symbol=marker_symbol,
                marker_opacity=marker_opacity,
                hovertemplate="d<sub>%{customdata}</sub>: <b>%{y:.2f}</b><extra></extra>",
                customdata=customdata,
            ),
        ]

    # NORMAL

    delta_normal = delta_ks(ks_normal)
    [fig.add_trace(_graph, row=1, col=2) for _graph in delta_normal]
    delta_lognormal = delta_ks(ks_lognormal)
    [fig.add_trace(_graph, row=1, col=3) for _graph in delta_lognormal]
    delta_gumbel = delta_ks(ks_gumbel)
    [fig.add_trace(_graph, row=1, col=4) for _graph in delta_gumbel]
    delta_logpearson3 = delta_ks(ks_logpearson3)
    [fig.add_trace(_graph, row=1, col=5) for _graph in delta_logpearson3]

    # CHI SQUARE

    # ADD CRITICAL

    n_class = hk141._calc_k(series.size)
    xcr = hk141.calc_xcr(alpha, dk=hk141._calc_dk(n_class, 2), source=src_chisquare)

    bar_xcr = go.Bar(
        x=["X Critical"],
        y=[xcr],
        showlegend=False,
        name="X Critical",
        width=[0.5],
        text=[xcr],
        texttemplate="<b>%{text:.5f}</b>",
        textposition="auto",
        hoverinfo="skip",
        marker_color=pytemplate.fktemplate.layout.colorway[2],
    )

    fig.add_trace(bar_xcr, row=2, col=1)

    # X DISTRIB

    chi_normal = hk141.chisquare(
        dataframe,
        dist="normal",
        source_dist=src_normal,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    )
    chi_lognormal = hk141.chisquare(
        dataframe,
        dist="lognormal",
        source_dist=src_lognormal,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    )
    chi_gumbel = hk141.chisquare(
        dataframe,
        dist="gumbel",
        source_dist=src_gumbel,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    )
    chi_logpearson3 = hk141.chisquare(
        dataframe,
        dist="logpearson3",
        source_dist=src_logpearson3,
        alpha=alpha,
        source_xcr=src_chisquare,
        show_stat=False,
    )

    # PLOT

    def x_chisquare(chidf: pd.DataFrame, dist: str, xcalc: list = None):
        from itertools import cycle, islice

        fe = chidf.fe
        ft = chidf.ft
        x_calc = np.sum(np.power(2, (fe - ft)) / ft)
        xcalc.append(x_calc)

        no = chidf.index

        colorway_list = pytemplate.fktemplate.layout.colorway
        colors = list(islice(cycle(colorway_list), fe.size))

        return [
            go.Scatter(
                x=[np.mean(no)],
                y=[x_calc],
                showlegend=False,
                mode="markers",
                marker_size=12,
                marker_symbol="x-dot",
                marker_opacity=0.8,
                marker_color=pytemplate.fktemplate.layout.colorway[2],
                marker_line_width=2,
                marker_line_color=pytemplate.fktemplate.layout.font.color,
                hovertemplate="X<sup>2</sup>: <b>%{y:.2f}</b><extra></extra>",
            ),
            go.Bar(
                x=no,
                y=fe,
                marker_line_width=2,
                marker_line_color=pytemplate.FONT_COLOR_RGB_ALPHA.replace(
                    "0.2", "0.8"
                ),
                marker_color=colors,
                marker_opacity=0.1,
                hoverinfo="skip",
                showlegend=False,
                text=fe.to_list(),
                texttemplate="<b>%{text:d}</b>",
                textposition="auto",
                textfont_color=pytemplate.FONT_COLOR_RGB_ALPHA,
            ),
            go.Scatter(
                x=no,
                y=fe,
                mode="lines",
                line_shape="spline",
                line_color=colorway_list[2],
                opacity=0.2,
                hoverinfo="skip",
                showlegend=False,
            ),
        ]

    SECONDARY = (False, True, True)
    xcalc = []

    x2_normal = x_chisquare(chi_normal, "Normal", xcalc)
    [
        fig.add_trace(_graph, row=2, col=2, secondary_y=sec_y)
        for _graph, sec_y in zip(x2_normal, SECONDARY)
    ]

    x2_lognormal = x_chisquare(chi_lognormal, "Log Normal", xcalc)
    [
        fig.add_trace(_graph, row=2, col=3, secondary_y=sec_y)
        for _graph, sec_y in zip(x2_lognormal, SECONDARY)
    ]

    x2_gumbel = x_chisquare(chi_gumbel, "Gumbel", xcalc)
    [
        fig.add_trace(_graph, row=2, col=4, secondary_y=sec_y)
        for _graph, sec_y in zip(x2_gumbel, SECONDARY)
    ]

    x2_logpearson3 = x_chisquare(chi_logpearson3, "Log Pearson III", xcalc)
    [
        fig.add_trace(_graph, row=2, col=5, secondary_y=sec_y)
        for _graph, sec_y in zip(x2_logpearson3, SECONDARY)
    ]

    # [fig.add_trace({"x": [], "y": []}, row=2, col=_col) for _col in range(3, COLS + 1)]

    # ADD LINE

    [
        fig.add_hline(
            dcr, line_width=1, line_dash="dashdot", row=1, col=n, layer="below"
        )
        for n in range(1, 6)
    ]

    [
        fig.add_hline(
            xcr, line_width=1, line_dash="dashdot", row=2, col=n, layer="below"
        )
        for n in range(1, 6)
    ]

    # UPDATE LAYOUT (ANNOTATION)

    UPDATE_XAXIS_KS = {
        "showticklabels": False,
        "fixedrange": False,
    }

    for n, _ksdf in zip(
        range(2, 6), [ks_normal, ks_lognormal, ks_gumbel, ks_logpearson3]
    ):
        fig.add_annotation(
            text=f"$\\text{{max}}(\\Delta)={_ksdf.d.max():.2f}$",
            x=0.02,
            xref=f"x{n} domain",
            xanchor="left",
            y=0.98,
            yref=f"y{n} domain",
            yanchor="top",
            xshift=2,
            yshift=-2,
            showarrow=False,
            font_size=13,
        )

    DIST_KS = [
        r"$\Delta_{\text{Critical}}$",
        r"$\Delta_{\text{Normal}}$",
        r"$\Delta_{\text{Log Normal}}$",
        r"$\Delta_{\text{Gumbel}}$",
        r"$\Delta_{\text{Log Pearson III}}$",
    ]

    for n, dist in zip(range(1, 6), DIST_KS):
        fig.update(layout={f"xaxis{n}": UPDATE_XAXIS_KS})
        fig.add_annotation(
            text=dist,
            showarrow=False,
            x=0.5,
            xref=f"x{n} domain" if n != 1 else "x domain",
            xanchor="center",
            y=0,
            yref=f"y{n} domain" if n != 1 else "y domain",
            yanchor="top",
            yshift=-4,
        )

    fig.add_annotation(
        text=r"$\text{Kolmogorov-Smirnov }(\text{max}(\Delta_{\text{Distribution}}) \le \Delta_{\text{Critical}})$",
        showarrow=False,
        x=0.5,
        xref="x3 domain",
        xanchor="center",
        y=1,
        yref="y3 domain",
        yanchor="bottom",
        yshift=4,
    )

    DIST_CHI = [
        r"$X^2_{\text{Critical}}$",
        r"$X^2_{\text{Normal}}$",
        r"$X^2_{\text{Log Normal}}$",
        r"$X^2_{\text{Gumbel}}$",
        r"$X^2_{\text{Log Pearson III}}$",
    ]

    UPDATE_XAXIS_CHI = {
        "showticklabels": False,
        "fixedrange": False,
        "tickvals": [3],
        "ticktext": ["X<sup>2</sup>"],
    }

    for n_x, n_y, _xcalc in zip(range(7, 11), range(7, 14, 2), xcalc):
        fig.add_annotation(
            text=f"$X^2={_xcalc:.2f}$",
            x=0.02,
            xref=f"x{n_x} domain",
            xanchor="left",
            y=0.98,
            yref=f"y{n_y} domain",
            yanchor="top",
            xshift=2,
            yshift=-2,
            showarrow=False,
            font_size=13,
        )

    for n, dist in zip(range(6, 11), DIST_CHI):
        fig.update(layout={f"xaxis{n}": UPDATE_XAXIS_CHI})
        fig.add_annotation(
            text=dist,
            showarrow=False,
            x=0.5,
            xref=f"x{n} domain",
            xanchor="center",
            y=0,
            yref=f"y{n} domain",
            yanchor="top",
            yshift=-4,
        )

    [
        fig.update(layout={f"yaxis{n}": {"showticklabels": False, "showgrid": False}})
        for n in [8, 10, 12, 14]
    ]

    fig.add_annotation(
        text=r"$\text{Chi-Square }(X^2_{\text{Distribution}} \le X^{2}_{\text{Critical}})$",
        showarrow=False,
        x=0.5,
        xref="x8 domain",
        xanchor="center",
        y=1,
        yref="y8 domain",
        yanchor="bottom",
        yshift=4,
    )

    fig.update_layout(
        margin=dict(t=30, r=0),
        uniformtext_minsize=16,
        uniformtext_mode="hide",
    )

    return fig

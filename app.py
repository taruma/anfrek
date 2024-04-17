"""Main application for Frequency Analysis using Dash."""

from pathlib import Path
from dash import Output, Input, State, dcc, html
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import plotly.io as pio
from pyconfig import appConfig
from pytemplate import fktemplate
import pylayout, pyfunc, pylayoutfunc, pyfigure  # pylint: disable=multiple-imports

pio.templates.default = fktemplate

# DASH APP CONFIG
APP_TITLE = appConfig.DASH_APP.APP_TITLE
HEAD_TITLE = appConfig.DASH_APP.HEAD_TITLE
UPDATE_TITLE = appConfig.DASH_APP.UPDATE_TITLE
DEBUG = appConfig.DASH_APP.DEBUG

# BOOTSTRAP THEME
THEME = appConfig.TEMPLATE.THEME
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.1.2/dbc.min.css"
)

# MAIN APP
app = dash.Dash(
    name=APP_TITLE,
    external_stylesheets=[getattr(dbc.themes, THEME), DBC_CSS],
    title=HEAD_TITLE,
    update_title=UPDATE_TITLE,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
server = app.server

# LAYOUT APP
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        pylayout.HTML_ROW_TITLE,
                        pylayout.HTML_ROW_CREATED_BY,
                        html.Hr(),
                        pylayout.HTML_ROW_NOTE,
                        pylayout.HTML_ROW_BUTTON_UPLOAD,
                        html.Hr(),
                        pylayout.HTML_ROW_BUTTON_EXAMPLE,
                        pylayout.HTML_ROW_BUTTON_DOWNLOAD_TABLE,
                    ],
                    md=3,
                    align="start",
                    class_name="text-center pt-3",
                ),
                dbc.Col(
                    [
                        pylayout.HTML_CARDS,
                    ],
                    class_name="pt-3",
                ),
            ],
        ),
        # pylayout._HTML_TROUBLESHOOTER,
        pylayout.HTML_FOOTER,
    ],
    fluid=True,
    class_name="dbc my-3 px-3",
)

# CALLBACK FUNCTION


@app.callback(
    Output("row-table-data", "children"),
    Output("card-stat", "disabled"),
    Output("card-frequency", "disabled"),
    Output("card-goodness", "disabled"),
    Output("button-download-table", "disabled"),
    Input("dcc-upload", "contents"),
    State("dcc-upload", "filename"),
    State("dcc-upload", "last_modified"),
    Input("button-example", "n_clicks"),
)
def callback_upload(content, filename, filedate, _):
    """Callback function for uploading data and generating table."""

    ctx = dash.ctx
    _ = filedate

    if content is not None:
        report, dataframe = pyfunc.parse_upload_data(content, filename)

    if ctx.triggered_id == "button-example":
        dataframe = pd.read_csv(
            Path(r"./example_data.csv"), index_col=0, parse_dates=True
        )

    tab_stat_disabled = True
    tab_frequency_disabled = True
    tab_goodness_disabled = True
    button_download_disabled = True

    if dataframe is None:
        children = report
    else:
        editable = [False, True]
        children = pylayoutfunc.create_table_layout(
            dataframe,
            "output-table",
            filename=filename,
            editable=editable,
            deletable=False,
        )
        tab_stat_disabled = False
        tab_frequency_disabled = False
        tab_goodness_disabled = False
        button_download_disabled = False

    return (
        children,
        tab_stat_disabled,
        tab_frequency_disabled,
        tab_goodness_disabled,
        button_download_disabled,
    )


@app.callback(
    Output("row-table-viz", "children"),
    Input("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
)
def callback_table_visualize(table_data, table_columns):
    """Callback function for visualizing table data."""

    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    fig = pyfigure.generate_data_viz(dataframe)

    return dcc.Graph(figure=fig)


@app.callback(
    Output("row-stat-statistics", "children"),
    Output("row-stat-distribution", "children"),
    Output("button-stat-download", "outline"),
    Output("button-stat-download", "disabled"),
    Input("button-stat-calc", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
)
def callback_calc_statout(_, table_data, table_columns):
    """Callback function for calculating statistics and distribution."""

    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    fig_statout = pyfigure.generate_statistic_outlier(dataframe)

    fig_dist = pyfigure.generate_distribution_check(dataframe)

    return (
        dcc.Graph(figure=fig_statout),
        dcc.Graph(figure=fig_dist, mathjax=True),
        False,
        False,
    )


@app.callback(
    Output("download-stat", "data"),
    Input("button-stat-download", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
)
def callback_download_stat(_, table_data, table_columns):
    """Callback function for downloading statistics and distribution."""
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)
    text_file = pyfunc.generate_report_statout(dataframe)
    return {"content": text_file, "filename": "STATOUT.TXT"}


@app.callback(
    Output("row-freq-viz", "children"),
    Output("button-freq-download", "outline"),
    Output("button-freq-download", "disabled"),
    Input("button-freq-calc", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("input-freq-return-period", "value"),
    State("select-freq-normal", "value"),
    State("select-freq-lognormal", "value"),
    State("select-freq-gumbel", "value"),
    State("select-freq-logpearson3", "value"),
)
def callback_calc_freq(
    _,
    table_data,
    table_columns,
    return_period,
    src_normal,
    src_lognormal,
    src_gumbel,
    src_logpearson3,
):
    """Callback function for calculating frequency analysis."""
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    return_period = pyfunc.transform_return_period(return_period)

    fig = pyfigure.generate_frequency_analysis(
        dataframe, return_period, src_normal, src_lognormal, src_gumbel, src_logpearson3
    )
    return dcc.Graph(figure=fig), False, False


@app.callback(
    Output("download-freq", "data"),
    Input("button-freq-download", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("input-freq-return-period", "value"),
    State("select-freq-normal", "value"),
    State("select-freq-lognormal", "value"),
    State("select-freq-gumbel", "value"),
    State("select-freq-logpearson3", "value"),
)
def callback_down_freq(
    _,
    table_data,
    table_columns,
    return_period,
    src_normal,
    src_lognormal,
    src_gumbel,
    src_logpearson3,
):
    """Callback function for downloading frequency analysis."""
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    return_period = pyfunc.transform_return_period(return_period)

    result = pyfunc.generate_dataframe_freq(
        dataframe, return_period, src_normal, src_lognormal, src_gumbel, src_logpearson3
    )

    return dcc.send_data_frame(result.to_csv, "FREQUENCY.csv")


@app.callback(
    Output("row-fit-viz", "children"),
    Output("row-fit-result", "children"),
    Output("button-fit-download", "outline"),
    Output("button-fit-download", "disabled"),
    Input("button-fit-calc", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("input-fit-alpha", "value"),
    State("select-fit-ks", "value"),
    State("select-fit-chisquare", "value"),
    State("select-freq-normal", "value"),
    State("select-freq-lognormal", "value"),
    State("select-freq-gumbel", "value"),
    State("select-freq-logpearson3", "value"),
)
def callback_calc_fit(
    _,
    table_data,
    table_columns,
    alpha,
    src_ks,
    src_chisquare,
    src_normal,
    src_lognormal,
    src_gumbel,
    src_logpearson3,
):
    """Callback function for calculating goodness of fit."""
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    alpha = float(alpha)

    fig_fit_viz = pyfigure.generate_goodness_fit_viz(
        dataframe,
        alpha,
        src_ks,
        src_chisquare,
        src_normal,
        src_lognormal,
        src_gumbel,
        src_logpearson3,
    )

    fig_fit_result = pyfigure.generate_goodness_fit_critical(
        dataframe,
        alpha,
        src_ks,
        src_chisquare,
        src_normal,
        src_lognormal,
        src_gumbel,
        src_logpearson3,
    )
    return (
        dcc.Graph(figure=fig_fit_viz, mathjax=True),
        dcc.Graph(figure=fig_fit_result, mathjax=True),
        False,
        False,
    )


@app.callback(
    Output("download-fit-ks", "data"),
    Output("download-fit-chisquare", "data"),
    Output("download-fit", "data"),
    Input("button-fit-download", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("input-fit-alpha", "value"),
    State("select-fit-ks", "value"),
    State("select-fit-chisquare", "value"),
    State("select-freq-normal", "value"),
    State("select-freq-lognormal", "value"),
    State("select-freq-gumbel", "value"),
    State("select-freq-logpearson3", "value"),
)
def callback_download_fit(
    _,
    table_data,
    table_columns,
    alpha,
    src_ks,
    src_chisquare,
    src_normal,
    src_lognormal,
    src_gumbel,
    src_logpearson3,
):
    """Callback function for downloading goodness of fit."""
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    alpha = float(alpha)

    ks_frame, chi_frame, report_fit = pyfunc.generate_report_fit(
        dataframe,
        alpha,
        src_ks,
        src_chisquare,
        src_normal,
        src_lognormal,
        src_gumbel,
        src_logpearson3,
    )

    return (
        dcc.send_data_frame(ks_frame.to_csv, "KS.csv"),
        dcc.send_data_frame(chi_frame.to_csv, "CHI.csv"),
        {"content": report_fit, "filename": "FIT.TXT"},
    )


@app.callback(
    Output("download-table", "data"),
    Input("button-download-table", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
)
def callback_download_table(_, table_data, table_columns):
    """Callback function for downloading table data."""
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    return dcc.send_data_frame(dataframe.to_csv, "TABLE.csv")


if __name__ == "__main__":
    app.run(debug=DEBUG)

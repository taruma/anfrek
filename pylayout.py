"""Layout for Dash App"""

import plotly.io as pio
import dash_bootstrap_components as dbc
from dash import html, dcc
from pyconfig import appConfig
from pytemplate import fktemplate
import pyfigure, pylayoutfunc  # pylint: disable=multiple-imports

pio.templates.default = fktemplate

# LEFT SIDE

HTML_ROW_TITLE = html.Div(
    [
        html.H1(appConfig.DASH_APP.APP_TITLE, className="fw-bold"),
        html.Span(
            html.A(
                [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
                href=appConfig.GITHUB_LINK,
                target="_blank",
            ),
            className="text-muted",
        ),
    ],
    className="my-2",
)

HTML_ROW_BUTTON_UPLOAD = html.Div(
    dcc.Upload(
        dbc.Button(
            "Upload File (.csv)",
            color="primary",
            id="button-upload",
            class_name="m-2",
            size="lg",
        ),
        id="dcc-upload",
        multiple=False,
        # className="d-grid",
    ),
    className="text-center",
)

HTML_ROW_BUTTON_DOWNLOAD_TABLE = html.Div(
    [
        dbc.Button(
            "Download Table (.csv)",
            color="success",
            id="button-download-table",
            class_name="m-2",
            size="sm",
            disabled=True,
        ),
        dcc.Download(id="download-table"),
    ]
)

HTML_ROW_BUTTON_EXAMPLE = html.Div(
    dbc.Button(
        "Example Data (R24, 32 Years)",
        color="secondary",
        id="button-example",
        class_name="m-2",
        size="md",
    )
)

HTML_ROW_CREATED_BY = html.P(
    [
        "created by ",
        html.A("taruma", href="https://github.com/taruma"),
        " & powered by ",
        html.A("hidrokit", href="https://github.com/hidrokit/hidrokit"),
    ],
    className="text-center",
)

HTML_ROW_NOTE = dbc.Alert(
    [
        "fiako-anfrek is "
        " a web application designed for statistical parameter calculation, "
        "distribution type analysis, "
        "frequency analysis, and distribution fit testing.",
    ],
    color="info",
    # className="m-4",
)

# FOOTER

HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022-2024 ",
            html.A(
                "Taruma Sakti Megariansyah",
                href="https://dev.taruma.info/",
            ),
            ".",
        ],
        className="text-muted text-center my-3",
    ),
)

# TAB CONTENT

TAB_DATA = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("TABLE", className="fw-bold text-center"),
                            dcc.Loading(
                                pylayoutfunc.graph_as_staticplot(
                                    pyfigure.generate_empty_figure(
                                        height=700, margin_all=50
                                    )
                                ),
                                id="row-table-data",
                            ),
                        ]
                    ),
                ),
            ],
            md=4,
            className="my-2",
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("VISUALIZATION", className="fw-bold text-center"),
                        dcc.Loading(
                            pylayoutfunc.graph_as_staticplot(
                                pyfigure.generate_empty_figure(
                                    height=700, margin_all=50
                                )
                            ),
                            id="row-table-viz",
                        ),
                    ],
                ),
            ),
            md=8,
            className="my-2",
        ),
    ],
    class_name="mt-3",
)

TAB_STAT = dbc.Row(
    dbc.Col(
        [
            html.Div(
                [
                    dbc.Button(
                        "CALCULATE",
                        id="button-stat-calc",
                        color="warning",
                        size="lg",
                        className="me-3",
                    ),
                    dbc.Button(
                        "DOWNLOAD STATOUT.TXT",
                        id="button-stat-download",
                        color="success",
                        size="lg",
                        className="me-3",
                        outline=True,
                        disabled=True,
                    ),
                    dcc.Download(id="download-stat"),
                ],
                className="mx-3 mb-3 text-center",
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3(
                            "STATISTICS & OUTLIER", className="fw-bold text-center"
                        ),
                        dcc.Loading(
                            pylayoutfunc.graph_as_staticplot(
                                pyfigure.generate_empty_figure(
                                    height=350, margin_all=50
                                )
                            ),
                            id="row-stat-statistics",
                        ),
                    ]
                ),
                className="my-4",
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("DISTRIBUTION", className="fw-bold text-center"),
                        dcc.Loading(
                            pylayoutfunc.graph_as_staticplot(
                                pyfigure.generate_empty_figure(
                                    height=250, margin_all=50
                                )
                            ),
                            id="row-stat-distribution",
                        ),
                    ],
                ),
                className="my-4",
            ),
        ],
    ),
    class_name="mt-3",
)

TAB_FREQ = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("OPTIONS", className="fw-bold text-center"),
                            dbc.Label("Return Period", className="fw-bold"),
                            dbc.Input(
                                value="2 5 10 25 50 100",
                                type="text",
                                id="input-freq-return-period",
                            ),
                            dbc.FormText(
                                "Use Space as Separator", className="text-muted"
                            ),
                            html.H4("SOURCE", className="fw-bold text-center mt-3"),
                            dbc.Label("Normal", className="fw-bold mt-2"),
                            dbc.Select(
                                id="select-freq-normal",
                                options=[
                                    dict(label="SCIPY", value="scipy"),
                                    dict(label="SOEWARNO", value="soewarno"),
                                ],
                                value="scipy",
                            ),
                            dbc.Label("Log Normal", className="fw-bold mt-2"),
                            dbc.Select(
                                id="select-freq-lognormal",
                                options=[
                                    dict(label="SCIPY", value="scipy"),
                                    dict(label="SOEWARNO", value="soewarno"),
                                ],
                                value="scipy",
                            ),
                            dbc.Label("Gumbel", className="fw-bold mt-2"),
                            dbc.Select(
                                id="select-freq-gumbel",
                                options=[
                                    dict(label="GUMBEL", value="gumbel"),
                                    dict(label="SOEWARNO", value="soewarno"),
                                    dict(label="SOETOPO", value="soetopo"),
                                    dict(label="SCIPY", value="scipy"),
                                    dict(label="POWELL", value="powell"),
                                ],
                                value="gumbel",
                            ),
                            dbc.Label("Log Pearson III", className="fw-bold mt-2"),
                            dbc.Select(
                                id="select-freq-logpearson3",
                                options=[
                                    dict(label="SCIPY", value="scipy"),
                                    dict(label="SOEWARNO", value="soewarno"),
                                    dict(label="SOETOPO", value="soetopo"),
                                    dict(label="LIMANTARA", value="limantara"),
                                ],
                                value="scipy",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "CALCULATE",
                                        id="button-freq-calc",
                                        color="warning",
                                        size="md",
                                        className="me-3 my-2",
                                    ),
                                    dbc.Button(
                                        "DOWNLOAD FREQUENCY.CSV",
                                        id="button-freq-download",
                                        color="success",
                                        size="md",
                                        className="me-3 my-2",
                                        outline=True,
                                        disabled=True,
                                    ),
                                    dcc.Download(id="download-freq"),
                                ],
                                className="my-3 text-center",
                            ),
                        ]
                    ),
                ),
            ],
            md=3,
            className="my-2",
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("VISUALIZATION", className="fw-bold text-center"),
                        dcc.Loading(
                            pylayoutfunc.graph_as_staticplot(
                                pyfigure.generate_empty_figure(
                                    height=700, margin_all=50
                                )
                            ),
                            id="row-freq-viz",
                        ),
                    ],
                ),
            ),
            md=9,
            className="my-2",
        ),
    ],
    class_name="mt-3",
)

TAB_FIT = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("OPTIONS", className="fw-bold text-center"),
                            dcc.Markdown(
                                r"The Significance Level ($\alpha$)",
                                mathjax=True,
                                className="fw-bold",
                            ),
                            dbc.Input(
                                value="0.05",
                                type="number",
                                id="input-fit-alpha",
                                min=0,
                                max=1,
                                step=0.01,
                            ),
                            dbc.FormText(
                                "Input as Decimal, 0.05 for 5%", className="text-muted"
                            ),
                            html.H4("SOURCE", className="fw-bold text-center mt-3"),
                            dbc.Label("Kolmogorov-Smirnov", className="fw-bold mt-2"),
                            dbc.Select(
                                id="select-fit-ks",
                                options=[
                                    dict(label="SCIPY", value="scipy"),
                                    dict(label="SOEWARNO", value="soewarno"),
                                    dict(label="SOETOPO", value="soetopo"),
                                ],
                                value="scipy",
                            ),
                            dbc.Label("Chi-Square", className="fw-bold mt-2"),
                            dbc.Select(
                                id="select-fit-chisquare",
                                options=[
                                    dict(label="SCIPY", value="scipy"),
                                    dict(label="LIMANTARA", value="limantara"),
                                ],
                                value="scipy",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "CALCULATE",
                                        id="button-fit-calc",
                                        color="warning",
                                        size="md",
                                        className="me-3 my-2",
                                    ),
                                    dbc.Button(
                                        "DOWNLOAD ALL RESULTS",
                                        id="button-fit-download",
                                        color="success",
                                        size="md",
                                        className="me-3 my-2",
                                        outline=True,
                                        disabled=True,
                                    ),
                                    dcc.Download(id="download-fit-ks"),
                                    dcc.Download(id="download-fit-chisquare"),
                                    dcc.Download(id="download-fit"),
                                ],
                                className="my-3 text-center",
                            ),
                        ]
                    ),
                ),
            ],
            md=3,
            className="my-2",
        ),
        dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3(
                                "GOODNESS OF FIT VISUALIZATION",
                                className="fw-bold text-center",
                            ),
                            dcc.Loading(
                                pylayoutfunc.graph_as_staticplot(
                                    pyfigure.generate_empty_figure(
                                        height=450, margin_all=50
                                    )
                                ),
                                id="row-fit-viz",
                            ),
                        ]
                    ),
                    className="mb-4",
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("RESULTS", className="fw-bold text-center"),
                            dcc.Loading(
                                pylayoutfunc.graph_as_staticplot(
                                    pyfigure.generate_empty_figure(
                                        height=450, margin_all=50
                                    )
                                ),
                                id="row-fit-result",
                            ),
                        ],
                    ),
                    className="my-4",
                ),
            ],
            md=9,
            className="my-2",
        ),
    ],
    class_name="mt-3",
)

HTML_CARDS = dbc.Tabs(
    [
        dbc.Tab(
            TAB_DATA,
            label="TABLE / DATA",
            tab_id="tabid-card-table",
            id="card-table",
            disabled=False,
        ),
        dbc.Tab(
            TAB_STAT,
            label="STATISTICS & OUTLIER",
            tab_id="tabid-card-stat",
            id="card-stat",
            disabled=True,
        ),
        dbc.Tab(
            TAB_FREQ,
            label="FREQUENCY ANALYSIS",
            tab_id="tabid-card-frequency",
            id="card-frequency",
            disabled=True,
        ),
        dbc.Tab(
            TAB_FIT,
            label="GOODNESS OF FIT",
            tab_id="tabid-card-goodness",
            id="card-goodness",
            disabled=True,
        ),
    ],
    active_tab="tabid-card-table",
)

# TEMPORARY

_HTML_TROUBLESHOOTER = html.Div(
    dbc.Container(
        [
            html.Div(id="row-troubleshooter"),
        ],
        fluid=True,
    )
)

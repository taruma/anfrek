import plotly.io as pio

# import pyfigure, pylayoutfunc, pyfunc  # noqa
from dash import html, dcc
from pyconfig import appConfig
from pytemplate import fktemplate
import dash_bootstrap_components as dbc
import pyfigure, pylayoutfunc  # noqa

pio.templates.default = fktemplate

# LEFT SIDE

HTML_ROW_TITLE = html.Div(
    [
        html.H1(appConfig.DASH_APP.APP_TITLE, className="fw-bold"),
        html.Span(
            [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
            className="text-muted",
        ),
    ],
    className="my-2",
)

HTML_ROW_BUTTON_UPLOAD = html.Div(
    dcc.Upload(
        dbc.Button(
            "Drag and Drop or Select File",
            color="info",
            id="button-upload",
            class_name="m-2",
        ),
        id="dcc-upload",
        multiple=False,
        className="d-grid gap-2",
    ),
    className="text-center",
)

HTML_ROW_BUTTON_EXAMPLE = html.Div(
    dbc.Button(
        "Use Example Data", color="secondary", id="button-example", class_name="m-2"
    )
)

# FOOTER

HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022 ",
            html.A(
                "PT. FIAKO ENJINIRING INDONESIA",
                href="https://fiako.co.id/",
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
                                    pyfigure.figure_empty(height=700, margin_all=50)
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
                                pyfigure.figure_empty(height=700, margin_all=50)
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
                    "DOWNLOAD STATOUT.OUT",
                    id="button-stat-download",
                    color="success",
                    size="lg",
                    className="me-3",
                ),
            ],
            className="mx-3 mb-3",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("STATISTICS & OUTLIER", className="fw-bold text-center"),
                    dcc.Loading(
                        pylayoutfunc.graph_as_staticplot(
                            pyfigure.figure_empty(height=350, margin_all=50)
                        ),
                        id="row-stat-statistics",
                    ),
                ]
            ),
            className="my-2",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("DISTRIBUTION", className="fw-bold text-center"),
                    dcc.Loading(
                        pylayoutfunc.graph_as_staticplot(
                            pyfigure.figure_empty(height=450, margin_all=50)
                        ),
                        id="row-stat-distribution",
                    ),
                ],
            ),
            className="my-2",
        ),
    ],
    class_name="mt-3",
)

tab3_freq = ...

tab4_fit = ...

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
            "None",
            label="FREQUENCY ANALYSIS",
            tab_id="tabid-card-frequency",
            id="card-frequency",
            disabled=True,
        ),
        dbc.Tab(
            "None",
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

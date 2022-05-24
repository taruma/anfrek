import plotly.io as pio

# import pyfigure, pylayoutfunc, pyfunc  # noqa
from dash import html, dcc
from pyconfig import appConfig
from pytemplate import fktemplate
import dash_bootstrap_components as dbc
import pyfigure, pylayoutfunc  # noqa

pio.templates.default = fktemplate

HTML_TITLE = html.Div(
    [
        html.H1(appConfig.DASH_APP.APP_TITLE, className="fw-bold"),
        html.Span(
            [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
            className="text-muted",
        ),
    ],
)

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
        className="text-muted mt-5",
    ),
)


tab1_table = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("TABLE/DATA", className="text-center fw-bold"),
                        dcc.Loading(
                            pylayoutfunc.graph_as_staticplot(
                                pyfigure.figure_empty(height=750, margin_all=50)
                            ),
                            id="row-table-data",
                        ),
                    ],
                ),
            ),
            md=8,
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H3("Options:", className="fw-bold text-center"),
                        dbc.Label("Stations:"),
                        dcc.Loading(
                            html.P(
                                "No Available",
                                className="text-muted text-center",
                            ),
                            id="row-table-stations",
                        ),
                        html.P("Click here"),
                    ]
                ),
            ),
        ),
    ],
    class_name="mt-3",
)

tab2_stat = ...

tab3_freq = ...

tab4_fit = ...

HTML_CARDS = dbc.Tabs(
    [
        dbc.Tab(
            tab1_table,
            label="TABLE / DATA",
            tab_id="tabid-card-table",
            id="card-table",
            disabled=False,
        ),
        dbc.Tab(
            "None",
            label="STAT. & OUTLIER",
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

import dash
from pyconfig import appConfig
from pytemplate import fktemplate
import dash_bootstrap_components as dbc
import plotly.io as pio
import pylayout

pio.templates.default = fktemplate

# DASH APP CONFIG
APP_TITLE = appConfig.DASH_APP.APP_TITLE
UPDATE_TITLE = appConfig.DASH_APP.UPDATE_TITLE
DEBUG = appConfig.DASH_APP.DEBUG

# BOOTSTRAP THEME
THEME = appConfig.TEMPLATE.THEME
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)

# MAIN APP
app = dash.Dash(
    name=APP_TITLE,
    external_stylesheets=[getattr(dbc.themes, THEME), DBC_CSS],
    title=APP_TITLE,
    update_title=UPDATE_TITLE,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

# server = app.server

# LAYOUT APP
app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    pylayout.HTML_TITLE,
                    pylayout.HTML_FOOTER,
                ],
                md=3,
                align="center",
                class_name="pt-3",
            ),
            dbc.Col(
                [
                    pylayout.HTML_CARDS,
                ],
                class_name="pt-3",
            ),
        ],
    ),
    fluid=True,
    class_name="dbc my-3 px-3",
)

if __name__ == "__main__":
    app.run_server(debug=DEBUG)

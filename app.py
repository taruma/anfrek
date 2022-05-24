import dash
from pyconfig import appConfig
from pytemplate import fktemplate
import dash_bootstrap_components as dbc
import plotly.io as pio

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

server = app.server

# LAYOUT APP
app.layout = dbc.Container(
    [],
    fluid=False,
    class_name="dbc",
)

if __name__ == "__main__":
    app.run_server(debug=DEBUG)

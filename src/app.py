'''
 # @ Create Time: 2023-12-18 01:20:44.940167
'''

import pathlib
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import folium
from folium import plugins
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import openpyxl

app = Dash(__name__, title="dd1")
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


app.layout = html.Div([
    html.H4('Implement from here'),
])


if __name__ == "__main__":
    app.run_server(debug=True)

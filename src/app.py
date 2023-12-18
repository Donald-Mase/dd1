'''
 # @ Create Time: 2023-12-18 01:20:44.940167
'''

import pathlib
from dash import Dash, dcc, html, Input, Output,dash_table
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
# Source our data using the actual link to your CSV file
csv_link = 'https://raw.githubusercontent.com/Donald-Mutai/Files/main/wfp_food_prices_ken.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_link)
data = pd.read_csv(csv_link)

app.layout = html.Div([
    html.H4('Implement from here'),
    html.Button("Switch Axis", n_clicks=0,
                id='button'),
])


if __name__ == "__main__":
    app.run_server(debug=True)

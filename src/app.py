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
# Source our data using the actual link to your CSV file
csv_link = 'https://raw.githubusercontent.com/Donald-Mutai/Files/main/wfp_food_prices_ken.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_link)
data = pd.read_csv(csv_link)

# csv data to dataframe
df = pd.DataFrame(df)
# data = pd.DataFrame(df)

# adjust for invalid and missing values
df = df.dropna()
df.isnull().sum()

# eliminate the second row to standardize dataframe format
df = df.drop(0)

"""
==========================================================================
Map Visual
"""

mymap = folium.Map([-1.287905, 36.792712], id="folium-map", tiles="cartodbpositron", zoom_start=8, width="100%",
                   height="100%")
locations = list(zip(df.latitude, df.longitude))

# Create a MarkerCluster object
marker_cluster = plugins.MarkerCluster(popups=df['market'].tolist()).add_to(mymap)

# Add individual markers to the MarkerCluster using a loop
for location in locations:
    folium.Marker(location, popup=f'Marker at {location}').add_to(marker_cluster)

# Save the map
mymap.save('map_with_marker_cluster.html')

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, title="dd1")
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


app.layout = html.Div([
    html.H4('Implement from here'),
])


if __name__ == "__main__":
    app.run_server(debug=True)

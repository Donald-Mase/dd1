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
import statsmodels.api as sm

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
df = pd.read_excel('wfp.xlsx', engine='openpyxl', parse_dates=["date"], index_col="date")
# df["date"] = pd.to_datetime(df["date"])
data = pd.read_excel('wfp.xlsx', engine='openpyxl')
datax = pd.read_excel('wfp.xlsx', engine='openpyxl')

data = pd.DataFrame(data)
data = data.drop([0])

datax = pd.DataFrame(datax)
datax = datax.drop([0])

series = df['admin1'].value_counts()
series2 = df['admin2'].value_counts()
series3 = df['market'].value_counts()
series4 = df['commodity'].value_counts()

df_result = pd.DataFrame(series)
df_result2 = pd.DataFrame(series2)
df_result3 = pd.DataFrame(series3)
df_result4 = pd.DataFrame(series4)

df_result = df_result.reset_index()
df_result2 = df_result2.reset_index()
df_result3 = df_result3.reset_index()
df_result4 = df_result4.reset_index()

df_result.columns = ['admin1', 'Total']
df_result2.columns = ['admin2', 'Total']
df_result3.columns = ['market', 'Total']
df_result4.columns = ['commodity', 'Total']


selected = ['date', 'commodity', 'category', 'market', 'unit', 'pricetype', 'price']
selected_df = data[selected]
dash_table = dash_table.DataTable(df.to_dict('records'),
                                  [{"name": i, "id": i} for i in selected_df.tail(15).columns], page_size=15)

# Pie Chart

fig1 = px.pie(df_result,
              values='Total',
              names='admin1',
              labels='admin1',
              title='Pie Chart for Market Proportions Based on Adminstrative Region1 ')

fig12 = go.Figure(
    data=[go.Bar(x=df_result4['commodity'], y=df_result4['Total'], text=df_result4['commodity'], orientation='v')])

# Donut Chart
# Create a figure with a donut chart
fig2 = go.Figure(data=[go.Pie(values=df_result2['Total'], labels=df_result2['admin2'], hole=0.5)])

# Add a title and labels
fig2.update_layout(title='Administrative Region 2 Data Proportions ', xaxis_title='x', yaxis_title='y', height=600)

# Create a figure with a bar chart
fig3 = go.Figure(
    data=[go.Bar(x=df_result3['market'], y=df_result3['Total'], text=df_result3['market'], orientation='v')])

# Add a title and labels
fig3.update_layout(title='Bar Chart on Major Market Proportions Data', xaxis_title='', yaxis_title='Total', height=800)

data['date'] = pd.to_datetime(data['date'])
datax['date'] = pd.to_datetime(datax['date'])

data = data.query("unit == 'KG'")
# maize
data = data.query("commodity == 'Maize'")

# -forecast
data = data.query("priceflag == 'actual'")

# Linechart

fig = px.line(data, x="date", y="price", color="market", hover_name="market", title="Maize Price Series", height=300)

data = data.query("market == 'Nairobi'")

fig14 = px.area(data, x="date", y="price", color="market", hover_name="market", title="Nairobi Maize Price Series")
fig15 = px.scatter(data, x="date", y="price", color="market", hover_name="market", title="Nairobi Maize Price Series",
                   trendline="ols", trendline_scope="overall")


app.layout = html.Div([
    html.H4('Implement from here'),
])


if __name__ == "__main__":
    app.run_server(debug=True)

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
"""
==========================================================================
Markdown Text
"""

datasource_text = dcc.Markdown(
    """
    [Data source:](https://data.humdata.org/dataset/wfp-food-prices-for-kenya?force_layout=desktop)
    Kenya - Food PricesThis dataset contains Food Prices data for Kenya, sourced from the World Food Programme Price Database.
    The World Food Programme Price Database covers foods such as maize, rice, beans, fish, and sugar for 98 countries and some 3000 markets.
    It is updated weekly but contains to a large extent monthly data.
     The data goes back as far as 1992 for a few countries, although many countries started reporting from 2003 or thereafter.
    """
)

Introduction_text = dcc.Markdown(
    """
    The dashboard provides an overview of price trends across multiple regions in Kenya, enabling us to analyze price movements over time and identify contrasts in price changes across various markets.
    By examining the data, we can gain valuable insights into the performance of different commodities and make informed decisions based on the latest market trends.

    Objectives

    ⦁	 Get a visual on the distribution of commodities in different areas.

    ⦁	Interact with the trends in prices for commodities across different markets.

    ⦁	Study the changes in market prices.

    ⦁	Understand the dynamics of price movements relative to time.  

    """
)

Visual_Report_text = dcc.Markdown(
    """
    For our dataset, the first administrative region has the highest collective representation and supersedes all other regions in terms of geographic distribution of food. 
    The rift valley accounts for the largest share of the market data, with approximately 38% of the total. 
    This suggests that the region is a significant producer of food and has a substantial impact on the subsequent administrative tiers and local markets within the region.
    """
)
Visual_Report_text_b = dcc.Markdown(
    """
    The second administrative tier displays a higher level of refinement in its geographic representation, with smaller regions within the tier. 
    Nairobi takes the lead with a significant representation of approximately 28%, according to our data. 
    A unique perspective could suggest that the Rift Valley region from the first administrative tier has a higher aggregate representation in the second administrative region. 
    Nairobi is followed closely by Turkana, Garissa, and Mombasa with notable data output.
    """
)

Timeseries_text = dcc.Markdown(
    """
> In this section, our main goal is to study the price trends of commodities, focusing on Maize in Kenya.
  Maize is essential in agriculture and widely consumed in households. The study aims to uncover patterns in prices over the past few years and understand if there are predictable changes.
  Given Maize's importance as a staple food, understanding what influences its prices is crucial.

> We're not only looking at one market but exploring different regions, comparing pricing behaviors.
 Through careful time series analysis, our goal is to provide detailed insights into the Maize market, enhancing our understanding of its trends and regional differences.
"""
)
Timeseries2_text = dcc.Markdown(
    """
>  Based on our case study, it appears that Nairobi dominates the market share of commodities for our dataset, followed by Eldoret. 
 The significant proportion of commodities traded in Nairobi suggests that it is an ideal destination for marketing solutions, which can be attributed to its large population and well-developed network infrastructure that connects buyers and sellers.

"""
)

analysis_text = dcc.Markdown(
    """
    Using the visual analysis,it appears that Nairobi is the dominant region for market activity and administration, and maize is the dominant crop with a significant proportion of the market share. 
    Additionally, there is a positive relationship between price changes and time for maize in Nairobi, with some outliers detected in 2017 that may indicate an abnormal increase in price followed by a slump. 
    Further confirmation is needed to fully understand these price fluctuations.

    """
)
analysis2_text = dcc.Markdown(
    """
    From the time series graph, it appears that the prices of maize in the 5 major markets in Kenya have been relatively similar in terms of changes  over the period from 2006 to 2023. 
    However, there are some noticeable differences between the lowest and highest performing markets. 
    Specifically, Nakuru consistently had the lowest prices for a kilo of maize, while prices in Kisumu were significantly higher.

    """
)

forecast_text = dcc.Markdown(
    """
    forecast stuff
    """
)

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only and is not a substitute for professional advice and
        services from qualified financial services providers familiar with your financial
        situation.
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)
Introduction_card = dbc.Card(
    [
        dbc.CardHeader("Report Analysis on Kenyan Food Market"),
        dbc.CardBody(Introduction_text),
    ],
    className="mt-4",
)

Visual_Report_card = dbc.Card(
    [
        dbc.CardHeader("Visual Analysis of the Report"),
        dbc.CardBody(Visual_Report_text),
        dcc.Graph(id="fig1", figure=fig1, className="mb-2"),
        dbc.CardBody(Visual_Report_text_b),
        dcc.Graph(id="fig2", figure=fig2, className="mb-2"),
        dbc.CardBody(Visual_Report_text_b),
        dcc.Graph(id="fig12", figure=fig12, className="mb-2"),
    ],
    className="mt-4",
)
geo_card = dbc.Card(
    [
        dbc.CardHeader("GeoVisual"),
        html.Iframe(width="100%", height="600", srcDoc=mymap._repr_html_()),
    ],
    className="mt-4",
)
timeseries_card = dbc.Card(
    [
        dbc.CardHeader("Analysis"),
        dbc.CardBody(Timeseries_text),
        # dcc.Graph(id="fig14", figure=fig14, className="mb-2"),
        dbc.CardBody(analysis_text),
        dcc.Graph(id="fig15", figure=fig15, className="mb-2"),
        dbc.CardBody(analysis_text),
    ],
    className="mt-4",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(Introduction_card, tab_id="tab-1", label="Overview"),
        dbc.Tab(geo_card, tab_id="tab-2", label="GeoData"),
        dbc.Tab(Visual_Report_card, tab_id="tab-3", label="Visual Analysis"),
        dbc.Tab(
            [timeseries_card,
             dcc.Graph(id="fig", figure=fig, className="mb-2"),
             dbc.CardBody(analysis2_text),
             ],
            tab_id="tab-4",
            label="Timeseries Analysis",
            className="pb-4",
        ),
    ],
    id="tabs",
    active_tab="tab-2",
    className="mt-2",
)

navbar = dbc.NavbarSimple(
    brand='Attain Solutions Ltd',
    brand_style={'fontSize': 40, 'color': 'white'},
    children=html.A('Data Source',
                    href='https://data.humdata.org/dataset/wfp-food-prices-for-kenya?force_layout=desktop',
                    target='_blank',
                    style={'textAlign': 'center', 'color': 'black'}),
    color='primary',
    fluid=True,
    sticky='top'
)

# selecting unique value in markets
marketdropdown = dcc.Dropdown(
    id='market-dropdown',
    options=[{'label': val, 'value': val} for val in df['market'].unique()],
    value=df['market'].unique()[0],
    style={'width': '50%', 'margin-bottom': '20px','color': 'black'},
    multi=False,
)
# selecting unique value in commodities
commoditydropdown = dcc.Dropdown(
    id='commodity-dropdown',
    options=[{'label': val, 'value': val} for val in df['commodity'].unique()],
    value=df['commodity'].unique()[0],
    style={'width': '50%', 'margin-bottom': '20px', 'color': 'black'},
    multi=False,
)
averagepricecard = dbc.Card(
    [
        dbc.CardHeader("Price Statistics"),
        dbc.CardBody([
            html.H4("Market Statistics", className="card-title"),
            commoditydropdown,
            marketdropdown,
            html.P(id="average-price", className="card-text")
        ]),

    ],
    color="primary",
    inverse=True,
    style={'margin-bottom': '20px'},
    className="mt-4",
)
"""=====================================================
Main Layout
======================
"""

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Kenya Food Market Concept App by Attain",
                    className="text-center bg-primary text-white p-2",
                ),
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.CardBody(averagepricecard),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.CardHeader("Market Chart"),
                        # dcc.Graph(id="fig14", figure=fig14, className="mb-2"),
                        dcc.Graph(id='area-chart')
                    ],
                    width=8,
                ),
            ]),     
        dbc.Row(dbc.Col(footer)),
    ],
    fluid=True,
)
# Callbacks ***************************************************************

if __name__ == "__main__":
    app.run_server(debug=True)

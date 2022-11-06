from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
airbnb = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/airbnb_lisbon_1480_2017-07-27.csv')[['overall_satisfaction', 'neighborhood', 'price']]


app = Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css]
)

# HTML structure (and some CSS)
app.layout = html.Div( 
    dbc.Container(
        [   
            dbc.Row(
                dbc.Col(html.Div([
                    html.H1('AirBnB places in Lisbon', style = {'margin-top': '50px', 'margin-bottom': '40px'}),
                    ]
                ), width={"size": 6, "offset": 3})
            ),
            
            dbc.Row([
                dbc.Col(html.Div("Insert the amount of neighborhoods to display:"), width = 4),
                dbc.Col(html.Div(dbc.Input(value = '6', id = 'n-neigh-filter', type="text")), width = 8), 
            ], style = {'margin-left': '7px', 'margin-top': '7px'}),
            dcc.Graph(id = 'price-per-neigh', className="m-4"),
        ])
    )

# Callbacks
@app.callback(
    Output(component_id = 'price-per-neigh', component_property = 'figure'),
    Input(component_id = 'n-neigh-filter', component_property = 'value')
)
def update_price_per_neigh(n_neigh):

    n_neigh = int(n_neigh)
    
    # Filtering dataset
    neigh_list = airbnb.groupby('neighborhood').agg({'overall_satisfaction': 'mean'})\
                        .sort_values('overall_satisfaction', ascending = False)[:n_neigh].index
    airbnb_cut = airbnb[airbnb['neighborhood'].isin(neigh_list)]

    # Building figure
    # ppn_fig = px.box(airbnb_cut, x="neighborhood", y="price")
    ppn_fig = px.histogram(airbnb_cut, x="price")

    return ppn_fig


if __name__ == "__main__":
    app.run_server()
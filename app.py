import logging
import os
import dash
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

from plots import plot_config, get_map_plot, get_country_timeseries,get_bar_plot2
from wrangle import wrangle_data

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
locks = {}

template = 'plotly dark'
default_layout = {
    'autosize': True,
    'xaxis': {'title': None},
    'yaxis': {'title': None},
    'margin': {'l': 20, 'r': 10, 't': 30, 'b': 10},
    'hovermode': 'x',
    'paper_bgcolor': '#303030',
    'plot_bgcolor': '#303030'
}

external_stylesheets = [
    'https://codepen.io/mikesmith1611/pen/QOKgpG.css',
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css',
    dbc.themes.BOOTSTRAP,
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.index_string = open('index.html', 'r').read()

'''
try:
    import kaggle
    print("Downloading ..")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('imdevskp/corona-virus-report', path='./data', unzip=True)
except:
    print('download kaggle auth to ~/.kaggle.json')
'''


covid_df = pd.read_csv('./data/covid_19_clean_complete.csv')
pop_df = pd.read_csv('./data/macro_corona_data.csv')
covid_df = wrangle_data(covid_df, pop_df)
country_options2 = covid_df ["Country"].unique()


def get_graph(class_name, height,**kwargs):
    return html.Div(
        className=class_name,
        children=[
            dcc.Graph(**kwargs, style = {"height":height, "width":"100%"}),           
        ],
    )



head = dbc.Jumbotron(
    [
        html.H1("COVID-19 AFrica", className="display-3"),
        html.P(
            "COVID-19 Tracking "
            "",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "This is a project of DataPivoAfrica"
            "Tracking COVID-19 in Africa Continent."
        ),
        html.P(dbc.Button("Learn more", color="info"), className="lead"),
    ]
    
)

card = [   
        dbc.FormGroup(
            [
            dcc.Dropdown(
                id="Country",
                options=[{
                    'label': i,
                    'value': i
                } for i in country_options2],
                value='Algeria'),
            ]
        )
    ]

card2 = [   
        dbc.FormGroup(
            [
            dcc.Dropdown(
                id="Country2",
                options=[{
                    'label': i,
                    'value': i
                } for i in country_options2],
                value='Algeria'),
            ]
        )
    ]

radio = dbc.FormGroup(
    [
        dbc.Label("CASES"),
        dbc.RadioItems(
            options=[
                {"label": "CONFIRMED", "value": "Confirmed"},
                {"label": "DEAD", "value": "Deaths"},
                {"label": "RECOVERED", "value": "Recovered"},
                {"label": "ACTIVE", "value": "Active"},
            ],
            value='Confirmed',
            id="count_category",
            inline=True
        ),
    ]
)


app.layout = dbc.Container([
    head,
    dbc.Col(radio,md=12),
    dbc.Row([  
         dbc.Col(
            get_graph(
            class_name="row",
            height=600,            
            figure=get_map_plot(covid_df),
            id='map_graph',
            config=plot_config,
        ),
       md=12),      
    ]),
    html.Hr(),
     dbc.Row([  
        dbc.Col(html.P(""), md=2),        
        dbc.Col([html.H2("Cases Per Country")],md=8)
        ],align="center"),
    html.Hr(),
    dbc.Row(
            [
            dbc.Col(card, md=2),
            dbc.Col(get_graph(
            class_name="row", 
            height=400,            
            figure=get_bar_plot2(covid_df),
            id='funnel-graph',
            config=plot_config,
        ),                
                md=10),
            ],
            align="center",
        ),  
        html.Hr(),
        dbc.Row([  
        dbc.Col(html.P(""), md=2),        
        dbc.Col([html.H2("Countries Trends")],md=8)
        ],align="center"),
        html.Hr(),
        dbc.Row([  
        dbc.Col(card2, md=2),        
         dbc.Col(
         get_graph(
            class_name="row",  
            height=400,           
            figure=get_country_timeseries(covid_df,count_col="Algeria"),
            id='total_graph',
            config=plot_config,
        ),
       md=10),      
    ]),  
    html.Hr(),
], 
fluid = True
#style={'backgroundColor':'#303030'}

)

@app.callback(
    Output('map_graph', 'figure'),
    [
        #Input('count_type', 'value'),
        Input('count_category', 'value')
    ])
def update_map_plot(count_category):
    count_col = count_category 
    return get_map_plot(covid_df, count_col)

@app.callback(
    Output('funnel-graph', 'figure'),
    [
        Input('Country', 'value'),        
    ])
def update_bar_plot(Country):
    count_col = Country
    return get_bar_plot2(covid_df, count_col)

@app.callback(
    Output('total_graph', 'figure'),
    [
        Input('Country2', 'value'),        
    ])
def update_x_timeseries(c):   
    return get_country_timeseries(covid_df,count_col=c)

if __name__ == '__main__':
    app.run_server(debug=True,port=8000)
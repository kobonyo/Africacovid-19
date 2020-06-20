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

from wrangle import wrangle_data
from plots import plot_config, get_map_plot, get_country_timeseries,get_bar_plot2,get_country_timeseries_new,total_timeseries

covid_df = pd.read_csv('./data/covid_19_clean_complete.csv')
pop_df = pd.read_csv('./data/macro_corona_data.csv')
covid_df = wrangle_data(covid_df, pop_df)
full_grouped_df = pd.read_csv('./data/full_grouped.csv')
full_grouped_df = full_grouped_df[full_grouped_df['WHO Region'] == "Africa"]
country_options2 = covid_df ["Country"].unique()
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


def get_graph(class_name, height,**kwargs):
    return html.Div(
        className=class_name,
        children=[
            dcc.Graph(**kwargs, style = {"height":height, "width":"100%","margin":"2px"})
            #html.I(className='fa fa-expand'),       
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
        html.P("This is a project of DataPivotAfrica"
            "It is aimed at tracking COVID-19 in Africa."
        ),
        html.P(dbc.Button("Learn more", color="info"), className="lead"),
    ]
    
)

card = [   
        dbc.FormGroup(
            [
            dbc.Label("Select Country", html_for="Country", color="white"),
            dcc.Dropdown(
                id="Country",                
                #className = ".bg-dark",
                options=[{
                    'label': i,
                    'value': i
                } for i in country_options2],
                value='Algeria')
            ]
        #,style={'backgroundColor':'#303030'}
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

card3 = [   
        dbc.FormGroup(
            [
            dcc.Dropdown(
                id="Country3",
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

nav = dbc.Nav(
    [
        dbc.NavLink("Cases", active=True, href="#"),
        dbc.NavLink("Per Country", href="#"),
        dbc.NavLink("New Cases", href="#new_cases"),
        dbc.NavLink("Disabled", href="#"),
    ]
)

def card_content(b,t):
    return[dbc.CardBody([
            html.H4(t, className="card-title"),
            html.H1(b, className="card-text"),
        ]
    ),
    ]

def total_cases(df):  
    df = covid_df[covid_df['Confirmed'] > 0] \
    .groupby(['Date']).sum() \
    .reset_index() \
    .melt(id_vars='Date',
            value_vars=[
                'Confirmed',
                'Recovered',
                'Active',
                'Deaths'
            ]).sort_values('Date') 
    print(df)
    return 0


c,a,d,r = 0,0,0,0

#total_cases(full_grouped_df)

cards = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(c,"Confirmed"),color="info"),md=3),
                dbc.Col(dbc.Card(card_content(r,"Recovered"), color="success"),md=3),
                dbc.Col(dbc.Card(card_content(d,"Daths"), color="danger", inverse=True),md=3),
                dbc.Col(dbc.Card(card_content(a,"Active"), color="warning", inverse=True),md=3)                
                
            ]
                      
        ),
 
    ]
)

line = html.Hr()

map_graph = dbc.Col(get_graph(
            class_name="row",
            height=300,            
            figure=get_map_plot(covid_df),
            id='map_graph',
            config=plot_config,
        ), md = 6
)

cases_per_country =  dbc.Row([  
        dbc.Col([html.H2("Cases Per Country")],md=12)
        ],align="center")

bar_plots = dbc.Col(get_graph(
            class_name="row", 
            height=300,            
            figure=get_bar_plot2(covid_df),
            id='funnel-graph',
            config=plot_config,
        ), md = 6
)

country_time_series = dbc.Col(get_graph(
            class_name="row",  
            height=300,           
            figure=get_country_timeseries(covid_df,count_col="Algeria"),
            id='total_graph',
            config=plot_config,
        ), md = 6
)

new_cases_daily = dbc.Col(
         get_graph(
            class_name = "row",  
            height = 300,           
            figure = get_country_timeseries_new(full_grouped_df,count_col="Algeria"),
            id = 'new_cases',
            config = plot_config,
        ), md = 6     
    )


new_cases_daily2 = dbc.Col(
         get_graph(
            class_name = "row",  
            height = 300,           
            figure = get_country_timeseries_new(full_grouped_df,count_col="Algeria"),
            id = 'new_cases2',
            config = plot_config,
        ), md = 6     
    )

total_africa = dbc.Col(
         get_graph(
            class_name = "row",  
            height = 300,           
            figure = total_timeseries(covid_df),
            id = 'general',
            config = plot_config,
        ), md = 6     
    )

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
locks = {}
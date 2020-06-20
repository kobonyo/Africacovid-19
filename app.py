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
from  layout import *


app = dash.Dash(__name__,external_stylesheets=external_stylesheets, suppress_callback_exceptions = True)
server = app.server

app.index_string = open('index.html', 'r').read()


app.layout = dbc.Container([line,
                           #cards,
                           #line,
                           #dbc.Row([dbc.Col(card, md=8)]),
                           dbc.Row(dbc.Col(html.Div(card))),
                           dbc.Row([bar_plots,country_time_series]),                           
                           dbc.Row([new_cases_daily,total_africa]),
                           line
                           ],
                           fluid = True,
                           style={'backgroundColor':'#303030'}

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
        Input('Country', 'value'),        
    ])
def update_x_timeseries(c):   
    return get_country_timeseries(covid_df,count_col=c)

@app.callback(
    Output('new_cases', 'figure'),
    [
        Input('Country', 'value'),        
    ])
def update_x_timeseries_new(c):   
    return get_country_timeseries_new(full_grouped_df,count_col=c)



if __name__ != "__main__":
    app.config.update({
        'routes_pathname_prefix': '/',
        'requests_pathname_prefix': '/dev/'
    })
    app.css.config.serve_locally = False
    app.scripts.config.serve_locally = False

if __name__ == '__main__':
    app.run_server(debug=True,port=5000,host='0.0.0.0')
    
'''

if __name__ == '__main__':
    app.run_server(debug=True,port=5000,host='127.0.0.1')

'''
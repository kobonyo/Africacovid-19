import os

import numpy as np
import plotly.graph_objects as go
from plotly import express as px

plot_config = {
    'modeBarButtonsToRemove': [
        'lasso2d',
        'hoverClosestCartesian',
        'hoverCompareCartesian',
        'toImage',
        'sendDataToCloud',
        'hoverClosestGl2d',
        'hoverClosestPie',
        'toggleHover',
        'resetViews',
        'toggleSpikelines',
        'resetViewMapbox'
    ]
}

plot_palette = [
    '#185d6a',
    '#385e4c',
    '#597043',
    '#7a8339',
    '#9b9530',
    '#bca727',
    '#ddb91e',
    '#ffcc14',
]

mapbox_token = "pk.eyJ1Ijoia29ib255byIsImEiOiJja2I3N2ZzYjgwMzBlMnFxbHphZWNuengwIn0.bN8XMm_vZokAV9E8HF-jCQ"
mapbox_cofig = dict(
    accesstoken='pk.eyJ1Ijoia29ib255byIsImEiOiJja2I3N2ZzYjgwMzBlMnFxbHphZWNuengwIn0.bN8XMm_vZokAV9E8HF-jCQ',
    style='mapbox://styles/nite/ck7z7pu6p1utj1jlkfgpwvo3q', )

bggolor = '#24252A'
default_layout = {
    'margin': {'r': 10, 't': 20, 'l': 10, 'b': 50},

}

def get_default_color(count_col='Confirmed'):
    if count_col == 'Confirmed':
        return '#6195d2'
    if count_col == 'Active':
        return '#2B34B9'
    if count_col == 'Recovered':
        return '#BC472A'
    return '#BC472A'
        


def get_map_plot(covid_df, count_col='Confirmed'):
    df = covid_df[covid_df[count_col] > 0]
    values = df['logCumConf' if count_col == 'Confirmed' else count_col]
    fig = px.scatter_geo(df,lat='Latitude', lon='Longitude', hover_name='Description',
                        size='logCumConf', projection='natural earth',scope='africa', 
                        animation_frame=df['Date'].astype(str),template='plotly_dark',
                        #height=400,                       
                        color_discrete_sequence=[get_default_color(count_col)]
                        )                           
    #fig.update_geos(fitbounds='locations')
    #pdate_layout(height=300, margin={"r":0,"t":25,"l":0,"b":0}), output_type='div', show_link=False)
    if mapbox_token:
        fig.update_layout(mapbox=mapbox_cofig)
    return fig

def get_country_timeseries(covid_df, count_col='Algeria'):
    df = covid_df[covid_df['Country'] == count_col]    
    trace1 = go.Scatter(x = df['Date'],  y = df.Confirmed.values, name='Confirmed',mode='lines+markers')
    trace2 = go.Scatter(x = df['Date'],  y = df.Deaths.values,     name='Dead',mode='lines+markers')
    trace3 = go.Scatter(x =df['Date'],  y = df.Recovered.values, name='Recovered',mode='lines+markers')
    trace4 = go.Scatter(x = df['Date'], y = df.Active.values,   name='Active',mode='lines+markers')

    fig = go.Figure(data=[trace1,trace2,trace3,trace4])
    fig.update_layout( 
        template="plotly_dark",       
        **default_layout
    )
    return fig

def get_bar_plot2(covid_df,Country='Kenya'):
    count_col = ['Confirmed', 'Deaths', 'Recovered', 'Active']
    last_df = covid_df[covid_df['Date'] == covid_df['Date'].max()]
    last_df = last_df[last_df['Country'] == Country]
    df = last_df.groupby(['Country',]).sum().reset_index()
    trace1 = go.Bar(x = ['Confirmed'],  y = df.Confirmed.values, name='Confirmed')
    trace2 = go.Bar(x = ['Dead'],       y = df.Deaths.values,     name='Dead')
    trace3 = go.Bar(x = ['Recovered'],  y = df.Recovered.values, name='Recovered')
    trace4 = go.Bar(x = ['Active'],     y = df.Active.values,   name='Active')

    fig = go.Figure(data=[trace1,trace2,trace3,trace4])
    fig.update_layout(
        selectdirection='v',
        template="ggplot2",   
        **default_layout
    )
    return fig

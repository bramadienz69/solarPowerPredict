import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from datetime import datetime, date, time
from sklearn import linear_model
import sqlalchemy
from dash import dash_table as dt
import time

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

html.Div([
    dcc.Interval(id = 'solar_wind_card',
                 interval = 30000,
                 n_intervals = 0),
]),


def wind_fourth_card_value(n_intervals):
    header_list = ['Date Time', 'Voltage', 'Current']
    df = pd.read_csv('sensors_data.csv', names = header_list)
    df['Power (W)'] = df['Voltage'] * df['Current']
    df['Power (KW)'] = df['Power (W)'] / 1000
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    df['Date'] = df['Date Time'].dt.date
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    unique_month = df['Month'].unique()
    energy_watts = (df[df['Month'] == unique_month[-1]]['Power (W)'].sum()) / 24
    energy_kilo_watts = (df[df['Month'] == unique_month[-1]]['Power (KW)'].sum()) / 24

    return [
        html.P('This Month Wind Energy', className = 'card_text'),
        html.Div([
            html.P('{0:,.5f}'.format(energy_kilo_watts) + ' ' + 'KWh',
                   className = 'card_value1'),
            html.P('{0:,.5f}'.format(energy_watts) + ' ' + 'Wh',
                   className = 'card_value2')
        ], className = 'card_values_gap')
    ]

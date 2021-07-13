import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from logging import disable
import re
import dash
import dash_core_components as dcc
from dash_html_components.Label import Label
from numpy.lib.npyio import recfromtxt
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_html_components.Div import Div
from dash_html_components.Span import Span
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import wfdb
import os
from dash.exceptions import PreventUpdate
from scipy import sparse
import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.signal import find_peaks
import plotly.graph_objs as go

import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__,prevent_initial_callbacks=True)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

record = wfdb.rdrecord('269', channels=[1]) 
signals, fields = wfdb.rdsamp('269', channels=[1])
signal=signals.reshape(record.sig_len)



app.layout = html.Div(children=[
    html.Header(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Img(src="static/svg/logo-hrv-nuevo.svg",width='160px'),
                    html.Div(children=[
                        html.Div(children=[
                            html.Div('Record name: ',className='title'),
                            html.Div(id='record_name', className='ml-2')], className='item'),
                        html.Div(children=[
                            html.Div('Lenght signal: ',className='title'),
                            html.Div(id='lenght_name', className='ml-2')], className='item'),
                        html.Div(children=[
                            html.Div('FS: ',className='title'),
                            html.Div(id='fs_name', className='ml-2')], className='item')], className='box')],className='container_m'),
                html.Div(children=[
                        dbc.Button('Show Metadata',color="success",className="btn-sm disabled mr-2 btn-hrv",id="show_metadata"),
                        dbc.Button('Download as csv',color="success",className="btn-sm disabled mr-4 btn-hrv",id="download_csv")],className='container-btn')
                ],className='container-ge'),
            ]),

    dcc.Store(id='signal'),
                
    html.Div(children=[
            dcc.Upload(id='upload-data', accept='.dat', children=[
                dbc.Button(html.I(className='bi bi-folder2-open m-2'), color="succes", className="mb-1 btn-outline-success")
                ]),
                dbc.Button("1", color="succes", className="mb-1 btn-outline-success"),
                dbc.Button("1", color="succes", className="mb-1 btn-outline-success"),
                dbc.Button("1", color="succes", className="mb-1 btn-outline-success"),
                dbc.Button("1", color="succes", active=True, className="mb-1 btn-outline-success")],className='vertical_checks'),    
    html.Div([
        dcc.Graph(
        id='clientside-graph'
    ),
    dcc.Store(
        id='clientside-figure-store',
        data=[{
            'x': None,
            'y': None,
        }]
    )],className='central-graph p-3'),
    html.Div(children='Dash: A web application framework for Python.',id='hola',className='features'),
])

@app.callback(
    Output('clientside-figure-store', 'data'),
    Input('hola', 'children')
)
def update_store_data(value):
    return [{
        'x': list(range(int(len(signal))+1)),
        'y': list(signal[:int(len(signal))]),
        'mode': 'line'
    }]



app.clientside_callback(
    """
    function(data, scale) {
        return {
            'data': data,
            'layout': {
                 'yaxis': {'type': scale}
             }
        }
    }
    """,
    Output('clientside-graph', 'figure'),
    Input('clientside-figure-store', 'data')
    )


if __name__ == '__main__':
    app.run_server(debug=True)

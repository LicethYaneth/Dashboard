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
                dbc.Button(html.Img(src="static/svg/open_filled.svg"), color="succes", className="mb-1 btn-success btn-gn text-center")
                ]),
                dbc.Button(html.Img(src="static/svg/ng_filled.svg"), color="succes", className="mb-1 btn-success btn-gn text-center"),
                dbc.Button(html.Img(src="static/svg/bl_filled.svg"), color="succes", className="mb-1 btn-success btn-gn text-center"),
                dbc.Button(html.Img(src="static/svg/pk_filled.svg"), color="succes", className="mb-1 btn-success btn-gn text-center")
                ],className="vertical_checks"),    
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
    html.Div(id='hola',children=[
        html.Div(children=[
            html.Div("Time Domain Features", className="text-center title-inputs"),
            html.Div(children=[
            html.Div(children=[
                html.H6("SDDN", className="text-left"),
                html.Div(id="sddn", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("NN20 Count", className="text-left"),
                html.Div(id="nn20", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),
            
            html.Div(children=[
            html.Div(children=[
                html.H6("SDSD:", className="text-left"),
                html.Div(id="sdsd", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("NN50 Count", className="text-left"),
                html.Div(id="nn50", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div(children=[
            html.Div(children=[
                html.H6("SDANN", className="text-left"),
                html.Div(id="sdann", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("PNN50 Count", className="text-left"),
                html.Div(id="pnn50", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div(children=[
            html.Div(children=[
                html.H6("RMSSD", className="text-left"),
                html.Div(id="rmssd", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("PNN20 Count", className="text-left"),
                html.Div(id="pnn20", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div("Frecuency Domain Features", className="text-center title-inputs"),

            html.Div(children=[
            html.Div(children=[
                html.H6("LF", className="text-left"),
                html.Div(id="lf", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("LF Norm", className="text-left"),
                html.Div(id="lfnorm", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div(children=[
            html.Div(children=[
                html.H6("HF", className="text-left"),
                html.Div(id="hf", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("HF Norm", className="text-left"),
                html.Div(id="hfnorm", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div(children=[
            html.Div(children=[
                html.H6("VLF", className="text-left"),
                html.Div(id="vlf", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("Total Power", className="text-left"),
                html.Div(id="totalpower", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div("Geometrical Domain Features", className="text-center title-inputs"),

            html.Div(children=[
            html.Div(children=[
                html.H6("Triangular Index", className="text-left"),
                html.Div(id="tindex", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("TINN", className="text-left"),
                html.Div(id="tinn", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-row flex-nowrap justify-content-between"),

            html.Div("Graphical metrics", className="text-center title-inputs"),

            html.Div(children=[
            html.Div(children=[
                html.H6("metrica1", className="text-left"),
                html.Div(id="metrica1", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("metrica2", className="text-left"),
                html.Div(id="metrica2", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            html.Div(children=[
                html.H6("metrica3", className="text-left"),
                html.Div(id="metrica3", className="input-data"),
            ],className="d-flex flex-column flex-nowrap input-father"),
            ],className="d-flex flex-column flex-nowrap justify-content-between"),

        ],className="d-flex flex-column flex-nowrap justify-content-start overflow-visible")
    ],className='features'),
])


@app.callback(
    Output('clientside-figure-store', 'data'),
    Input('hola', 'children')
)
def update_store_data(value):
    return [{
        'x': list(range(int(len(signal[:2000]))+1)),
        'y': list(signal[:int(len(signal[:2000]))]),
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

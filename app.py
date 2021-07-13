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




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css']

UPLOAD_DIRECTORY = "/project/app_uploaded_files"

app = dash.Dash(__name__,prevent_initial_callbacks=True)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



colors = {
    'background': '#ffffff',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 14, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


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
    html.Div(
        dcc.Graph(
            id='central-graph',
        ),className='central-graph p-3'),
    html.Div(children='Dash: A web application framework for Python.',className='features'),
])

def baseline_als(y, lam, p, niter=10):
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    D = lam * D.dot(D.transpose()) # Precompute this term since it does not depend on `w`
    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)
    for i in range(niter):
        W.setdiag(w) # Do not create a new matrix, just update diagonal values
        Z = W + D
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z


def apply_baseline(signal,record):
    signal_bas=baseline_als(signal[:int(len(signal)/2)],100,0.001)
    signal_bas_2=baseline_als(signal[int(len(signal)/2):int(len(signal))],100,0.001)
    sub_1=np.subtract(signal[:int(len(signal)/2)],signal_bas)
    sub_2=np.subtract(signal[int(len(signal)/2):int(len(signal))],signal_bas_2)
    signal_com=np.concatenate((sub_1,sub_2),None)

    signal_prep=pd.DataFrame(signal_com)
    signal_prep_w=signal_prep.rolling(10).mean() 
    x=signal_prep_w.values.reshape(record.sig_len)
    peaks_1, _ = find_peaks(x, height=(0.7))
    meanp=np.mean(signal_prep_w.values[peaks_1])
    desv=np.std(signal_prep_w.values[peaks_1])

    return x


def load_dat(filename_o):
    record = wfdb.rdrecord(filename_o[:-4], channels=[1]) 
    signals, fields = wfdb.rdsamp(filename_o[:-4], channels=[1])
    signal=signals.reshape(record.sig_len)
    return record.__dict__['record_name'], record.sig_len, record.fs, signal


@app.callback(Output('record_name', 'children'),
              Output('lenght_name', 'children'),
              Output('fs_name', 'children'),
              Output('signal','data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output_p(contents,filename_o, list_of_dates):
    if contents is None:
        raise PreventUpdate
    else:
        return load_dat(filename_o)

@app.callback(Output('central-graph','figure'),Input('signal','data'))
def central_plot(data):
    if data is None:
        raise PreventUpdate
    else:
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3,4,5,6,7,8,9,10], y=data[:9])])
        return fig




if __name__ == '__main__':
    app.run_server(debug=True)
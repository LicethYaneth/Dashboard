from logging import disable
import dash
import dash_core_components as dcc
from dash_html_components.Label import Label
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_html_components.Div import Div
from dash_html_components.Span import Span
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['http://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css']

app = dash.Dash(__name__)
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

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Header(
        children=[
            html.Div(children=[
                html.Div(children=[
                    html.Img(src="static/svg/logo-hrv-nuevo.svg",width='160px'),
                    html.Div(children=[
                        html.Div(children=[
                            html.Div('Record name: ',className='title'),
                            html.Div(id='record_name')], className='item'),
                        html.Div(children=[
                            html.Div('Lenght signal: ',className='title'),
                            html.Div(id='lenght_name')], className='item'),
                        html.Div(children=[
                            html.Div('fs: ',className='title'),
                            html.Div(id='fs_name')], className='item')], className='box')],className='container_m'),
                    dbc.Button('Download as csv',color="success",className="btn-sm disabled",id="download_csv")],className='container'),
            ],
        style={ 
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(children=[
    html.Div(children=[
            dbc.Button(html.Img(src='static/svg/folder-open.svg',width=15,alt='open'), color="succes", className="mb-1 btn-outline-success"),
            dbc.Button("1", color="succes", className="mb-1 btn-outline-success"),
            dbc.Button("1", color="succes", className="mb-1 btn-outline-success"),
            dbc.Button("1", color="succes", className="mb-1 btn-outline-success"),
            dbc.Button("1", color="succes", active=True, className="mb-1 btn-outline-success")],className='vertical_checks'),
    html.Div(
        dcc.Graph(
            id='example-graph-2',
            figure=fig,
        )),
    html.Div(children='Dash: A web application framework for Python.',className='features', style={
        'textAlign': 'right',
        'width':'250px',
        'margin':'10px',
        'justifySelf': 'end',
        'color': colors['text']
    })], className='total_graph'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
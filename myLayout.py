
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
from sqlalchemy import create_engine

import myFunction
from myFunction import salariesDF, tipsDF, productDF

app = dash.Dash()
app.title = 'Latihan Ujian'

app.layout = html.Div(
    children=[
        dcc.Tabs(id='tabs', value='tab-4', 
            children=[
                dcc.Tab(label='GoBar vs Histogram', value='tab-1', children=[
                    html.Div([
                        html.Table(
                            [
                                html.Tr([
                                    html.Td([html.P('Jobs: ')]),
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-tab1-jobs',
                                            options=[
                                                {'label': 'NURSE', 'value': 'NURSE'},
                                                {'label': 'POLICE', 'value': 'POLICE'},
                                                {'label': 'FIRE', 'value': 'FIRE'}
                                            ],
                                            value='NURSE'
                                        ),
                                    ]),
                                ]),
                                html.Tr([
                                    html.Td([html.P('Year: ')]),
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-year-tab1',
                                            options= myFunction.yearOption,
                                            multi=True
                                        ),
                                    ]),
                                ]),

                            ], 
                            style = {'width' : '800px', 'margin': '0 auto'}
                        ),
                        html.Table(
                            [
                                html.Tr([
                                    html.Td([html.P('Job Title: ')]),
                                ]),
                                html.Tr([
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-jobtitle-tab1',
                                            options=[],
                                            multi=True
                                        ),
                                    ]),
                                ])
                            ], 
                            style = {'width' : '800px', 'margin': '0 auto'}
                        ),
                        html.Div(
                            children=[], id='div-graph-tab1'),
                    ])
                ]),
                dcc.Tab(label='Tips Data Set', value='tab-2', children=[
                    html.Div([
                        html.P('Range Total Bill: '),
                        dcc.RangeSlider(
                            min=min(tipsDF['total_bill']),
                            max=max(tipsDF['total_bill']),
                            value=[min(tipsDF['total_bill']), max(tipsDF['total_bill'])],
                            step=1,
                            id='slider-range-totalbill-tab2'
                        ),
                        html.Div(children=[], 
                        id='div-tabletip-tab2')
                    ])
                ]),
                dcc.Tab(label='Scatter Plot', value='tab-3', children=[
                    html.Div([
                        html.Table(
                            [
                                html.Tr([
                                    html.Td([html.P('Hue: ')]),
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-hue-tab3',
                                            options=[
                                                {'label': '-- Choose --', 'value': ''},
                                                {'label': 'Tip', 'value': 'tip'},
                                                {'label': 'Sex', 'value': 'sex'},
                                                {'label': 'Smoker', 'value': 'smoker'},
                                                {'label': 'Day', 'value': 'day'},
                                                {'label': 'Time', 'value': 'time'}
                                            ],
                                            value=''
                                        ),
                                    ]),
                                ]),
                            ], 
                            style = {'width' : '800px', 'margin': '0 auto'}
                        ),
                        dcc.Graph(
                            id='scatterPlot',
                            figure={
                                'data': [
                                    go.Scatter(
                                    x = tipsDF['total_bill'],
                                    y = tipsDF['tip'],
                                    mode='markers',
                                    marker=dict(size=5, line={'width':0.5, 'color': 'white'})
                                    )
                                ],
                                'layout' : go.Layout(
                                    xaxis = {'title' : 'Total Bill'},
                                    yaxis = {'title' : 'Tip'},
                                    margin = {'l': 40, 'b': 40, 't':40, 'r':10},
                                    hovermode = 'closest'
                                )
                            }
                        ),
                    ])
                ]),
                dcc.Tab(label='Product Data Table', value='tab-4', children=[
                    html.Div([
                        dcc.Graph(
                            id='tbl-product-tab4',
                            figure = { 
                                'data': [
                                    go.Table(
                                        header=dict(values=list(productDF.columns),
                                            fill = dict(color='#C2D4FF'),
                                            align = ['center'] * 5
                                        ),  
                                        cells=dict(values=[productDF[col] for col in productDF.columns], align=['left'])
                                    )
                                ],
                                'layout' : go.Layout(
                                    height=600, margin={'t': 10}, width=900
                                )
                            }
                        ),
                    ])
                ]),
                dcc.Tab(label='Product Histogram', value='tab-5', children=[
                    html.Div([
                        html.Table(
                            [
                                html.Tr([
                                    html.Td([html.P('Columns: ')]),
                                    html.Td([
                                        dcc.Dropdown(
                                            id='ddl-columns-tab5',
                                            options=[
                                                {'label': 'Price', 'value': 'price'},
                                                {'label': 'Total Stock', 'value': 'totalStock'},
                                                {'label': 'Stock Sekarang', 'value': 'stockSekarang'},
                                                {'label': 'Stock Terjual', 'value': 'stockTerjual'},
                                                {'label': 'Total Income', 'value': 'totalIncome'},
                                            ],
                                            value='price'
                                        ),
                                    ]),
                                ]),
                            ], 
                            style = {'width' : '400px'}
                        ),
                    ]),
                    html.Br(),
                    html.Div(children = 
                        [], id = 'div-histogram-product-tab5')
                ])
            ],
            style = { # untuk tab
                'fontFamily' : 'system-ui'
            },
            content_style = { # untuk conten yg dibungkus tab
                'fontFamily' : 'Calibri',
                'borderLeft' : '1px solid #d6d6d6',
                'borderRight' : '1px solid #d6d6d6',
                'borderBottom' : '1px solid #d6d6d6',
                'padding' : '40px'
            },
        ),
    ],
    style = {
            'maxWidth' : '1000px',
            'margin' : '0 auto'
        }
)
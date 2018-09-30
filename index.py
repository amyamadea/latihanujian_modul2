
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

import myLayout
from myLayout import app

@app.callback(
    Output('ddl-jobtitle-tab1', 'options'), 
    [Input('ddl-tab1-jobs', 'value')]
)
def set_jobtitle_option_tab1(jobs):
    return myFunction.set_jobtitle_option(jobs)

@app.callback(
    Output('div-graph-tab1', 'children'), 
    [Input('ddl-jobtitle-tab1', 'value'), Input('ddl-year-tab1', 'value')]
)
def update_div_gobar_tab1(jobtitle, year):
    axisy = ['BasePay', 'TotalOtherPay']
    goBar = []
    goHistogram = []

    if (jobtitle!=None):
        for i in range (len(axisy)):
            x, y = [],[]
            for iJob in range (len(jobtitle)):
                y.append(salariesDF[salariesDF['JobTitle']==jobtitle[iJob]][axisy[i]].sum())
            
                goHistogram.append(
                    go.Histogram(
                        x= salariesDF[salariesDF['JobTitle']==jobtitle[iJob]][axisy[i]],
                        # marker={'color':'#28a999'},
                        name=jobtitle[iJob] + ' ' + axisy[i]
                    )
                )
            
            goBar.append(
                go.Bar (
                    x = jobtitle,
                    y = y,
                    # text = y,
                    opacity=0.7,
                    name= axisy[i],
                    # marker={'color': color[i]}
                )
            ),
   
    return [
        html.H1('GoBar'),
        dcc.Graph(
            id='gobar-tab1',
            figure = { # kanvas
                'data': goBar,
                'layout' : go.Layout(
                    xaxis = {'title' : ''},
                    yaxis = {'title' : 'US $'},
                    margin = {'l': 40, 'b': 40, 't':40, 'r':10},
                    hovermode = 'closest',
                    # legend={'x':0, 'y':1} # menentukan lokasi legend,
                )
            }
        ),
        html.H1('Histogram'),
        dcc.Graph(
            id='histogram-tab1',
            figure={
                    'data': goHistogram,
                    'layout' : go.Layout(
                        margin = {'l': 40, 'b': 40, 't':40, 'r':10},
                        legend={'x':0, 'y':1},
                        bargap=0.2
                )
            }
        )
    ]

@app.callback(
    Output('div-tabletip-tab2', 'children'), 
    [Input('slider-range-totalbill-tab2', 'value')]
)
def update_div_tabletip_tab2(range_totalbill):
    filterTipsDF = tipsDF[(tipsDF['total_bill']>=range_totalbill[0]) & (tipsDF['total_bill']<=range_totalbill[1])]
    filterTipsDF.sort_values(by=['total_bill'], inplace=True)
    return [
        html.P('Min Total Bill: ' + str(range_totalbill[0]) + ' - Max Total Bill: ' + str(range_totalbill[1])),
        html.H4('Total row: ' + str(len(filterTipsDF))),
        dcc.Graph(
            id='gobar-tab1',
            figure = { # kanvas
                'data': [
                    go.Table(
                        header=dict(values=list(filterTipsDF.columns),
                            fill = dict(color='#C2D4FF'),
                            align = ['center'] * 5
                        ),  
                        cells=dict(values=[filterTipsDF[col] for col in filterTipsDF.columns], align=['left'])
                    )
                ],
                'layout' : go.Layout(
                    height=600, margin={'t': 10}
                )
            }
        )
    ]

@app.callback(
    Output('div-histogram-product-tab5', 'children'), 
    [Input('ddl-columns-tab5', 'value')]
)

def update_div_histogram_product_tab5(column):
    std = np.std(productDF['price'])
    min = productDF['price'].mean()-std
    max = productDF['price'].mean()+std

    return [
        dcc.Graph(
            id='histogram-product-tab5',
            figure={
                    'data': [
                        go.Histogram(
                            x=productDF[(productDF[column]<min) | (productDF[column]>max)][column],
                            marker=dict(
                                color="green"
                            ),
                            name="Tidak Normal",
                            opacity=0.7,
                        ),
                        go.Histogram(
                            x=productDF[(productDF[column]>=min) & (productDF[column]<=max)][column],
                            marker=dict(
                                color="blue"
                            ),
                            name="Normal",
                            opacity=0.7,
                        )
                    ],
                    'layout' : go.Layout(
                        margin = {'l': 40, 'b': 40, 't':40, 'r':10},
                        legend={'x':0, 'y':1},
                        bargap=0.2,
                        xaxis={'title': 'Price Range'},
                        yaxis={'title': 'Count'},
                        title='Product Price'   
                )
            }
        )
    ]
    

if __name__ == '__main__': # menandakan file yg di run adalah main file. tidak diimport
    # debug = True for auto restart if ode edited
    app.run_server(debug=True, port = 2828)
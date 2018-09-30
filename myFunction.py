
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
from sqlalchemy import create_engine

def set_jobtitle_option(jobs='NURSE'):
    jobtitle = salariesDF[salariesDF['JobTitle'].str.contains(jobs)]['JobTitle']
    return [{'label': jobtitle, 'value': jobtitle} for jobtitle, i in zip (jobtitle.unique(), range(jobtitle.nunique()))]

def getDataframe(query):
    query = conn.execute(query).fetchall()
    dataframe = pd.DataFrame(query)
    dataframe.columns = query[0].keys()
    dataframe.set_index('id', inplace=True)

    return dataframe

salariesDF = pd.read_csv('Salaries.csv')
salariesDF.fillna(0, inplace=True)
salariesDF['TotalOtherPay'] = salariesDF['OvertimePay'] + salariesDF['OtherPay'] + salariesDF['Benefits']
tipsDF = sns.load_dataset('tips')
yearOption = [{'label': year, 'value': year} for year, i in zip (salariesDF['Year'].unique(), range(salariesDF['Year'].nunique()))]

# connect db
engine = create_engine("mysql+mysqlconnector://root:@localhost/ujian?host=localhost?port=3306")
conn = engine.connect()
productDF = getDataframe("SELECT P.*, C.nama category, V.nama vendor FROM product P JOIN category C ON P.categoryid = C.id JOIN vendor V ON P.vendorid = V.id LIMIT 20")


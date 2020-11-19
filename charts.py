import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# from plotly.subplots import make_subplots
from urllib.request import urlopen
import json


layout = go.Layout(
    # paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    spikedistance =  -1,
    xaxis = dict(showspikes=True,
        spikedash = 'solid',
        spikemode  = 'across',
        spikesnap = 'cursor'),
    yaxis = dict(rangemode = 'tozero',
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=0.01),
    legend=dict(yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01),
    hovermode='x',
    font=dict(family='Arial'),
    title = dict(x=0.5)
)

PASTELS = px.colors.qualitative.Pastel
DARK2 = px.colors.qualitative.Dark2
PASTEL2 = px.colors.qualitative.Pastel2
G10 = px.colors.qualitative.G10
ANTIQUE = px.colors.qualitative.Antique
ANTIQUE_ALT = [ANTIQUE[2],ANTIQUE[1],ANTIQUE[6],ANTIQUE[0],ANTIQUE[5]]

LIGHT24 = px.colors.qualitative.Light24

AGES_LIST = ['0-18','19-30','31-40','41-50','51-60','61-70','71-80','81+']

def load_data():
    dccovid = pd.read_csv(r'data.csv')
    dccovid.index = pd.to_datetime(dccovid['Date'])
    dccovid['Unknown Ward Tests'] = pd.to_numeric(dccovid['Unknown Ward Tests'])
    hood_demos = pd.read_csv(r'nhood_demographics.csv',index_col='Neighborhood Name')
    ward_demos = pd.read_csv(r'ward_demographics.csv', index_col='Ward')
    with urlopen('https://opendata.arcgis.com/datasets/de63a68eb7674548ae0ac01867123f7e_13.geojson') as response:
        hood_map = json.load(response)
    return dccovid, hood_demos, ward_demos, hood_map

# Load data into the dataframe.
data, hood_demos, ward_demos, hood_map = load_data()

# Cases
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=data['Positives'].diff(),name='New Cases',marker_color='rgb(158,202,225)'))
fig.add_trace(go.Line(x=data['Date'], y=data['Positives'].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
fig.update_layout(title=dict(text='New Cases'))
fig.write_html("./chart_htmls/cases.html")

# Deaths
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=data['Deaths'].diff(),name='New Deaths',marker_color='maroon'))
fig.add_trace(go.Line(x=data['Date'], y=data['Deaths'].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
fig.update_layout(title=dict(text='New Deaths',),yaxis=dict(rangemode="nonnegative"))
fig.write_html("./chart_htmls/deaths.html")

# Tests
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=data['Tested'].diff(),name='New Tests',marker_color='orange'))
fig.add_trace(go.Line(x=data['Date'], y=data['Tested'].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
fig.update_layout(title=dict(text='New Tests',))
fig.write_html("./chart_htmls/tests.html")

########### Demographic Statistics ################
# Ages
fig = go.Figure(layout=layout)
ages_data = data.iloc[:,10:18].diff().rolling(7).mean()
for i in range(len(AGES_LIST)):
    fig.add_trace(go.Line(x=data['Date'], y=ages_data.iloc[:,i],name=AGES_LIST[i],line=dict(color=G10[i],)))
fig.update_layout(title=dict(text='New Cases by Age, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/ages.html")

# New Cases Makeup
age_daily_s = ages_data*7
age_daily_s_pct = age_daily_s.divide(age_daily_s.sum(axis=1),axis=0)
fig = go.Figure(layout=layout)
for i in range(8):
    fig.add_trace(go.Line(
        x=data['Date'],y=age_daily_s_pct.iloc[:,i],
        mode='lines',
        stackgroup='one',
        name=AGES_LIST[i],
        line=dict(color=G10[i],width=0)
    ))
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(range=['2020-03-16',data.index[-1]])
fig.update_layout(title=dict(text='Breakdown of New Cases by Age, 7-Day Average'),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/ages_makeup.html")


# # Ages of Cases
# fig = go.Figure(data=[go.Pie(labels=AGES_LIST,values=data.loc[data.index[-1],'age0-18':'age81'],marker=dict(colors=G10))],layout=layout)
# fig.update_layout(title=dict(text='Case Breakdown by Age'),legend=dict(y=0.75,x=1))
# # Ages of Deaths
# fig = go.Figure(data=[go.Pie(labels=data.columns[186:194],values=data.loc[data.index[-1],'0-19':'80+'],marker=dict(colors=G10))],layout=layout)
# fig.update_layout(title=dict(text='Death Breakdown by Age'),legend=dict(y=0.75,x=1))
# # Race of Cases
# fig = go.Figure(data=[go.Pie(labels=data.columns[47:53],values=data.iloc[-1,47:53],marker=dict(colors=ANTIQUE))],layout=layout)
# fig.update_layout(title=dict(text='Case Breakdown by Race'),legend=dict(y=0.75,x=1))
# # Race of Deaths
# fig = go.Figure(data=[go.Pie(labels=data.columns[37:42],values=data.iloc[-1,37:42],marker=dict(colors=ANTIQUE_ALT))],layout=layout)
# fig.update_layout(title=dict(text='Death Breakdown by Race/Ethnicity'),legend=dict(y=0.75,x=1))

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
WARD_LIST = ['Ward 1','Ward 2','Ward 3','Ward 4','Ward 5','Ward 6','Ward 7','Ward 8']
NHOOD_START_IDX = 81
NTEST_START_IDX = 134

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
# Define positive tests in DC
dc_pos = data['New Cases'].rolling(7).sum().divide(data['New Tested'].rolling(7).sum())

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


# Ages of Cases
fig = go.Figure(data=[go.Pie(labels=AGES_LIST,values=data.loc[data.index[-1],'age0-18':'age81'],marker=dict(colors=G10))],layout=layout)
fig.update_layout(title=dict(text='Case Breakdown by Age'),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/ages_cases_pie.html")
# Ages of Deaths
fig = go.Figure(data=[go.Pie(labels=data.columns[186:194],values=data.loc[data.index[-1],'0-19':'80+'],marker=dict(colors=G10))],layout=layout)
fig.update_layout(title=dict(text='Death Breakdown by Age'),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/ages_deaths_pie.html")
# Race of Cases
fig = go.Figure(data=[go.Pie(labels=data.columns[47:53],values=data.iloc[-1,47:53],marker=dict(colors=ANTIQUE))],layout=layout)
fig.update_layout(title=dict(text='Case Breakdown by Race'),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/races_cases_pie.html")
# Race of Deaths
fig = go.Figure(data=[go.Pie(labels=data.columns[37:42],values=data.iloc[-1,37:42],marker=dict(colors=ANTIQUE_ALT))],layout=layout)
fig.update_layout(title=dict(text='Death Breakdown by Race/Ethnicity'),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/races_deaths_pie.html")

########### Wards #####################
# Ward Cases
fig = go.Figure(layout=layout)
ward_avg = data.loc[:,'Ward 1':'Ward 8'].diff().rolling(7).mean()
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=ward_avg[WARD_LIST[i]],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
fig.update_layout(title=dict(text='New Cases by Ward, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/wards.html")

#Ward Breakdown
ward_daily_s = data.loc[:,WARD_LIST].diff().rolling(7).sum()
ward_daily_s_pct = ward_daily_s.divide(ward_daily_s.sum(axis=1),axis=0)
fig = go.Figure(layout=layout)
for i in range(8):
    fig.add_trace(go.Line(
        x=data['Date'],y=ward_daily_s_pct.iloc[:,i],
        mode='lines',
        stackgroup='one',
        name=WARD_LIST[i],
        line=dict(color=PASTELS[i],width=0)
    ))
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(range=['2020-03-16',data.index[-1]])
fig.update_layout(title=dict(text='Breakdown of New Cases by Ward, 7-Day Average'),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/wards_breakdown.html")

# Per Capita Ward Cases
fig = go.Figure(layout=layout)
ward_avg_pc = np.divide(ward_avg,ward_demos.loc[WARD_LIST,'Population (2020)'])*10000
dc_avg_pc = np.divide(data['Positives'].diff().rolling(7).mean(), ward_demos.loc['All Wards','Population (2020)'])*10000
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=ward_avg_pc[WARD_LIST[i]],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
fig.add_trace(go.Line(x=data['Date'], y=dc_avg_pc,name='District-Wide',line=dict(color='black')))
fig.update_layout(title=dict(text='New Cases Per 10,000 Residents, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/wards_pc.html")

# Ward Positivity
fig = go.Figure(layout=layout)
positivity = np.divide(data.loc[:,'Ward 1':'Ward 8'].diff().rolling(7).sum(),data.loc[:,'Ward 1 Tests':'Ward 8 Tests'].diff().rolling(7).sum())
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=positivity.iloc[:,i],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
fig.add_trace(go.Line(x=data['Date'], y=dc_pos,name='District-Wide',line=dict(color='black')))
fig.update_layout(title=dict(text='Positivity by Ward, 7-Day Average'),yaxis=dict(tickformat=".1%"),legend=dict(x=0.99))
fig.write_html("./chart_htmls/wards_positivity.html")

# Ward Deaths
fig = go.Figure(data=[go.Bar(
    x=WARD_LIST,
    y=data.iloc[-1,58:66],
    name='Deaths',
    marker_color=PASTELS[0:8] # marker color can be a single color value or an iterable
)],layout = layout)
fig.update_layout(title=dict(text='Total Deaths'))
st.plotly_chart(fig)

# Ward Deaths Per Capita
ward_deaths = data.iloc[-1,58:66]
ward_deaths.index = WARD_LIST
fig = go.Figure(data=[go.Bar(
    x=WARD_LIST,
    y=ward_deaths.divide(ward_demos.loc[WARD_LIST,'Population (2020)'])*10000,
    name='Deaths',
    marker_color=PASTELS[0:8] # marker color can be a single color value or an iterable
)],layout = layout)
fig.update_layout(title=dict(text='Deaths per 10,000 Residents'),yaxis=dict(tickformat=".1f"))
st.plotly_chart(fig)

############## Hospital Statistics ####################
st.header('Hospital Statistics')

# COVID Patients Only
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Patients'],name='Hospitalized',marker_color=DARK2[0]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID ICU Patients'],name='In ICU',marker_color=DARK2[1]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Ventilators'], name = 'On Ventilator',marker_color=DARK2[2]))
fig.update_layout(title=dict(text='COVID Patients'),barmode='overlay',legend=dict(x=1))
fig.write_html("./chart_htmls/patients.html")

# Hospitalized
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['Total Patients'],name='Total Patients',marker_color=PASTEL2[0]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Patients'],name='COVID Patients',marker_color=DARK2[0]))
fig.add_trace(go.Line(x=data['Date'],y=np.full((data['Date'].size), 2487, dtype=int),name='Total Hospital Beds',marker_color='black'))
fig.update_layout(title=dict(text='All Hospitalized'),barmode='overlay',legend=dict(x=1))
fig.write_html("./chart_htmls/patients_hospitalized.html")
# In ICU
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['Total ICU Beds']-data['ICU Beds Available'],name='Total Patients in ICU',marker_color=PASTEL2[1]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID ICU Patients'],name='COVID Patients in ICU',marker_color=DARK2[1]))
fig.add_trace(go.Line(x=data['Date'],y=data['Total ICU Beds'],name='Total ICU Beds',marker_color='black'))
fig.update_layout(title=dict(text='All ICU Patients'),barmode='overlay',legend=dict(x=1))
fig.write_html("./chart_htmls/patients_icu.html")
# Ventilated
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['In-Use Ventilators'],name='Total Patients on Ventilators',marker_color=PASTEL2[2]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Ventilators'],name='COVID Patients on Ventilators',marker_color=DARK2[2]))
fig.add_trace(go.Line(x=data['Date'],y=data['Total Ventilators'],name='Total Ventilators',marker_color='black'))
fig.update_layout(title=dict(text='All Patients on Ventilators'),barmode='overlay',legend=dict(x=1))
fig.write_html("./chart_htmls/patients_ventilator.html")

############# MAPS #################
hood_data = data.iloc[:,NHOOD_START_IDX:NHOOD_START_IDX+51].diff().rolling(7).mean()
hood_data_pc = hood_data.divide(hood_demos['Population (2018 ACS)'])*10000
rolling_cases = data.iloc[:,NHOOD_START_IDX:NHOOD_START_IDX+51].diff().rolling(7).sum()
rolling_tests = data.iloc[:,NTEST_START_IDX:NTEST_START_IDX+51].diff().rolling(7).sum()
rolling_tests.columns = rolling_cases.columns
hood_positive = np.divide(rolling_cases,rolling_tests)
pos_this_week = hood_positive.iloc[-1,:].sort_values()
pos_this_week = pd.concat([pos_this_week,rolling_cases.iloc[-1,:],rolling_tests.iloc[-1,:],hood_demos['Population (2018 ACS)'],hood_demos['OBJECTID']],axis=1)
pos_this_week.columns = ['Positivity This Week','Positives This Week','Tests This Week','Population','OBJECTID']
pos_this_week['Positives This Week Per 10k'] = pos_this_week['Positives This Week'].divide(pos_this_week['Population']) * 10000
pos_this_week['Neighborhood'] = pos_this_week.index
map_list = ['Positives This Week Per 10k','Positives This Week','Positivity This Week']
for plotdata in map_list:
    if(plotdata=='Positives This Week Per 10k'):
        range_color = (0,25)
        filename = "./chart_htmls/nhood_map_pc.html"
    elif(plotdata=='Positives This Week'):
        range_color = (0,np.max(pos_this_week['Positives This Week']))
        filename = "./chart_htmls/nhood_map_cases.html"
    elif(plotdata=='Positivity This Week'):
        range_color = (0,.10)
        filename = "./chart_htmls/nhood_map_positivity.html"
    fig = px.choropleth_mapbox(pos_this_week, geojson=hood_map, color=plotdata,
                               locations="OBJECTID", featureidkey="properties.OBJECTID",
                               center={"lat": 38.91, "lon": -77.03},
                               color_continuous_scale="Hot_r",
                               range_color=range_color,
                               opacity=0.5,
                               mapbox_style="carto-positron", zoom=10,
                               hover_name='Neighborhood',
                               hover_data={'Neighborhood':False,
                                           'OBJECTID':False,
                                           'Positives This Week':True,
                                           'Tests This Week':True,
                                           'Population':True,
                                           'Positivity This Week':':.2%',
                                           'Positives This Week Per 10k':':.1f'})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_html(filename)

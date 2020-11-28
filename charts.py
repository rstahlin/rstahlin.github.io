import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.cm
import matplotlib.colors
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        gridwidth=1),
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

LIGHT24 = px.colors.qualitative.Dark24

AGES_LIST = ['0-18','19-30','31-40','41-50','51-60','61-70','71-80','81+']
WARD_LIST = ['Ward 1','Ward 2','Ward 3','Ward 4','Ward 5','Ward 6','Ward 7','Ward 8']
NHOOD_START_IDX = 81
NTEST_START_IDX = 134
HOOD_LIST =['16th St Heights', 'Cathedral Heights', 'Chevy Chase', 'Chinatown', 'Columbia Heights', 'Congress Heights/Shipley', 'DC Medical Center', 'Douglass', 'Eastland Gardens', 'Edgewood', 'Forest Hills', 'Adams Morgan', 'Fort Dupont', 'Fort Lincoln/Gateway', 'Georgetown', 'Georgetown East', 'GWU', 'Hill East', 'Historic Anacostia', 'Kent/Palisades', 'Kingman Park', 'Lamond Riggs', 'Barnaby Woods', 'Lincoln Heights', 'Logan Circle/Shaw', 'Marshall Heights', 'Michigan Park', 'Mount Pleasant', 'National Mall', 'Naval Station & Air Force', 'Naylor/Hillcrest', 'Petworth', 'Saint Elizabeths', 'Bellevue', 'Shepherd Park', 'South Columbia Heights', 'Stadium Armory', 'SW/Waterfront', 'Tenleytown', 'Trinidad', 'Twining', 'U St/Pleasant Plains', 'Union Station', 'Washington Highlands', 'Bloomingdale', 'Woodley Park', 'Woodridge', 'Brentwood', 'Brightwood', 'Brightwood Park', 'Capitol Hill']

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
dc_pos = data['Positives'].diff().rolling(7).sum().divide(data['Tested'].diff().rolling(7).sum())
# dc_pos = data.[:,'Ward 1':'Unknown Ward'].diff().rolling(7).sum().divide(data.loc[:,'Ward 1 Tests':'Unknown Ward Tests'].diff().rolling(7).sum())

data['Date'] = pd.to_datetime(data['Date'])

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
fig.update_layout(title=dict(text='Positivity by Ward, 7-Day Average'),yaxis=dict(tickformat=".1%"),legend=dict(y=0.75,x=1))
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

# Ward Test Rates
fig = go.Figure(layout=layout)
ward_test_pc = np.divide(data.loc[:,'Ward 1 Tests':'Ward 8 Tests'].diff().rolling(7).mean(),ward_demos.loc[WARD_LIST,'Population (2020)'])*10000
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=ward_test_pc.iloc[:,i],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
dc_tests = np.divide(data['Tested'].diff().rolling(7).mean(), ward_demos.loc['All Wards','Population (2020)'])*10000
fig.add_trace(go.Line(x=data['Date'], y=dc_tests,name='District-Wide',line=dict(color='black')))
fig.update_layout(title=dict(text='Tests Per 10,000 Residents, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/wards_tests.html")


############## Hospital Statistics ####################
st.header('Hospital Statistics')

# COVID Patients Only
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Patients'],name='Hospitalized',marker_color=DARK2[0]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID ICU Patients'],name='In ICU',marker_color=DARK2[1]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Ventilators'], name = 'On Ventilator',marker_color=DARK2[2]))
fig.update_layout(title=dict(text='COVID Patients'),barmode='overlay',legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/patients.html")

# Hospitalized
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['Total Patients'],name='Total Patients',marker_color=PASTEL2[0]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Patients'],name='COVID Patients',marker_color=DARK2[0]))
fig.add_trace(go.Line(x=data['Date'],y=np.full((data['Date'].size), 2487, dtype=int),name='Total Hospital Beds',marker_color='black'))
fig.update_layout(title=dict(text='All Hospitalized'),barmode='overlay',legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/patients_hospitalized.html")
# In ICU
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['Total ICU Beds']-data['ICU Beds Available'],name='Total Patients in ICU',marker_color=PASTEL2[1]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID ICU Patients'],name='COVID Patients in ICU',marker_color=DARK2[1]))
fig.add_trace(go.Line(x=data['Date'],y=data['Total ICU Beds'],name='Total ICU Beds',marker_color='black'))
fig.update_layout(title=dict(text='All ICU Patients'),barmode='overlay',legend=dict(y=0.75,x=1))
fig.write_html("./chart_htmls/patients_icu.html")
# Ventilated
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['In-Use Ventilators'],name='Total Patients on Ventilators',marker_color=PASTEL2[2]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Ventilators'],name='COVID Patients on Ventilators',marker_color=DARK2[2]))
fig.add_trace(go.Line(x=data['Date'],y=data['Total Ventilators'],name='Total Ventilators',marker_color='black'))
fig.update_layout(title=dict(text='All Patients on Ventilators'),barmode='overlay',legend=dict(y=0.75,x=1))
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
pos_this_week.to_html('nhoods_this_week.html')
map_list = ['Positives This Week Per 10k','Positives This Week','Positivity This Week']
for plotdata in map_list:
    if(plotdata=='Positives This Week Per 10k'):
        no_nat_mall = pos_this_week.drop(index=['National Mall'])
        range_color = (0,np.max(no_nat_mall['Positives This Week Per 10k']))
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



############## NEIGHBORHOODS ####################
to_plot = hood_data_pc.drop(columns=['National Mall'])
to_plot = to_plot.sort_values(by=to_plot.index[-1],axis=1,ascending=False)


nrows = 6
ncols = 9

fig = make_subplots(rows=nrows, cols=ncols, shared_xaxes=True, shared_yaxes=True,subplot_titles=to_plot.columns)
index = 0
row = 1
col = 1
for nhood in to_plot.columns:
    fig.add_trace(go.Scatter(x=to_plot.index,y=to_plot[nhood],line=dict(color='black'),name=nhood),row=row,col=col)

    index += 1
    if col == ncols:
        row+=1
        col = 0
    col+=1

fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    font=dict(family='Arial'),
    title = dict(x=0.5,text='7-Day Average Cases per 10,000 Residents in the last 14 Days')
)

fig.update_layout(showlegend=False)
fig.update_xaxes(range=[to_plot.index[-15],to_plot.index[-1]],
        showspikes=True,
        showticklabels = False,
        spikedash = 'solid',
        spikecolor = 'black',
        spikemode  = 'across',
        spikesnap = 'cursor')
fig.update_yaxes(rangemode = 'tozero',showticklabels = False,
        showgrid=False,
        range=[0,6.5])
for i in fig['layout']['annotations']:
    i['font'] = dict(size=9)
fig.write_html('chart_htmls/nhood_matrix_pc.html')

# Neighborhood cases
fig = go.Figure(layout=layout)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data[HOOD_LIST[i]],name=HOOD_LIST[i],visible='legendonly',line=dict(color=LIGHT24[i%24])))
fig.update_yaxes(rangemode="nonnegative")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='New Positives, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(
    orientation="h",
    yanchor="top",
    y=-.1,
    xanchor="center",
    x=.5
))
fig.write_html('chart_htmls/nhood_cases.html')


# Neighborhoods Per capita
fig = go.Figure(layout=layout)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data_pc[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
fig.add_trace(go.Line(x=data['Date'], y=dc_avg_pc,name='District-Wide',line=dict(color='black',width=3.0)))
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data_pc[HOOD_LIST[i]],name=HOOD_LIST[i],visible='legendonly',line=dict(color=LIGHT24[i%24])))
fig.update_yaxes(rangemode="nonnegative",range=[0,10])
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='New Positives per 10,000 Residents, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(
    orientation="h",
    yanchor="top",
    y=-.1,
    xanchor="center",
    x=.5
))
fig.write_html('chart_htmls/nhood_pc.html')

# Neighborhood Test positivity
fig = go.Figure(layout=layout)
hood_positive = np.divide(rolling_cases,rolling_tests)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_positive[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_positive[HOOD_LIST[i]],name=HOOD_LIST[i],visible='legendonly',line=dict(color=LIGHT24[i%24])))
fig.add_trace(go.Line(x=data['Date'],y=dc_pos,name="District-Wide",line=dict(color='black')))
fig.update_yaxes(rangemode="nonnegative",range=[0,.15],tickformat=".0%")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='Test Positivity, 7-Day Average'),legend=dict(
    orientation="h",
    yanchor="top",
    y=-.1,
    xanchor="center",
    x=.5
))
fig.write_html('chart_htmls/nhood_positivity.html')

diamond_dict={
'16th St Heights':(3,4),
 'Cathedral Heights':(5,2),
 'Chevy Chase':(3,3),
 'Chinatown':(7,5),
 'Columbia Heights':(4,5),
 'Congress Heights/Shipley':(9,6),
 'DC Medical Center':(4,6),
 'Douglass':(9,7),
 'Eastland Gardens':(5,9),
 'Edgewood':(5,6),
 'Forest Hills':(4,3),
 'Adams Morgan':(6,3),
 'Fort Dupont':(6,9),
 'Fort Lincoln/Gateway':(4,8),
 'Georgetown':(6,2),
 'Georgetown East':(7,3),
 'GWU':(7,4),
 'Hill East':(7,7),
 'Historic Anacostia':(8,7),
 'Kent/Palisades':(5,1),
 'Kingman Park':(6,7),
 'Lamond Riggs':(2,6),
 'Barnaby Woods':(2,4),
 'Lincoln Heights':(6,10),
 'Logan Circle/Shaw':(6,4),
 'Marshall Heights':(7,9),
 'Michigan Park':(4,7),
 'Mount Pleasant':(4,4),
 'National Mall':(8,5),
 'Naval Station & Air Force':(10,5),
 'Naylor/Hillcrest':(8,8),
 'Petworth':(3,6),
 'Saint Elizabeths':(8,6),
 'Bellevue':(11,5),
 'Shepherd Park':(1,5),
 'South Columbia Heights':(5,4),
 'Stadium Armory':(6,8),
 'SW/Waterfront':(9,5),
 'Tenleytown':(4,2),
 'Trinidad':(5,8),
 'Twining':(7,8),
 'U St/Pleasant Plains':(5,5),
 'Union Station':(6,6),
 'Washington Highlands':(10,6),
 'Bloomingdale':(6,5),
 'Woodley Park':(5,3),
 'Woodridge':(3,7),
 'Brentwood':(5,7),
 'Brightwood':(2,5),
 'Brightwood Park':(3,5),
 'Capitol Hill':(7,6)
}
to_plot = hood_data_pc.drop(columns=['National Mall'])
to_plot = to_plot.sort_values(by=to_plot.index[-1],axis=1,ascending=False)


nrows = 11
ncols = 11

vmin, vmax = to_plot.iloc[-1,:].min(), to_plot.iloc[-1,:].max()


norm = matplotlib.colors.Normalize(vmin=0, vmax=vmax)
cmap = matplotlib.cm.get_cmap('YlOrRd') # yellow to orange to red

fig = make_subplots(rows=nrows, cols=ncols, shared_xaxes=True, shared_yaxes=True,vertical_spacing=0.005,horizontal_spacing=0.005)
ymax = np.max(np.max(to_plot.iloc[-15:-1,:]))*1.1


for nhood in hood_data_pc.columns:
    color = 'rgba' + str(cmap(norm(np.round(hood_data_pc[nhood][-1]),4)))[:]
    fig.add_trace(go.Scatter(x=[hood_data_pc.index[-15],hood_data_pc.index[-1]],y= [ymax*1.5,ymax*1.5],fill='tozeroy',fillcolor=color,hoverinfo='skip'),row=diamond_dict[nhood][0],col=diamond_dict[nhood][1])
    if nhood != 'National Mall':
        fig.add_trace(go.Scatter(x=hood_data_pc.index,
                                 y=hood_data_pc[nhood],
                                 line=dict(color='black'),
                                 name=nhood,
                                 hovertemplate="%{y:.1f}"),row=diamond_dict[nhood][0],col=diamond_dict[nhood][1])
    else:
        fig.add_trace(go.Scatter(x=hood_data_pc.index,
                             y=hood_data_pc[nhood],
                             line=dict(color='black'),
                             name=nhood,
                             hovertemplate="%{y:.1f} (May be anomalous)"),row=diamond_dict[nhood][0],col=diamond_dict[nhood][1])


fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    font=dict(family='Arial'),
    title = dict(x=0.5,text='7-Day Average Cases per 10,000 Residents (Last 2 Weeks)'),
    showlegend=False,width=750, height=750)
fig.update_xaxes(range=[to_plot.index[-15],to_plot.index[-1]],
        showspikes=False,
        showticklabels = False,
        spikedash = 'solid',
        spikecolor = 'black',
        spikemode  = 'across',
        spikesnap = 'cursor',
        fixedrange = True)

fig.update_yaxes(rangemode = 'tozero',showticklabels = False,
        showgrid=False,
        range=[0,ymax],tickformat="0.1f",
        fixedrange = True)

fig.write_html('chart_htmls/nhood_diamond_pc.html')

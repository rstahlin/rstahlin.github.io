import pandas as pd
import numpy as np
import streamlit as st
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
        gridwidth=0.01),
    legend=dict(yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01),
    hovermode='x',
    font=dict(family='Arial'),
    title = dict(x=0.5)
)

NHOOD_START_IDX = 81
NTEST_START_IDX = 134
HOOD_LIST =['16th St Heights', 'Cathedral Heights', 'Chevy Chase', 'Chinatown', 'Columbia Heights', 'Congress Heights/Shipley', 'DC Medical Center', 'Douglass', 'Eastland Gardens', 'Edgewood', 'Forest Hills', 'Adams Morgan', 'Fort Dupont', 'Fort Lincoln/Gateway', 'Georgetown', 'Georgetown East', 'GWU', 'Hill East', 'Historic Anacostia', 'Kent/Palisades', 'Kingman Park', 'Lamond Riggs', 'Barnaby Woods', 'Lincoln Heights', 'Logan Circle/Shaw', 'Marshall Heights', 'Michigan Park', 'Mount Pleasant', 'National Mall', 'Naval Station & Air Force', 'Naylor/Hillcrest', 'Petworth', 'Saint Elizabeths', 'Bellevue', 'Shepherd Park', 'South Columbia Heights', 'Stadium Armory', 'SW/Waterfront', 'Tenleytown', 'Trinidad', 'Twining', 'U St/Pleasant Plains', 'Union Station', 'Washington Highlands', 'Bloomingdale', 'Woodley Park', 'Woodridge', 'Brentwood', 'Brightwood', 'Brightwood Park', 'Capitol Hill']
WARD_LIST = ['Ward 1','Ward 2','Ward 3','Ward 4','Ward 5','Ward 6','Ward 7','Ward 8']
AGES_LIST = ['0-18','19-30','31-40','41-50','51-60','61-70','71-80','81+']

WARD_1_LIST = ['Mount Pleasant','Columbia Heights','South Columbia Heights','Adams Morgan','U St/Pleasant Plains']
WARD_2_LIST = ['Georgetown','Georgetown East','GWU','Logan Circle/Shaw','Chinatown']
WARD_3_LIST = ['Chevy Chase','Forest Hills','Tenleytown','Kent/Pallisades','Cathedral Heights','Woodley Park']
WARD_4_LIST = ['Barnaby Woods','Shepherd Park','Brightwood','Brightwood Park','Petworth','16th St Heights','Lamond Riggs',]
WARD_5_LIST = ['DC Medical Center','Bloomingdale','Edgewood','Brentwood','Trinidad','Fort Lincoln/Gateway','Woodridge']
WARD_6_LIST = ['Union Stataion','Capitol Hill','SW/Waterfront','Hill East','Kingman Park','Michigan Park']
WARD_7_LIST = ['Stadium Armory','Fort Dupont', 'Eastland Gardens','Lincoln Heights','Marshall Heights','Twining','Naylor/Hillcrest']
WARD_8_LIST = ['Historic Anacostia','Douglass','Saint Elizabeths','Naval Station & Air Force','Congress Heights/Shipley','Washington Highlands','Bellevue']

PASTELS = px.colors.qualitative.Pastel
DARK2 = px.colors.qualitative.Dark2
PASTEL2 = px.colors.qualitative.Pastel2
G10 = px.colors.qualitative.G10
ANTIQUE = px.colors.qualitative.Antique
ANTIQUE_ALT = [ANTIQUE[2],ANTIQUE[1],ANTIQUE[6],ANTIQUE[0],ANTIQUE[5]]
LIGHT24 = px.colors.qualitative.Light24



st.title('Charting Covid')

@st.cache
def load_data():
    dccovid = pd.read_csv(r'data.csv')
    dccovid.index = pd.to_datetime(dccovid['Date'])
    dccovid['Unknown Ward Tests'] = pd.to_numeric(dccovid['Unknown Ward Tests'])
    hood_demos = pd.read_csv(r'nhood_demographics.csv',index_col='Neighborhood Name')
    ward_demos = pd.read_csv(r'ward_demographics.csv', index_col='Ward')
    with urlopen('https://opendata.arcgis.com/datasets/de63a68eb7674548ae0ac01867123f7e_13.geojson') as response:
        hood_map = json.load(response)
    groups_dict = {
        "Under 20*":("age0-18","0-19"),
        "20s*":("age19-30","20-29"),
        "30s*":("age31-40","30-39"),
        "40s*":("age41-50","40-49"),
        "50s*":("age51-60","50-59"),
        "60s*":("age61-70","60-69"),
        "70s*":("age71-80","70-79"),
        "80+*":("age81","80+"),
        "Ward 1":("Ward 1","Ward 1 Deaths"),
        "Ward 2":("Ward 2","Ward 2 Deaths"),
        "Ward 3":("Ward 3","Ward 3 Deaths"),
        "Ward 4":("Ward 4","Ward 4 Deaths"),
        "Ward 5":("Ward 5","Ward 5 Deaths"),
        "Ward 6":("Ward 6","Ward 6 Deaths"),
        "Ward 7":("Ward 7","Ward 7 Deaths"),
        "Ward 8":("Ward 8","Ward 8 Deaths"),
        "People in Shelter":("People Who Were in Shelter","Homeless Deaths"),
        "Hispanic/Lantinx":("Hispanic or Latinx Ethnicity","Hispanic/Latinx Deaths"),
        "Asian":("Asian","Asian Deaths"),
        "Black":("Black","Black/African American Deaths"),
        "White†":("White","Non-Hispanic White Deaths"),
    }
    return dccovid, hood_demos, ward_demos, hood_map, groups_dict
#

# Load data into the dataframe.
data, hood_demos, ward_demos, hood_map, groups_dict = load_data()



# Notify the reader that the data was successfully loaded.
st.markdown('This information is compiled from DC\'s official coronavirus website and is subject to changes, typos, and incompleteness')
st.header('Top Level Information')
'Data updated as of ', data.index[-1].strftime('%A, %B %d'),'...'
'New Cases Reported:',int(data['Positives'].diff()[-1])
'New Deaths Reported:',int(data['Deaths'].diff()[-1])
'Total Cases:',int(data['Positives'][-1])
'Total Deaths:',int(data['Deaths'][-1])
'Total Recoveries',int(data['Recoveries'][-1])

############## Core Statistics ####################
st.header('New Cases, Deaths, and Tests')
# Cases
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=data['Positives'].diff(),name='New Cases',marker_color='rgb(158,202,225)'))
fig.add_trace(go.Line(x=data['Date'], y=data['Positives'].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
# fig.add_trace(go.Line(x=data['Date'], y=data['Date Corrected Positives'].rolling(7).mean(),name='7-Day Average, Date Corrected',line=dict(dash='dash',color='black')))
fig.update_layout(title=dict(text='New Cases'))
st.plotly_chart(fig)
# Deaths
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=data['Deaths'].diff(),name='New Deaths',marker_color='maroon'))
fig.add_trace(go.Line(x=data['Date'], y=data['Deaths'].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
fig.update_layout(title=dict(text='New Deaths',),yaxis=dict(rangemode="nonnegative"))
st.plotly_chart(fig)
# Tests
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=data['Tested'].diff(),name='New Tests',marker_color='orange'))
fig.add_trace(go.Line(x=data['Date'], y=data['Tested'].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
fig.update_layout(title=dict(text='New Tests',))
st.plotly_chart(fig)
# positivity
# fig = go.Figure(layout=layout)
dc_pos = data['New Cases'].rolling(7).sum().divide(data['New Tested'].rolling(7).sum())
# fig.add_trace(go.Line(x=data['Date'], y=ydata,name='7-Day Average',line=dict(color='black')))
# fig.update_layout(title=dict(text='Positivity'),yaxis=dict(tickformat=".1%"))
# st.plotly_chart(fig)

########### Demographic Statistics ################
st.header('Demographic Statistics')

# New Cases by Age
fig = go.Figure(layout=layout)
ages_data = data.iloc[:,10:18].diff().rolling(7).mean()
for i in range(len(AGES_LIST)):
    fig.add_trace(go.Line(x=data['Date'], y=ages_data.iloc[:,i],name=AGES_LIST[i],line=dict(color=G10[i],)))
fig.update_layout(title=dict(text='New Cases by Age, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
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
st.plotly_chart(fig)
# Ages of Cases
fig = go.Figure(data=[go.Pie(labels=AGES_LIST,values=data.loc[data.index[-1],'age0-18':'age81'],marker=dict(colors=G10))],layout=layout)
fig.update_layout(title=dict(text='Case Breakdown by Age'),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Ages of Deaths
fig = go.Figure(data=[go.Pie(labels=data.columns[186:194],values=data.loc[data.index[-1],'0-19':'80+'],marker=dict(colors=G10))],layout=layout)
fig.update_layout(title=dict(text='Death Breakdown by Age'),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Race of Cases
fig = go.Figure(data=[go.Pie(labels=data.columns[47:53],values=data.iloc[-1,47:53],marker=dict(colors=ANTIQUE))],layout=layout)
fig.update_layout(title=dict(text='Case Breakdown by Race'),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Race of Deaths
fig = go.Figure(data=[go.Pie(labels=data.columns[37:42],values=data.iloc[-1,37:42],marker=dict(colors=ANTIQUE_ALT))],layout=layout)
fig.update_layout(title=dict(text='Death Breakdown by Race/Ethnicity'),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)


############## Ward Statistics ####################
st.header('Ward Statistics')
# New Cases Makeup
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
st.plotly_chart(fig)
# Ward Cases
fig = go.Figure(layout=layout)
ward_avg = data.loc[:,'Ward 1':'Ward 8'].diff().rolling(7).mean()
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=ward_avg[WARD_LIST[i]],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
fig.update_layout(title=dict(text='New Cases by Ward, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Per Capita Cases
fig = go.Figure(layout=layout)
ward_avg_pc = np.divide(ward_avg,ward_demos.loc[WARD_LIST,'Population (2020)'])*10000
dc_avg_pc = np.divide(data['Positives'].diff().rolling(7).mean(), ward_demos.loc['All Wards','Population (2020)'])*10000
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=ward_avg_pc[WARD_LIST[i]],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
fig.add_trace(go.Line(x=data['Date'], y=dc_avg_pc,name='District-Wide',line=dict(color='black')))
fig.update_layout(title=dict(text='New Cases Per 10,000 Residents, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Ward Positivity
fig = go.Figure(layout=layout)
positivity = np.divide(data.loc[:,'Ward 1':'Ward 8'].diff().rolling(7).sum(),data.loc[:,'Ward 1 Tests':'Ward 8 Tests'].diff().rolling(7).sum())
for i in range(8):
    fig.add_trace(go.Line(x=data['Date'], y=positivity.iloc[:,i],name=WARD_LIST[i],line=dict(color=PASTELS[i])))
fig.add_trace(go.Line(x=data['Date'], y=dc_pos,name='District-Wide',line=dict(color='black')))
fig.update_layout(title=dict(text='Positivity by Ward, 7-Day Average'),yaxis=dict(tickformat=".1%"),legend=dict(x=0.99))
st.plotly_chart(fig)
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
st.plotly_chart(fig)
# Hospitalized
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['Total Patients'],name='Total Patients',marker_color=PASTEL2[0]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Patients'],name='COVID Patients',marker_color=DARK2[0]))
fig.add_trace(go.Line(x=data['Date'],y=np.full((data['Date'].size), 2487, dtype=int),name='Total Hospital Beds',marker_color='black'))
fig.update_layout(title=dict(text='All Hospitalized'),barmode='overlay',legend=dict(x=1))
st.plotly_chart(fig)
# In ICU
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['Total ICU Beds']-data['ICU Beds Available'],name='Total Patients in ICU',marker_color=PASTEL2[1]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID ICU Patients'],name='COVID Patients in ICU',marker_color=DARK2[1]))
fig.add_trace(go.Line(x=data['Date'],y=data['Total ICU Beds'],name='Total ICU Beds',marker_color='black'))
fig.update_layout(title=dict(text='All ICU Patients'),barmode='overlay',legend=dict(x=1))
st.plotly_chart(fig)
# Ventilated
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'],y=data['In-Use Ventilators'],name='Total Patients on Ventilators',marker_color=PASTEL2[2]))
fig.add_trace(go.Bar(x=data['Date'],y=data['COVID Ventilators'],name='COVID Patients on Ventilators',marker_color=DARK2[2]))
fig.add_trace(go.Line(x=data['Date'],y=data['Total Ventilators'],name='Total Ventilators',marker_color='black'))
fig.update_layout(title=dict(text='All Patients on Ventilators'),barmode='overlay',legend=dict(x=1))
st.plotly_chart(fig)


############## Neighborhood Statistics ####################
st.header('Neighborhood Statistics')

# Neighborhood Select
hoods = st.multiselect('Choose Neighborhoods to Highlight',HOOD_LIST,default=['Columbia Heights','Capitol Hill'])
hood_data = data.iloc[:,NHOOD_START_IDX:NHOOD_START_IDX+51].diff().rolling(7).mean()
hood_data_pc = hood_data.divide(hood_demos['Population (2018 ACS)'])*10000
rolling_cases = data.iloc[:,NHOOD_START_IDX:NHOOD_START_IDX+51].diff().rolling(7).sum()
rolling_tests = data.iloc[:,NTEST_START_IDX:NTEST_START_IDX+51].diff().rolling(7).sum()
rolling_tests.columns = rolling_cases.columns
# Warning Sign
if 'GWU' in hoods:
    st.warning('Warning: GWU has reported inconsistent data in the past.')
if 'National Mall' in hoods:
    st.warning('Warning: National Mall has reported inconsistent data in the past.')
# New Cases
fig = go.Figure(layout=layout)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(len(hoods)):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data[hoods[i]],name=hoods[i]))
fig.update_yaxes(rangemode="nonnegative")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='New Positives, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# New Cases Per Capita
fig = go.Figure(layout=layout)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data_pc[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(len(hoods)):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data_pc[hoods[i]],name=hoods[i]))
fig.add_trace(go.Line(x=data['Date'], y=dc_avg_pc,name='District-Wide',line=dict(color='black')))
fig.update_yaxes(rangemode="nonnegative",range=[0,10])
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='New Positives per 10,000 Residents, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Positivity
fig = go.Figure(layout=layout)
hood_positive = np.divide(rolling_cases,rolling_tests)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_positive[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(len(hoods)):
    fig.add_trace(go.Line(x=data['Date'],y=hood_positive[hoods[i]],name=hoods[i]))
fig.add_trace(go.Line(x=data['Date'],y=dc_pos,name="District-Wide",line=dict(color='black')))
fig.update_yaxes(rangemode="nonnegative",range=[0,.5],tickformat=".0%")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='Test Positivity, 7-Day Average'),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)
# Test Positivity This Week
fig = go.Figure(layout=layout)
pos_this_week = hood_positive.iloc[-1,:].sort_values()
pos_this_week = pd.concat([pos_this_week,rolling_cases.iloc[-1,:],rolling_tests.iloc[-1,:],hood_demos['Population (2018 ACS)'],hood_demos['OBJECTID']],axis=1)
pos_this_week.columns = ['Positivity This Week','Positives This Week','Tests This Week','Population','OBJECTID']
pos_this_week['Positives This Week Per 10k'] = pos_this_week['Positives This Week'].divide(pos_this_week['Population']) * 10000
pos_this_week['Neighborhood'] = pos_this_week.index
fig = px.bar(pos_this_week,x='Positivity This Week',y='Neighborhood',
    orientation='h',
    hover_name='Neighborhood',
    hover_data={'Neighborhood':False,
                'Positives This Week':True,
                'Tests This Week':True,
                'Population':True,
                'Positivity This Week':':.3%'},
    width=800,height=1000,
    )
fig.update_layout(title = dict(text='Positivity This Week',x=0.5),
    autosize=False, hovermode='y',
    xaxis = dict(showspikes=False,
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=0.01,
        tickformat=".0%",
        mirror=False),
    yaxis=dict(showgrid=False),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial'),
)
fig.update_traces(marker_color='orange')
st.plotly_chart(fig)
# Per Capita New Cases This Week
pos_this_week = pos_this_week.sort_values(by='Positives This Week Per 10k')
fig = px.bar(pos_this_week,x='Positives This Week Per 10k',y=pos_this_week.index,
    orientation='h',
    hover_data=['Positives This Week','Tests This Week','Positivity This Week'],
    width=800,height=1000,
    )
fig.update_layout(title = dict(text='New Cases per 10,000 Residents',x=0.5),
    autosize=False, hovermode='y',
    xaxis = dict(showspikes=False,
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=0.01,
        # tickformat=".0%",
        mirror=False),
    yaxis=dict(showgrid=False),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial'),
)
fig.update_traces(marker_color='orange')
st.plotly_chart(fig)


group_names = [*groups_dict.keys()]
opt = st.selectbox('Choose Group to Highlight',group_names)
opt_cases  = data[groups_dict.get(opt)[0]].diff()
opt_deaths = data[groups_dict.get(opt)[1]].diff()

fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(x=data['Date'], y=opt_cases,name=opt+" Cases",marker_color='rgb(158,202,225)'))
fig.add_trace(go.Line(x=data['Date'], y=opt_cases.rolling(7).mean(),name='7-Day Average',line=dict(color='rgb(158,202,225)')))
fig.add_trace(go.Bar(x=data['Date'], y=opt_deaths,name=opt+" Deaths",marker_color='maroon'))
fig.add_trace(go.Line(x=data['Date'], y=opt_deaths.rolling(7).mean(),name='7-Day Average',line=dict(color='maroon')))
fig.update_layout(title=dict(text='Cases and Deaths'),yaxis = dict(rangemode = "nonnegative"))
st.plotly_chart(fig)
st.write("Fatality Rate: ",data[groups_dict.get(opt)[1]][-1]/data[groups_dict.get(opt)[0]][-1]*100)

################ MAPPING ########################
st.header('Maps')
st.subheader('New Cases This Week per 10,000 Residents')
plotdata = st.selectbox('Choose a Map View',['Positives This Week Per 10k','Positives This Week','Positivity This Week'],index=0)
if(plotdata=='Positives This Week Per 10k'):
    range_color = (0,25)
elif(plotdata=='Positives This Week'):
    range_color = (0,np.max(pos_this_week['Positives This Week']))
elif(plotdata=='Positivity This Week'):
    range_color = (0,.10)
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
st.plotly_chart(fig)
download = st.button("Download Map as HTML")
if download:
    fig.write_html(r'C:\\Users\\611817\\Downloads/COVID_map.html')

##################### Vulnerable Members of our Community #####################
# option = st.selectbox('Choose a category',['Incarcerated','People Who Were in Shelter'],0)
#
# fig = go.Figure(layout=layout)
# fig.add_trace(go.Bar(x=data['Date'], y=data[option].diff(),name=option,marker_color='rgb(158,202,225)'))
# fig.add_trace(go.Line(x=data['Date'], y=data[option].diff().rolling(7).mean(),name='7-Day Average',line=dict(color='black')))
# fig.update_layout(title=dict(text='New Cases'),yaxis = dict(rangemode = "nonnegative"))
#
# st.plotly_chart(fig)
#
#
st.header('WMATA Data')
fig = go.Figure(layout=layout)
fig.add_trace(go.Line(x=data['Date'],y=data['Rail Change'],name='Rail'))
fig.add_trace(go.Line(x=data['Date'],y=data['Bus Change'],name='Bus'))
fig.update_yaxes(tickformat=".0%")
fig.update_layout(title=dict(text='Ridership Relative to Equivalent Day in 2019'))

st.plotly_chart(fig)

fig = go.Figure(layout=layout)
fig.add_trace(go.Line(x=data['Date'],y=data['Rail Ridership'],name='Rail'))
fig.add_trace(go.Line(x=data['Date'],y=data['Bus Ridership'],name='Bus'))
fig.update_layout(title=dict(text='Number of Riders'))

st.plotly_chart(fig)


hood_data_pc_mapping = hood_data_pc.iloc[69:,:]
hood_data_pc_mapping.columns = hood_demos['OBJECTID']
hood_data_pc_mapping['Date'] = hood_data_pc_mapping.index
test = pd.melt(hood_data_pc_mapping,id_vars=['Date'],var_name = 'Neighborhood',value_name='New Positives per 10,000 Residents, 7-D Average')
test['Date'] = test['Date'].dt.strftime('%B %d')


fig = go.Figure(layout=layout)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data[HOOD_LIST[i]],name=HOOD_LIST[i],visible='legendonly',line=dict(color=LIGHT24[i%24])))
fig.update_yaxes(rangemode="nonnegative")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='New Positives, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=.99,x=1))
st.plotly_chart(fig)
download_neighborhood = st.button("Download Neighborhood Data as HTML")
if download_neighborhood:
    fig.write_html(r'C:\\Users\\611817\\Downloads/nhood_data.html')
# # New Cases Per Capita
fig = go.Figure(layout=layout)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data_pc[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
fig.add_trace(go.Line(x=data['Date'], y=dc_avg_pc,name='District-Wide',line=dict(color='black',width=3.0)))

for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_data_pc[HOOD_LIST[i]],name=HOOD_LIST[i],visible='legendonly',line=dict(color=LIGHT24[i%24])))

fig.update_yaxes(rangemode="nonnegative",range=[0,10])
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='New Positives per 10,000 Residents, 7-Day Average'),yaxis=dict(tickformat=".1f"),legend=dict(y=1,x=1))
st.plotly_chart(fig)
download_pc_neighborhood = st.button("Download Per Capita Neighborhood Data as HTML")
if download_pc_neighborhood:
    fig.write_html(r'C:\\Users\\611817\\Downloads/nhood_data_per_capita.html')

#positivity
fig = go.Figure(layout=layout)
hood_positive = np.divide(rolling_cases,rolling_tests)
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_positive[HOOD_LIST[i]],line=dict(color='lightgrey',width=0.5),hoverinfo='skip',showlegend=False))
for i in range(51):
    fig.add_trace(go.Line(x=data['Date'],y=hood_positive[HOOD_LIST[i]],name=HOOD_LIST[i],visible='legendonly',line=dict(color=LIGHT24[i%24])))
fig.add_trace(go.Line(x=data['Date'],y=dc_pos,name="District-Wide",line=dict(color='black')))
fig.update_yaxes(rangemode="nonnegative",range=[0,.5],tickformat=".0%")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(title=dict(text='Test Positivity, 7-Day Average'),legend=dict(y=0.75,x=1))
st.plotly_chart(fig)


download2 = st.button("Download Historical Map as HTML")
if download2:
    fig = px.choropleth_mapbox(test, geojson=hood_map, color='New Positives per 10,000 Residents, 7-D Average',
                                locations="Neighborhood", featureidkey="properties.OBJECTID",
                                center={"lat": 38.91, "lon": -77.03},
                                color_continuous_scale="Hot_r",
                                range_color=(0,5),
                                opacity=0.5,
                                mapbox_style="carto-positron", zoom=10,
                                animation_group='Neighborhood',
                                animation_frame='Date')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_html(r'C:\\Users\\611817\\Downloads/animated_COVID_map.html')

import pandas as pd
import numpy as np
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
    xaxis = dict(
        showspikes=True,
        spikedash = 'solid',
        spikemode  = 'across',
        spikesnap = 'cursor',
        spikecolor = 'black',
        spikethickness = 1,
        ticks='outside'),
    yaxis = dict(
        rangemode = 'tozero',
        showgrid=True,
        gridcolor='grey',
        gridwidth=1),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01),
    hovermode='x',
    font=dict(
        family='Arial',
        size=14
    ),
    title = dict(
        x=0.5
    )
)

PASTELS = px.colors.qualitative.Pastel
DARK2 = px.colors.qualitative.Dark2
PASTEL2 = px.colors.qualitative.Pastel2
G10 = px.colors.qualitative.G10
ANTIQUE = px.colors.qualitative.Antique
ANTIQUE_ALT = [ANTIQUE[2],ANTIQUE[1],ANTIQUE[6],ANTIQUE[0],ANTIQUE[5]]

LIGHT24 = px.colors.qualitative.Dark24

AGES_LIST = ['0-18','19-30','31-40','41-50','51-60','61-70','71-80','81+']
AGES_LIST_CENSUS = ['0-4','5-14','15-19','20-24','25-44','45-64','65+']
WARD_LIST = ['Ward 1','Ward 2','Ward 3','Ward 4','Ward 5','Ward 6','Ward 7','Ward 8']
RACE_LIST = ['White','Black','Asian','American Indian','Native Hawaiian Pacific Islander','Two or More Races','Unknown Race','Refused Race']
NHOOD_START_IDX = 81
NTEST_START_IDX = 134
HOOD_LIST =['16th St Heights', 'Cathedral Heights', 'Chevy Chase', 'Chinatown', 'Columbia Heights', 'Congress Heights/Shipley', 'DC Medical Center', 'Douglass', 'Eastland Gardens', 'Edgewood', 'Forest Hills', 'Adams Morgan', 'Fort Dupont', 'Fort Lincoln/Gateway', 'Georgetown', 'Georgetown East', 'GWU', 'Hill East', 'Historic Anacostia', 'Kent/Palisades', 'Kingman Park', 'Lamond Riggs', 'Barnaby Woods', 'Lincoln Heights', 'Logan Circle/Shaw', 'Marshall Heights', 'Michigan Park', 'Mount Pleasant', 'National Mall', 'Naval Station & Air Force', 'Naylor/Hillcrest', 'Petworth', 'Saint Elizabeths', 'Bellevue', 'Shepherd Park', 'South Columbia Heights', 'Stadium Armory', 'SW/Waterfront', 'Tenleytown', 'Trinidad', 'Twining', 'U St/Pleasant Plains', 'Union Station', 'Washington Highlands', 'Bloomingdale', 'Woodley Park', 'Woodridge', 'Brentwood', 'Brightwood', 'Brightwood Park', 'Capitol Hill']
NON_RESIDENTIAL_HOODS = ['National Mall','DC Medical Center','Stadium Armory','Naval Station & Air Force']

def load_data():
    dccovid = pd.read_csv(r'data.csv')
    dccovid.index = pd.to_datetime(dccovid['Date'])
    dccovid['Unknown Ward Tests'] = pd.to_numeric(dccovid['Unknown Ward Tests'])
    hood_demos = pd.read_csv(r'nhood_demographics.csv',index_col='Neighborhood Name')
    ward_demos = pd.read_csv(r'ward_demographics.csv', index_col='Ward')
    snf_cases = pd.read_csv(r'snf_cases.csv')
    snf_keys = pd.read_csv(r'snf_keys.csv')
    al_cases = pd.read_csv(r'assisted_living_cases.csv')
    al_keys = pd.read_csv(r'assisted_living_keys.csv')
    school_info = pd.read_csv(r'schools.csv')
    school_cases = pd.read_csv(r'school_cases.csv')
    vax = pd.read_csv(r'vaccinations.csv')

    with urlopen('https://opendata.arcgis.com/datasets/de63a68eb7674548ae0ac01867123f7e_13.geojson') as response:
        hood_map = json.load(response)

    return dccovid, hood_demos, ward_demos, hood_map, snf_cases, snf_keys, al_cases, al_keys,school_info, school_cases, vax

# Load data into the dataframe.
data, hood_demos, ward_demos, hood_map, snf_cases, snf_keys, al_cases, al_keys, school_info, school_cases, vax  = load_data()
# Define positive tests in DC
dc_pos = data['Positives'].diff().rolling(7).sum().divide(data['Tested'].diff().rolling(7).sum())
# dc_pos = data.[:,'Ward 1':'Unknown Ward'].diff().rolling('7D').sum().divide(data.loc[:,'Ward 1 Tests':'Unknown Ward Tests'].diff().rolling('7D').sum())

data['Date'] = pd.to_datetime(data['Date'])
vax['Date'] = pd.to_datetime(vax['Date'])
vax.index = vax['Date']


bar_display = data.loc[data['Averaged'] != True,['Date','Positives','Deaths','Tested']]

# Cases
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=bar_display['Date'],
    y=bar_display['Positives'].diff(),
    name='New Cases',
    marker_color='rgb(158,202,225)'
))

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Positives'].diff().rolling(7).mean(),
    name='7-Day Average',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.add_annotation(
            x = '2020-12-26',
            y = 492,
            xanchor = 'right',
            text="Includes Cases<br>from 12/25",
            showarrow=True,
            arrowhead=1,
)
fig.update_layout(
    title=dict(
        text='New Cases'
    ),
    xaxis=dict(
        showspikes = False,
    ),
)
fig.write_html("./chart_htmls/cases.html")

# Deaths
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=bar_display['Date'],
    y=bar_display['Deaths'].diff(),
    name='New Deaths',
    marker_color='maroon'
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Deaths'].diff().rolling(7).mean(),
    name='7-Day Average',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.add_annotation(
            x = '2020-12-26',
            y = 6,
            xanchor = 'right',
            text="Includes Deaths<br>from 12/25",
            showarrow=True,
            arrowhead=1)

fig.update_layout(
    title=dict(
        text='New Deaths'
    ),
    yaxis=dict(
        rangemode="nonnegative"
    ),
    xaxis=dict(
        showspikes = False,
    ),
)
fig.write_html("./chart_htmls/deaths.html")

# Tests
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=bar_display['Date'],
    y=bar_display['Tested'].diff(),
    name='New Tests',
    marker_color='orange'
    )
)
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Tested'].diff().rolling(7).mean(),
    name='7-Day Average',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.add_annotation(
            x = '2020-12-26',
            y = 18440,
            xanchor = 'right',
            text="Includes Tests<br>from 12/25",
            showarrow=True,
            arrowhead=1)

fig.update_layout(
    title=dict(
        text='New Tests'
    ),
    xaxis=dict(
        showspikes = False,
    ),
)
fig.write_html("./chart_htmls/tests.html")

fig = go.Figure(layout=layout)
fig.add_trace(go.Scatter(
    x = data.index,
    y = data['Positives'].diff().divide(data['Tested'].diff()),
    mode='markers',
    marker=dict(
        color = 'orange'
    ),
    name = 'Single-Day',
    hovertemplate='New Tests: '+ data['Tested'].diff().map('{:,.0f}'.format)+
                  '<br>New Cases: '+ data['Positives'].diff().map('{:.0f}'.format)+
                  '<br>%{y:.1%} Positive'
))
fig.add_trace(go.Scatter(
    x = data.index,
    y = dc_pos,
    mode='lines',
    line=dict(
        color = 'black'
    ),
    hovertemplate='%{y:.1%}',
    name = '7-Day'
))
fig.update_layout(
    legend=dict(
        x=.8,
        y=.99,
    ),
    yaxis=dict(
        tickformat=".0%",
        range=[0,.4]
    ),
    xaxis=dict(
        showspikes=False
    ),
    title=dict(
        text = "Daily and Weekly Positivity Rate"
    )
    
)
fig.write_html("./chart_htmls/positivity.html")


########### Demographic Statistics ################
# Ages
fig = go.Figure(layout=layout)
ages_data = data.loc[:,'age0-18':'age81'].diff().rolling(7).mean()
for i in range(len(AGES_LIST)):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ages_data.iloc[:,i],
        name=AGES_LIST[i],
        mode='lines',
        line=dict(
            color=G10[i],
            )
        )
    )
fig.update_layout(
    title=dict(
        text='New Cases by Age, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/ages.html")

# New Cases Makeup
age_daily_s = ages_data*7
age_daily_s_pct = age_daily_s.divide(age_daily_s.sum(axis=1),axis=0)
fig = go.Figure(layout=layout)
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=age_daily_s_pct.iloc[:,i],
        mode='lines',
        stackgroup='one',
        name=AGES_LIST[i],
        line=dict(
            color=G10[i],
            width=0
        )
    ))
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(range=['2020-03-16',data.index[-1]])
fig.update_layout(
    title=dict(
        text='Breakdown of New Cases by Age, 7-Day Average'
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/ages_makeup.html")


# Ages of Cases
fig = go.Figure(
    data=[go.Pie(
        labels=AGES_LIST,
        values=data.loc[data.index[-1],'age0-18':'age81'],
        marker=dict(
            colors=G10
        )
    )],
    layout=layout
)
fig.update_layout(
    title=dict(
        text='Case Breakdown by Age'
    ),
    legend=dict(
        y=.5,
        x=1,
        bgcolor='rgba(0,0,0,0)',
        yanchor='middle'
    )
)
fig.write_html("./chart_htmls/ages_cases_pie.html")

# Ages of Deaths
fig = go.Figure(
    data=[go.Pie(
        labels=data.columns[186:194],
        values=data.loc[data.index[-1],'0-19':'80+'],
        marker=dict(
            colors=G10
        )
    )],
    layout=layout
)
fig.update_layout(
    title=dict(
        text='Death Breakdown by Age'
    ),
    legend=dict(
        y=.5,
        x=1,
        bgcolor='rgba(0,0,0,0)',
        yanchor='middle'
    )
)
fig.write_html("./chart_htmls/ages_deaths_pie.html")

#New age chart
age_demos = pd.read_csv('age_demos.csv',index_col=0).drop(index=['25-34 Cases','35-44 Cases','45-54 Cases','55-64 Cases','65-74 Cases','75+ Cases'])
age_data = data.loc[:,'0-4 Cases':'75+ Cases'].diff().rolling(7).mean()
age_data['25-44 Cases'] = age_data['25-34 Cases']+age_data['35-44 Cases']
age_data['45-64 Cases'] = age_data['45-54 Cases']+age_data['55-64 Cases']
age_data['65+ Cases'] = age_data['65-74 Cases']+age_data['75+ Cases']
age_data = age_data.drop(columns=['25-34 Cases','35-44 Cases','45-54 Cases','55-64 Cases','65-74 Cases','75+ Cases'])
age_data_pc = age_data.divide(age_demos['Population (2019 ACS)'])*10000

fig = go.Figure(layout=layout)
for i in range(len(age_data.columns)):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=age_data.iloc[:,i],
        name=AGES_LIST_CENSUS[i],
        mode='lines',
        line=dict(
            color=G10[i],
            width=2
        ),
    ))

fig.update_layout(
    title=dict(
        text='New Cases by Age, 7-Day Average'
   ),
    yaxis=dict(
        tickformat=".1f"
    ),
    xaxis=dict(
        ticks='outside',
    ),
    legend=dict(
        y=.5,
        x=1,
        yanchor='middle',
        xanchor='left'
    )
)
fig.write_html("./chart_htmls/ages_census.html")



fig = go.Figure(layout=layout)
# ages_data = data.loc[:,'0-4 Cases':'75+ Cases'].diff().rolling(7).mean()
for i in range(len(age_data.columns)):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=age_data_pc.iloc[:,i],
        name=AGES_LIST_CENSUS[i],
        mode='lines',
        line=dict(
            color=G10[i],
            width=2
        ),
#         stackgroup='one',
    ))

fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Positives'].diff().rolling(7).mean().divide(ward_demos.loc['All Wards','Population (2019 ACS)'])*10000,
    mode='lines',
    line=dict(
        color='black',
        width=3
    ),
    name='District-Wide'
))
fig.update_layout(
    title=dict(
        text='New Cases per 10,000 Residents by Age, 7-Day Average'
    ),
    yaxis=dict(
       tickformat=".1f"
    ),
    xaxis=dict(
        ticks='outside',
    ),
    legend=dict(
        y=.5,
        x=1,
        yanchor='middle',
        xanchor='left'
    )
)
fig.write_html("./chart_htmls/ages_census_pc.html")


# Race of Cases
fig = go.Figure(
    data=[go.Pie(
        labels=data.columns[47:53],
        values=data.iloc[-1,47:53],
        marker=dict(
            colors=ANTIQUE
        )
    )],
    layout=layout
)
fig.update_layout(
    title=dict(
        text='Case Breakdown by Race'
    ),
    legend=dict(
        y=-.2,
        x=0,
        bgcolor='rgba(0,0,0,0)'

    )
)
fig.write_html("./chart_htmls/races_cases_pie.html")
# Race of Deaths
fig = go.Figure(
    data=[go.Pie(
        labels=data.columns[37:42],
        values=data.iloc[-1,37:42],
        marker=dict(
            colors=ANTIQUE_ALT
        )
    )],
    layout=layout
)
fig.update_layout(
    title=dict(
        text='Death Breakdown by Race/Ethnicity'
    ),
    legend=dict(
        y=-.2,
        x=.0,
        bgcolor='rgba(0,0,0,0)'
    )
)
fig.write_html("./chart_htmls/races_deaths_pie.html")

# Race Breakdown

# race_cum_pct = data.loc['2020-04-05':,RACE_LIST].divide(data.loc['2020-04-05':,'Positives'],axis=0)
race_daily_s =  data.loc['2020-04-05':,'White':'Two or More Races'].diff().rolling(7).sum()
race_daily_s_pct = race_daily_s.divide(race_daily_s.sum(axis=1),axis=0)
fig = go.Figure(layout=layout)
for i in range(6):
    fig.add_trace(go.Scatter(
        x=data.loc['2020-04-05':,'Date'],
        y=race_daily_s_pct.iloc[:,i],
        mode='lines',
        stackgroup='one',
        name=RACE_LIST[i],
        line=dict(
            color=ANTIQUE[i],
            width=0
        )
    ))
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(range=['2020-03-16',data.index[-1]])
fig.update_layout(
    title=dict(
        text='Breakdown of New Cases by Race, 7-Day Average'
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/race_breakdown.html")

########### Wards #####################
# Ward Cases
fig = go.Figure(layout=layout)
ward_avg = data.loc[:,'Ward 1':'Ward 8'].diff().rolling(7).mean()
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ward_avg[WARD_LIST[i]],
        name=WARD_LIST[i],
        line=dict(
            color=PASTELS[i]
        )
    ))
fig.update_layout(
    title=dict(
        text='New Cases by Ward, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/wards.html")

#Ward Breakdown
ward_daily_s = data.loc[:,WARD_LIST].diff().rolling(7).sum()
ward_daily_s_pct = ward_daily_s.divide(ward_daily_s.sum(axis=1),axis=0)
fig = go.Figure(layout=layout)
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ward_daily_s_pct.iloc[:,i],
        mode='lines',
        stackgroup='one',
        name=WARD_LIST[i],
        line=dict(color=PASTELS[i],width=0)
    ))
fig.update_yaxes(
    tickformat=".0%"
)
fig.update_xaxes(
    range=['2020-03-16',data.index[-1]]
)
fig.update_layout(
    title=dict(
        text='Breakdown of New Cases by Ward, 7-Day Average'
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/wards_breakdown.html")

# Per Capita Ward Cases
fig = go.Figure(layout=layout)
ward_avg_pc = np.divide(ward_avg,ward_demos.loc[WARD_LIST,'Population (2019 ACS)'])*10000
dc_avg_pc = np.divide(data['Positives'].diff().rolling(7).mean(), ward_demos.loc['All Wards','Population (2019 ACS)'])*10000
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ward_avg_pc[WARD_LIST[i]],
        name=WARD_LIST[i],
        mode='lines',
        line=dict(
            color=PASTELS[i]
        )
    ))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=dc_avg_pc,
    name='District-Wide',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.update_layout(
    title=dict(
        text='New Cases Per 10,000 Residents, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/wards_pc.html")

# Ward Positivity
fig = go.Figure(layout=layout)
positivity = np.divide(data.loc['2020-06-01':,'Ward 1':'Ward 8'].diff().rolling(7).sum(),data.loc['2020-06-01':,'Ward 1 Tests':'Ward 8 Tests'].diff().rolling(7).sum())
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data.loc['2020-06-01':,'Date'],
        y=positivity.iloc[:,i],
        name=WARD_LIST[i],
        mode='lines',
        line=dict(
            color=PASTELS[i]
        )
    ))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=dc_pos,
    name='District-Wide',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.update_layout(
    title=dict(
        text='Positivity by Ward, 7-Day Window'
    ),
    yaxis=dict(
        tickformat=".1%"
    ),
    legend=dict(
        y=0.75,
        x=1
))
fig.write_html("./chart_htmls/wards_positivity.html")

# Ward Deaths
fig = go.Figure(
    data=[go.Bar(
        x=WARD_LIST,
        y=data.iloc[-1,58:66],
        name='Deaths',
        marker_color=PASTELS[0:8] # marker color can be a single color value or an iterable
    )],
    layout = layout
)
fig.update_layout(
    title=dict(
        text='Total Deaths'
    )
)

# Ward Deaths Per Capita
ward_deaths = data.iloc[-1,58:66]
ward_deaths.index = WARD_LIST
fig = go.Figure(
    data=[go.Bar(
        x=WARD_LIST,
        y=ward_deaths.divide(ward_demos.loc[WARD_LIST,'Population (2019 ACS)'])*10000,
        name='Deaths',
        marker_color=PASTELS[0:8] # marker color can be a single color value or an iterable
    )],
    layout = layout)
fig.update_layout(
    title=dict(
        text='Deaths per 10,000 Residents'
    ),
    yaxis=dict(
        tickformat=".1f"
    )
)

# Ward Test Rates
fig = go.Figure(layout=layout)
ward_test_pc = np.divide(data.loc['2020-06-01':,'Ward 1 Tests':'Ward 8 Tests'].diff().rolling(7).mean(),ward_demos.loc[WARD_LIST,'Population (2019 ACS)'])*10000
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data.loc['2020-06-01':,'Date'],
        y=ward_test_pc.iloc[:,i],name=WARD_LIST[i],
        mode='lines',
        line=dict(
            color=PASTELS[i]
        )
    ))
dc_tests = np.divide(data['Tested'].diff().rolling(7).mean(), ward_demos.loc['All Wards','Population (2019 ACS)'])*10000
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=dc_tests,
    name='District-Wide',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.update_layout(
    title=dict(
        text='Tests Per 10,000 Residents, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/wards_tests.html")


#Ward Breakdown
ward_daily_s_tests = data.loc['2020-06-01':,'Ward 1 Tests':'Ward 8 Tests'].diff().rolling(7).sum()
ward_daily_s_tests_pct = ward_daily_s_tests.divide(ward_daily_s_tests.sum(axis=1),axis=0)
fig = go.Figure(layout=layout)
for i in range(8):
    fig.add_trace(go.Scatter(
        x=data.loc['2020-06-01':,'Date'],
        y=ward_daily_s_tests_pct.iloc[:,i],
        mode='lines',
        stackgroup='one',
        name=WARD_LIST[i],
        line=dict(
            color=PASTELS[i],
            width=0
        )
    ))
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(range=['2020-03-16',data.index[-1]])
fig.update_layout(
    title=dict(
        text='Breakdown of New Tests by Ward, 7-Day Average'
    ),
    legend=dict(
        y=0.75,
        x=1
    )
)
fig.write_html("./chart_htmls/wards_tests_breakdown.html")

fig = go.Figure(layout=layout)
ward_daily_s_tests_pct.columns = WARD_LIST
ward_daily_s_pct
ward_demos['makeup'] = ward_demos.loc[WARD_LIST,'Population (2019 ACS)']

############## Hospital Statistics ####################
# COVID Patients Only
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['COVID Patients'],
    name='Hospitalized',
    marker_color=DARK2[0]
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['COVID ICU Patients'],
    name='In ICU',
    marker_color=DARK2[1]
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['COVID Ventilators'],
    name='On Ventilator',
    marker_color=DARK2[2]
))
fig.update_layout(
    title=dict(
        text='COVID Patients'
    ),
    barmode='overlay',
    legend=dict(
        y=-.1,
        x=.5,
        orientation='h',
        xanchor='center'
    )
)
fig.write_html("./chart_htmls/patients.html")

# Hospitalized
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Total Patients'],
    name='Total Patients',
    marker_color=PASTEL2[0],
    hovertemplate =
        'Total: %{y}'+'<br>'+
        '% Beds in Use (Pre-Surge): %{text:.1f}%',
    text = data['Total Patients']/2487*100
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['COVID Patients'],
    name='COVID Patients',
    marker_color=DARK2[0],
    hovertemplate =
        'Total: %{y}'+'<br>'+
        '% of All Patients: %{text:.1f}%',
    text = data['COVID Patients'].divide(data['Total Patients'])*100
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=np.full((data['Date'].size), 2487, dtype=int),
    name='Total Hospital Beds',
    mode='lines',
    marker_color='black'
))
fig.update_layout(
    title=dict(
        text='All Hospitalized'
    ),
    barmode='overlay',
    legend=dict(
        y=-.1,
        x=.5,
        orientation='h',
        xanchor='center'
    )
)
fig.write_html("./chart_htmls/patients_hospitalized.html")
# In ICU
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Total ICU Beds']-data['ICU Beds Available'],
    name='Total Patients in ICU',
    marker_color=PASTEL2[1],
    hovertemplate =
        'Total: %{y}'+'<br>'+
        '% ICU Beds in Use (Pre-Surge): %{text:.1f}%',
    text = (data['Total ICU Beds']-data['ICU Beds Available']).divide(data['Total ICU Beds'])*100
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['COVID ICU Patients'],
    name='COVID Patients in ICU',
    marker_color=DARK2[1],
    hovertemplate =
        'Total: %{y}'+'<br>'+
        '% of All ICU Patients: %{text:.1f}%',
    text = data['COVID ICU Patients'].divide(data['Total ICU Beds']-data['ICU Beds Available'])*100
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Total ICU Beds'],
    mode='lines',
    name='Total ICU Beds',
    marker_color='black'
))
fig.update_layout(
    title=dict(
        text='All ICU Patients'
    ),
    barmode='overlay',
    legend=dict(
        y=-.1,
        x=.5,
        orientation='h',
        xanchor='center'
    )
)
fig.write_html("./chart_htmls/patients_icu.html")
# Ventilated
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['In-Use Ventilators'],
    name='Total Patients on Ventilators',
    marker_color=PASTEL2[2],
    hovertemplate =
        'Total: %{y}'+'<br>'+
        '% Ventilators in Use (Pre-Surge): %{text:.1f}%',
    text = data['In-Use Ventilators'].divide(data['Total Ventilators'])*100
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['COVID Ventilators'],
    name='COVID Patients on Ventilators',
    marker_color=DARK2[2],
    hovertemplate =
        'Total: %{y}'+'<br>'+
        '% of All Ventilated : %{text:.1f}%',
    text = data['COVID Ventilators'].divide(data['In-Use Ventilators'])*100
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Total Ventilators'],
    name='Total Ventilators',
    mode='lines',
    marker_color='black'
))
fig.update_layout(
    title=dict(
        text='All Patients on Ventilators'
    ),
    barmode='overlay',
    legend=dict(
        y=-.1,
        x=.5,
        orientation='h',
        xanchor='center'
    )
)
fig.write_html("./chart_htmls/patients_ventilator.html")

############# MAPS #################
hood_data = data.loc[:,'16th St Heights':'Capitol Hill'].diff().rolling(7).mean()
hood_data_pc = hood_data.divide(hood_demos['Population (2019 ACS)'])*10000
rolling_cases = data.loc[:,'16th St Heights':'Capitol Hill'].diff().rolling(7).sum()
rolling_tests = data.loc[:,'16th St Heights Tests':'Capitol Hill Tests'].diff().rolling(7).sum()
rolling_tests.columns = rolling_cases.columns
hood_positive = np.divide(rolling_cases,rolling_tests)
pos_this_week = hood_positive.iloc[-1,:].sort_values()
pos_this_week = pd.concat([pos_this_week,rolling_cases.iloc[-1,:],rolling_tests.iloc[-1,:],hood_demos['Population (2019 ACS)'],hood_demos['OBJECTID']],axis=1)
pos_this_week.columns = ['Positivity This Week','Positives This Week','Tests This Week','Population','OBJECTID']
pos_this_week['Positives This Week Per 10k'] = pos_this_week['Positives This Week'].divide(pos_this_week['Population']) * 10000
pos_this_week['Neighborhood'] = pos_this_week.index
pos_this_week.to_html('nhoods_this_week.html')
map_list = ['Positives This Week Per 10k','Positives This Week','Positivity This Week']
for plotdata in map_list:
    if(plotdata=='Positives This Week Per 10k'):
        no_nat_mall = pos_this_week.drop(index=['National Mall','DC Medical Center'])
        range_color = (0,35)
        filename = "./chart_htmls/nhood_map_pc.html"
        tickformat = ".0f"
        titletext = 'Positives This<br>Week Per 10k'
    elif(plotdata=='Positives This Week'):
        range_color = (0,70)
        filename = "./chart_htmls/nhood_map_cases.html"
        tickformat = ".0f"
        titletext = 'Positives This Week'
    elif(plotdata=='Positivity This Week'):
        range_color = (0,.10)
        filename = "./chart_htmls/nhood_map_positivity.html"
        tickformat = "%.0f"
        titletext = 'Postivity This Week'

    fig = px.choropleth_mapbox(
        pos_this_week,
        geojson=hood_map,
        color=plotdata,
        locations="OBJECTID",
        featureidkey="properties.OBJECTID",
        center={"lat": 38.91,
                "lon": -77.03
                },
        color_continuous_scale="Hot_r",
        range_color=range_color,
        opacity=0.5,
        mapbox_style="carto-positron",
        zoom=10,
        hover_name='Neighborhood',
        hover_data={'Neighborhood':False,
                    'OBJECTID':False,
                    'Positives This Week':True,
                    'Tests This Week':True,
                    'Population':True,
                    'Positivity This Week':':.2%',
                    'Positives This Week Per 10k':':.1f'
                    }
       )
    fig.update_layout(margin={
        "r":0,
        "t":0,
        "l":0,
        "b":0
        },
        coloraxis=dict(
            colorbar = dict(
                tickformat = tickformat,
                ticksuffix = '+',
                showticksuffix = 'last',
                title = dict(
                    text = titletext
                )

            )

        )
    )
    fig.write_html(filename)



############## NEIGHBORHOODS ####################
# to_plot = hood_data_pc.drop(columns=['National Mall'])
# to_plot = to_plot.sort_values(by=to_plot.index[-1],axis=1,ascending=False)
#
#
# nrows = 6
# ncols = 9
#
# fig = make_subplots(rows=nrows, cols=ncols, shared_xaxes=True, shared_yaxes=True,subplot_titles=to_plot.columns)
# index = 0
# row = 1
# col = 1
# for nhood in to_plot.columns:
#     fig.add_trace(go.Scatter(x=to_plot.index,y=to_plot[nhood],line=dict(color='black'),name=nhood),row=row,col=col)
#
#     index += 1
#     if col == ncols:
#         row+=1
#         col = 0
#     col+=1
#
# fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
#     hovermode='x',
#     font=dict(family='Arial'),
#     title = dict(x=0.5,text='7-Day Average Cases per 10,000 Residents in the last 14 Days')
# )
#
# fig.update_layout(showlegend=False)
# fig.update_xaxes(range=[to_plot.index[-15],to_plot.index[-1]],
#         showspikes=True,
#         showticklabels = False,
#         spikedash = 'solid',
#         spikecolor = 'black',
#         spikemode  = 'across',
#         spikesnap = 'cursor')
# fig.update_yaxes(rangemode = 'tozero',showticklabels = False,
#         showgrid=False,
#         range=[0,6.5])
# for i in fig['layout']['annotations']:
#     i['font'] = dict(size=9)
# fig.write_html('chart_htmls/nhood_matrix_pc.html')

# Neighborhood cases
HOOD_LIST_SORTED = sorted(HOOD_LIST)
fig = go.Figure(layout=layout)
for i in range(51):
    if HOOD_LIST_SORTED[i] in NON_RESIDENTIAL_HOODS:
        continue
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=hood_data[HOOD_LIST_SORTED[i]],
        mode='lines',
        line=dict(
            color='lightgrey',
            width=1
        ),
        hoverinfo='skip',
        showlegend=False
    ))
for i in range(51):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=hood_data[HOOD_LIST_SORTED[i]],
        name=HOOD_LIST_SORTED[i],
        mode='lines',
        visible='legendonly',
        line=dict(
            color=LIGHT24[i%24]
        )
    ))
fig.update_yaxes(rangemode="nonnegative")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(
    title=dict(
        text='New Positives, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-.1,
        xanchor="center",
        x=.5,
        bgcolor='rgba(0,0,0,0)'
    )
)
fig.write_html('chart_htmls/nhood_cases.html')


# Neighborhoods Per capita
fig = go.Figure(layout=layout)
for i in range(51):
    if HOOD_LIST_SORTED[i] in NON_RESIDENTIAL_HOODS:
        continue
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=hood_data_pc[HOOD_LIST_SORTED[i]].drop(columns=['National Mall','DC Medical Center']),
        mode='lines',
        line=dict(
            color='lightgrey',
            width=1
        ),
        hoverinfo='skip',
        showlegend=False
    ))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=dc_avg_pc,
    name='District-Wide',
    mode='lines',
    line=dict(
        color='black',
        width=3.0
    )
))
for i in range(51):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=hood_data_pc[HOOD_LIST_SORTED[i]],
        mode='lines',
        name=HOOD_LIST_SORTED[i],
        visible='legendonly',
        line=dict(
            color=LIGHT24[i%24]
        )
    ))
fig.update_yaxes(
    rangemode="nonnegative",
    range=[0,10]
)
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(
    title=dict(
        text='New Positives per 10,000 Residents, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-.1,
        xanchor="center",
        x=.5,
        bgcolor='rgba(0,0,0,0)'

    )
)
fig.write_html('chart_htmls/nhood_pc.html')

# Neighborhoods Tests Per capita
ntests = data.loc[:,'16th St Heights Tests':'Capitol Hill Tests'].diff().rolling(7).mean()
ntests.columns = HOOD_LIST
ntests_pc = ntests.divide(hood_demos['Population (2019 ACS)'])*10000
fig = go.Figure(layout=layout)
for i in range(51):
    if HOOD_LIST_SORTED[i] in NON_RESIDENTIAL_HOODS:
        continue
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ntests_pc[HOOD_LIST_SORTED[i]].drop(columns=['National Mall','DC Medical Center']),
        line=dict(
            color='lightgrey',
            width=1
        ),
        mode='lines',
        hoverinfo='skip',
        showlegend=False
    ))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=dc_tests,
    name='District-Wide',
    mode='lines',
    line=dict(
        color='black',
        width=3.0
    )
))
for i in range(51):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ntests_pc[HOOD_LIST_SORTED[i]],
        name=HOOD_LIST_SORTED[i],
        mode='lines',
        visible='legendonly',
        line=dict(
            color=LIGHT24[i%24]
        )
    ))
fig.update_yaxes(
    rangemode="nonnegative",
    range=[0,450]
)
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(
    title=dict(
        text='New Tests per 10,000 Residents, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-.1,
        xanchor="center",
        x=.5,
        bgcolor='rgba(0,0,0,0)'
    )
)
fig.write_html('chart_htmls/nhood_tests_pc.html')

# Neighborhood tests
fig = go.Figure(layout=layout)
for i in range(51):
    if HOOD_LIST_SORTED[i] in NON_RESIDENTIAL_HOODS:
        continue
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ntests[HOOD_LIST_SORTED[i]],
        mode='lines',
        line=dict(
            color='lightgrey',
            width=1
        ),
        hoverinfo='skip',
        showlegend=False
    ))
for i in range(51):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=ntests[HOOD_LIST_SORTED[i]],
        name=HOOD_LIST_SORTED[i],
        visible='legendonly',
        mode='lines',
        line=dict(
            color=LIGHT24[i%24]
        )
    ))
fig.update_yaxes(rangemode="nonnegative")
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(
    title=dict(
        text='New Tests, 7-Day Average'
    ),
    yaxis=dict(
        tickformat=".1f"
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-.1,
        xanchor="center",
        x=.5,
        bgcolor='rgba(0,0,0,0)'
    )
)
fig.write_html('chart_htmls/nhood_tests.html')

# Neighborhood Test positivity
fig = go.Figure(layout=layout)
hood_positive = np.divide(rolling_cases,rolling_tests)
for i in range(51):
    if HOOD_LIST_SORTED[i] in NON_RESIDENTIAL_HOODS:
        continue
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=hood_positive[HOOD_LIST_SORTED[i]],
        line=dict(
            color='lightgrey',
            width=1
        ),
        mode='lines',
        hoverinfo='skip',
        showlegend=False
    ))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=dc_pos,
    mode='lines',
    name="District-Wide",
    line=dict(
        color='black',
        width=3.0
    )
))
for i in range(51):
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=hood_positive[HOOD_LIST_SORTED[i]],
        mode='lines',
        name=HOOD_LIST_SORTED[i],
        visible='legendonly',
        line=dict(
            color=LIGHT24[i%24]
        )
    ))
fig.update_yaxes(
    rangemode="nonnegative",
    range=[0,.15],
    tickformat=".1%"
)
fig.update_xaxes(range=['2020-05-13',data.index[-1]])
fig.update_layout(
    title=dict(
        text='Test Positivity, 7-Day Window'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-.1,
        xanchor="center",
        x=.5,
        bgcolor='rgba(0,0,0,0)'
    )
)
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
to_plot = hood_data_pc.drop(columns=['National Mall','DC Medical Center'])


nrows = 11
ncols = 11

vmin, vmax = to_plot.iloc[-1,:].min(), to_plot.iloc[-1,:].max()


norm = matplotlib.colors.Normalize(vmin=0, vmax=5)
cmap = matplotlib.cm.get_cmap('YlOrRd') # yellow to orange to red

fig = make_subplots(
    rows=nrows,
    cols=ncols,
    shared_xaxes=True,
    shared_yaxes=True,
    vertical_spacing=0.005,
    horizontal_spacing=0.005
)
ymax = np.max(np.max(to_plot.iloc[-15:-1,:]))*1.1


for nhood in hood_data_pc.columns:
    color = 'rgba' + str(cmap(norm(np.round(hood_data_pc[nhood][-1]),4)))[:]
    fig.add_trace(go.Scatter(x=[hood_data_pc.index[-15],hood_data_pc.index[-1]],y= [ymax*1.5,ymax*1.5],fill='tozeroy',fillcolor=color,hoverinfo='skip'),row=diamond_dict[nhood][0],col=diamond_dict[nhood][1])
    if nhood != 'National Mall':
        fig.add_trace(
            go.Scatter(
                x=hood_data_pc.index,
                y=hood_data_pc[nhood],
                line=dict(
                    color='black'
                ),
                name=nhood,
                hovertemplate="%{y:.1f}"
                ),
            row=diamond_dict[nhood][0],
            col=diamond_dict[nhood][1]
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=hood_data_pc.index,
                y=hood_data_pc[nhood],
                line=dict(
                    color='black'
                ),
                name=nhood,
                hovertemplate="%{y:.1f} (May be anomalous)"
            ),
            row=diamond_dict[nhood][0],
            col=diamond_dict[nhood][1]
        )


fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    font=dict(
        family='Arial'
    ),
    title = dict(
        x=0.5,
        text='7-Day Average Cases per 10,000 Residents (Last 2 Weeks)'
    ),
    showlegend=False,
    width=750,
    height=750
)
fig.update_xaxes(
        range=[to_plot.index[-15],to_plot.index[-1]],
        showspikes=False,
        showticklabels = False,
        spikedash = 'solid',
        spikecolor = 'black',
        spikemode  = 'across',
        spikesnap = 'cursor',
        fixedrange = True
)

fig.update_yaxes(
    rangemode = 'tozero',
    showticklabels = False,
    showgrid=False,
    range=[0,ymax],
    tickformat="0.1f",
    fixedrange = True
)
fig.write_image('chart_htmls/nhood_diamond_pc.png')
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)'
)
fig.write_html('chart_htmls/nhood_diamond_pc.html')


########## SCHOOL CASES ###########
school_info.index = school_info['NAME']
school_info = school_info[school_info['School ID'].notna()]
school_info['Students Scheduled for In-Person Programming in Term 3 (As of 2.4.21)'] = school_info['Students Scheduled for In-Person Programming in Term 3 (As of 2.4.21)'].astype('Int64')
school_info['TOTAL_STUD']= school_info['TOTAL_STUD'].astype('Int64')

school_info =  school_info.join(school_cases['School'].value_counts().rename('Number of Notifications'))
school_info['Number of Notifications']= school_info['Number of Notifications'].fillna(0).astype(int)

school_cases = school_cases.join(school_info,on='School',how='right')


school_cases['Resume Date'] = pd.to_datetime(school_cases['Resume Date'])
school_cases['Most Recent Day of Case'] = pd.to_datetime(school_cases['Most Recent Day of Case'])
school_cases['Day Announced'] = pd.to_datetime(school_cases['Day Announced'])

cases_closed = school_cases.loc[school_cases['Resume Date']>np.datetime64('today'),:]
cases_not_closed_bool = ((school_cases['Most Recent Day of Case']-np.datetime64('today'))>np.timedelta64(-14, 'D'))&(school_cases['Resume Date'].isna())

cases_not_closed = school_cases.loc[cases_not_closed_bool,:]

open_schools_bool = school_info['NAME'].isin(cases_not_closed['School'])|school_info['NAME'].isin(cases_closed['School'])
open_schools = school_info.loc[~open_schools_bool,:]



fig = go.Figure()

fig = go.Figure()


# Open Schools
fig.add_trace(go.Scattermapbox(
    lat=open_schools['LATITUDE'],
    lon=open_schools['LONGITUDE'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        color='green',
    ),
    text='<b>'+open_schools['NAME']+'</b>'+
         '<br>Total Case Notifications: '+open_schools['Number of Notifications'].astype(str)+
         '<br>'+open_schools['Students Scheduled for In-Person Programming in Term 3 (As of 2.4.21)'].astype(str)+'/'+open_schools['TOTAL_STUD'].astype(str)+
         ' Students Scheduled for<br>In-Person Learning'+
         '<br>Open '+open_schools['Days per Week'],
    hoverinfo='text',
    name = 'Open DCPS Schools'

))
# Open Schools, Cases in the last 2 weeks
fig.add_trace(go.Scattermapbox(
    lat=cases_not_closed['LATITUDE'],
    lon=cases_not_closed['LONGITUDE'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        color='orange',
    ),
    text='<b>'+cases_not_closed['NAME']+
      '</b><br>Case Last Reported on Campus: '+cases_not_closed['Most Recent Day of Case'].apply(lambda x: x.strftime('%m/%d'))+
      '<br>Total Case Notifications: '+cases_not_closed['Number of Notifications'].astype(str)+
      '<br>'+cases_not_closed['Students Scheduled for In-Person Programming in Term 3 (As of 2.4.21)'].astype(str)+'/'+cases_not_closed['TOTAL_STUD'].astype(str)+
      ' Students Scheduled for<br>In-Person Learning'+
      '<br>Open '+cases_not_closed['Days per Week'],
    hoverinfo='text',
    name = 'Case Reported on Campus in Last 2 Weeks'

))

# Closed Schools
fig.add_trace(go.Scattermapbox(
    lat=cases_closed['LATITUDE'],
    lon=cases_closed['LONGITUDE'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        color='red',
    ),
    text='<b>'+cases_closed['NAME']+
         '</b><br>Case Last Reported on Campus: '+cases_closed['Most Recent Day of Case'].apply(lambda x: x.strftime('%m/%d'))+
         '<br>Total Case Notifications: '+cases_closed['Number of Notifications'].astype(str)+
         '<br>'+cases_closed['Students Scheduled for In-Person Programming in Term 3 (As of 2.4.21)'].astype(str)+'/'+cases_closed['TOTAL_STUD'].astype(str)+
         ' Students Scheduled for<br>In-Person Learning'+
         '<br>Open '+cases_closed['Days per Week'],
    hoverinfo='text',
    name = 'Classroom Transition to Online Learning Reported Due to COVID-19'
))

fig.update_layout(
    title='DCPS Map',
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=open(".mapboxtoken").read(),
        center=dict(
            lat=38.8977,
            lon=-77.0365
        ),
        bearing=0,
        pitch=0,
        zoom=9.5,
        style='light',
    ),
    legend=dict(
            x=0,
            y=0.05,
            bgcolor='rgba(0,0,0,0)'
        ),
    margin={
        "r":0,
        "t":0,
        "l":0,
        "b":0}
)
fig.write_html("./chart_htmls/schools_map.html")

fig = go.Figure(layout=layout)
dcps_cases_nogaps = data.loc[~data['DCPS Personnel'].isna(),'DCPS Personnel':'DCPS Students in Quarrantine']
fig.add_trace(go.Scatter(
    x=dcps_cases_nogaps.index,
    y=dcps_cases_nogaps['DCPS Personnel in Quarrantine'],#+data['DCPS Students in Quarrantine'],
    name = 'Currently Quarrantined<br>DCPS Personnel',
    mode='lines',
    line = dict(
        width = 0.5,
        color = 'rgb(235, 169, 245)'
    ),
    stackgroup='one',
))
fig.add_trace(go.Scatter(
    x=dcps_cases_nogaps.index,
    y=dcps_cases_nogaps['DCPS Students in Quarrantine'],
    name = 'Currently Quarrantined<br>DCPS Students',
    mode='lines',
    line = dict(
        width = 0.5,
        color = 'rgb(188, 211, 247)'
    ),
    stackgroup='one',
))
fig.add_trace(go.Bar(
    x=dcps_cases_nogaps.index,
    y=dcps_cases_nogaps['DCPS Personnel'].diff(),
    name='DCPS Personnel',
    marker_color='rgb(113, 0, 130)'
))
fig.add_trace(go.Bar(
    x=dcps_cases_nogaps.index,
    y=dcps_cases_nogaps['DCPS Students'].diff(),
    name='DCPS Students',
    marker_color='rgb(0, 82, 130)'
))

fig.update_layout(
    title=dict(
        text='New DC Public School Cases'
    ),
    barmode='stack',
    xaxis=dict(
        showspikes = False,
    ),
    legend=dict(
        bgcolor = 'rgba(0,0,0,0)'
    )
)
fig.update_xaxes(range=['2020-11-18',data.index[-1]])

fig.write_html("./chart_htmls/schools_cases.html")


# MPD Positives
mpd_display = data.loc[~data['MPD Positives'].isna(),'MPD Positives']
# Cases
fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=mpd_display.index,
    y=mpd_display.diff(),
    name='New Cases',
    marker_color='rgb(158,202,225)'
))
fig.add_trace(go.Scatter(
    x=mpd_display.index,
    y=mpd_display.diff().rolling('7D').sum()/7,
    name='7-Day Average',
    mode='lines',
    line=dict(
        color = 'black'
    )
))
fig.update_layout(
    title=dict(
        text='New Cases, Metropolitan Police Department'
    ),
    xaxis=dict(
        showspikes = False,
    ),
    legend=dict(
        bgcolor = 'rgba(0,0,0,0)'
    )
)
fig.write_html("./chart_htmls/mpd_cases.html")

# fig = go.Figure(layout=layout)
# fig.add_trace(go.Line(
#     x=vax['Date'],
#     y=vax.loc[:,'Resident First Dose':'N/A Second Dose'].sum(axis=1).rolling('7D').mean(),
#     name='7-Day Average',
#     line=dict(
#         color='black'
#     ),
#     line_shape='hvh'
# ))
# fig.add_trace(go.Bar(
#     x = vax['Date'],
#     y = vax['Resident First Dose'],
#     name = '1st Dose: Residents',
#     marker_color = 'rgb(184, 230, 186)'
# ))
# fig.add_trace(go.Bar(
#     x = vax['Date'],
#     y = vax['Non-resident First Dose'],
#     name = '1st Dose: Non-residents',
#     marker_color = 'rgb(237, 226, 138)'
# ))
# fig.add_trace(go.Bar(
#     x = vax['Date'],
#     y = vax['N/A First Dose'],
#     name = '1st Dose: Unreported',
#     marker_color = 'rgb(191, 191, 191)'
# ))
# fig.add_trace(go.Bar(
#     x = vax['Date'],
#     y = vax['Resident Second Dose'],
#     name = '2nd Dose: Residents',
#     marker_color = 'rgb(44, 191, 50)'
# ))
# fig.add_trace(go.Bar(
#     x = vax['Date'],
#     y = vax['Non-resident Second Dose'],
#     name = '2nd Dose: Non-residents',
#     marker_color = 'rgb(181, 163, 14)'
# ))
# fig.add_trace(go.Bar(
#     x = vax['Date'],
#     y = vax['N/A Second Dose'],
#     name = '2nd Dose: Unreported',
#     marker_color = 'rgb(114, 114, 114)'
# ))
# # fig.add_trace(go.Bar(
# #     x = vax['Date'],
# #     y = vax['N/A Second Dose']+vax['Resident Second Dose']+vax['Non-resident Second Dose'],
# #     name = '2nd Dose Dose: 7-Day Average',
# #     marker_color = 'rgb(114, 114, 114)'
# # ))
#
# fig.update_layout(
#     title=dict(
#         text='Daily Vaccinations'
#     ),
#     barmode='stack',
#     xaxis=dict(
#         showspikes = False,
#     ),
#     legend=dict(
#         orientation="h",
#         yanchor="top",
#         y=-.1,
#         xanchor="center",
#         x=.5,
#         bgcolor = 'rgba(0,0,0,0)'
#     ),
#     hovermode='x unified'
# )
# # fig.update_xaxes(range=['2020-03-07',data.index[-1]])
# fig.write_html('./chart_htmls/vaccinations.html')
#
# fig = go.Figure(layout=layout)
# fig.add_trace(go.Scatter(
#     x=vax['Date'],
#     y=vax['Total Delivered'],
#     fill='tozeroy',
#     mode='lines',
#     line=dict(
#         width=0,
#         color='rgb(199, 214, 214)'
#     ),
#     name='Cumulative Doses Delivered',
#     text=vax.loc[:,'Resident First Dose':'N/A Second Dose'].cumsum().sum(axis=1).divide(vax['Total Delivered'])*100,
#     hovertemplate='Doses Delivered as of<br>6am the Next Morning: %{y:.0f}'+'<br>'+
#                   '% Administered: %{text:.1f}%',
# ))
# fig.add_trace(go.Bar(
#     x=vax['Date'],
#     y=vax['All First Dose'].cumsum(),
#     name='First Doses',
#     marker_color='rgb(63, 204, 202)',
# ))
# fig.add_trace(go.Bar(
#     x=vax['Date'],
#     y=vax['All Second Dose'].cumsum(),
#     name='Second Doses (Approximate)',
#     marker_color='rgb(0, 138, 136)',
# ))
# fig.update_layout(
#     title=dict(
#         text='Cumulative Vaccines Delivered and Administered'
#     ),
#     legend=dict(
#         y=1,
#         x=0,
#         bgcolor='rgba(0,0,0,0)'
#     ),
#     xaxis=dict(
#         showspikes=False,
#     ),
#     barmode='stack',
# )
# fig.write_html('./chart_htmls/vaccines_administered.html')
#
#
#
#
dc_pop = ward_demos.loc['All Wards','Population (DC Data)']

fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=data['Date'],
    y=(data['Positives'].subtract(data['Deaths']+data['Recoveries'],fill_value=0))/dc_pop*100,
    name='Not Cleared from Isolation',
    marker_color='gold',
    hovertemplate =
        '% Not Cleared: %{y:.2f}%'+'<br>'+
        'Total: %{text:.0f}',
    text =data['Positives'].subtract(data['Deaths']+data['Recoveries'],fill_value=0)
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Recoveries']/dc_pop*100,
    name='Cumulative Recoveries',
    marker_color='rgb(158,202,225)',
    hovertemplate =
        '% Cleared from Isolation: %{y:.2f}%'+'<br>'+
        'Total: %{text:.0f}',
    text = data['Recoveries']
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Deaths']/dc_pop*100,
    name='Cumulative Deaths',
    marker_color='maroon',
    hovertemplate =
        '% Died of COVID-19: %{y:.2f}%'+'<br>'+
        'Total: %{text:.0f}',
    text = data['Deaths']
))
fig.add_trace(go.Bar(
    x=vax['Date'],
    y=(vax['Cumulative Partial Doses: Residents']-vax['Cumulative Full Doses: Residents'].fillna(0))/dc_pop*100,
    name='Partially Vaccinated',
    marker_color='rgb(184, 230, 186)',
    hovertemplate =
        '% Partially vaccinated: %{y:.2f}%'+'<br>'+
        'Total: %{text:.0f}',
    text = vax['Cumulative Partial Doses: Residents']-vax['Cumulative Full Doses: Residents'].fillna(0)
))
fig.add_trace(go.Bar(
    x=vax['Date'],
    y=vax['Cumulative Full Doses: Residents']/dc_pop*100,
    name='Fully Vaccinated',
    marker_color='rgb(44, 191, 50)',
    hovertemplate =
        '% Fully vaccinated: %{y:.2f}%'+'<br>'+
        'Total: %{text:.0f}',
    text = vax['Cumulative Full Doses: Residents']
))
fig.add_trace(go.Line(
    x=data['Date'],
    y=np.full((data['Date'].size),100, dtype=int),
    name='Total Population',
    visible='legendonly',
    marker_color='black'
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=np.full((data['Date'].size),70, dtype=int),
    name='Estimate of Herd Immunity Threshold',
    visible='legendonly',
    mode='lines',
    line=dict(
        color='black',
        dash='dash'
    )
))
# fig.add_shape(
#     type='rect',
#     x0=data['Date'][0],
#     y0=70,
#     x1=data['Date'][-1],
#     y1=100,
#     fillcolor='lavender',
#     line=dict(
#         width=0,
#     ),
# )
fig.update_shapes(dict(xref='x', yref='y'))
fig.update_layout(
    title=dict(
        text='Path to Herd Immunity, D.C. Residents'
    ),
    barmode='stack',
    legend=dict(
        orientation="h",
        y=-.1,
        x=0.5,
        xanchor="center",
        bgcolor='rgba(0,0,0,0)'
    ),
    yaxis=dict(
        ticksuffix="%",
        showticksuffix='all'
    ),
    xaxis=dict(
        showspikes = False,
    ),
)
fig.write_html('./chart_htmls/herd_immunity.html')

# vax_ward = vax.loc[:,'Ward 1':'All Wards'].dropna()
# vax_ward_pc = vax_ward.divide(ward_demos['Population (2019 ACS)'])
# vax_ward_65 = vax.loc[:,'Ward 1 65+':'All Wards 65+'].dropna()
# vax_ward_65.columns = vax_ward.columns
# vax_ward_65_pc = vax_ward_65.divide(ward_demos['65+ (2019 ACS)'])

# fig = make_subplots(rows=1,cols=2,subplot_titles=['% Fully Vaccinated','% 65+ Population<br>Recieved First Dose'],shared_xaxes=True,)
# i=0
# for ward in WARD_LIST:
#     fig.add_trace(
#         go.Scatter(
#             x=vax_ward_pc.index,
#             y=vax_ward_pc[ward],
# #             mode='lines',
#             line=dict(
#                 color=PASTELS[i]
#             ),
#             name=ward,
#             legendgroup='group'+str(i+1),
#         ),
#         row=1,
#         col=1,
#     )
#     i+=1
# fig.add_trace(
#     go.Scatter(
#         x=vax_ward_pc.index,
#         y=vax_ward_pc['All Wards'],
#         line=dict(
#             color='black',
#             width=2,
#         ),
#         name='District-Wide',
#         legendgroup='group'+str(i+1),
#     ),
#     row=1,
#     col=1
# )
# i=0
# for ward in WARD_LIST:
#     fig.add_trace(
#         go.Scatter(
#             x=vax_ward_65_pc.index,
#             y=vax_ward_65_pc[ward],
# #             mode='lines',
#             line=dict(
#                 color=PASTELS[i]
#             ),
#             name=ward,
#             legendgroup='group'+str(i+1),
#             showlegend = False
#         ),
#         row=1,
#         col=2,
#     )
#     i+=1
# fig.add_trace(
#     go.Scatter(
#         x=vax_ward_65_pc.index,
#         y=vax_ward_65_pc['All Wards'],
#         line=dict(
#             color='black',
#             width=3,
#         ),
#         name='District-Wide',
#         legendgroup='group'+str(i+1),
#         showlegend = False,
#     ),
#     row=1,
#     col=2
# )
# fig.update_yaxes(
#     rangemode = 'tozero',
#     showgrid=True,
#     gridcolor='grey',
#     tickformat=".1%",
#     gridwidth=1
# )
# fig.update_xaxes(
#     showspikes=True,
#     spikedash = 'solid',
#     spikemode  = 'across',
#     spikesnap = 'cursor',
#     spikecolor = 'black',
#     spikethickness = 1,
#     ticks='outside'
# )
# fig.update_layout(
#     plot_bgcolor='rgba(0,0,0,0)',

#     spikedistance =  -1,
#     legend=dict(
#         yanchor="middle",
#         y=.5,
#         xanchor="center",
#         x=1.2,
#         bgcolor='rgba(0,0,0,0)'
#     ),
#     hovermode='x',
#     font=dict(
#         family='Arial',
#         size=14
#     ),
#     title=dict(
#         text='Cumulative Vaccinations by Ward',
#         x=0.5
#     ),

# )
# fig.update_xaxes(range=['2021-01-15',data.index[-1]])

# fig.write_html('./chart_htmls/cumulative_vaccinations.html')


# fig = make_subplots(rows=1,cols=2,subplot_titles=['New Second<br>Doses','New First Doses,<br>65+ Population'],shared_xaxes=True,)
# i=0
# for ward in WARD_LIST:
#     fig.add_trace(
#         go.Bar(
#             x=vax_ward.index,
#             y=vax_ward[ward].diff(),
#             marker_color=PASTELS[i],
#             name=ward,
#             legendgroup='group'+str(i+1),
#         ),
#         row=1,
#         col=1,
#     )
#     i+=1

# i=0
# for ward in WARD_LIST:
#     fig.add_trace(
#         go.Bar(
#             x=vax_ward_65.index,
#             y=vax_ward_65[ward].diff(),
#             marker_color=PASTELS[i],
#             name=ward,
#             legendgroup='group'+str(i+1),
#             showlegend = False
#         ),
#         row=1,
#         col=2,
#     )
#     i+=1

# fig.update_yaxes(
#     rangemode = 'tozero',
#     showgrid=True,
#     gridcolor='grey',
# #     tickformat=".1%",
#     gridwidth=1
# )
# fig.update_xaxes(
#     ticks='outside'
# )
# fig.update_layout(
#     barmode='stack',
#     plot_bgcolor='rgba(0,0,0,0)',
#     spikedistance =  -1,
#     legend=dict(
#         yanchor="middle",
#         y=.5,
#         xanchor="center",
#         x=1.2,
#         bgcolor='rgba(0,0,0,0)'
#     ),
#     hovermode='x',
#     font=dict(
#         family='Arial',
#         size=14
#     ),
#     title=dict(
#         text='New Vaccinations by Ward',
#         x=0.5
#     ),
# )
# fig.update_xaxes(range=['2021-01-13',data.index[-1]],title_text='Date of Vaccine Data Batch')
# fig.write_html('./chart_htmls/new_vaccinations.html')

fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=vax['Date'],
    y=vax['New Partial Doses: Residents'],
    marker_color='lightgreen',
    name='Resident Partial Doses',
))
fig.add_trace(go.Bar(
    x=vax['Date'],
    y=vax['New Partial Doses: Non-Residents'],
    marker_color='skyblue',
    name='Non-resident Partial Doses',
))
fig.add_trace(go.Bar(
    x=vax['Date'],
    y=vax['New Full Doses: Residents'],
    marker_color='darkgreen',
    name='Resident Full Doses',
))
fig.add_trace(go.Bar(
    x=vax['Date'],
    y=vax['New Full Doses: Non-residents'],
    marker_color='darkblue',
    name='Non-resident Full Doses',
))
fig.add_trace(go.Scatter(
    x=vax['Date'],
    y=vax.loc[:,'New Partial Doses: Residents':'New Full Doses: Non-residents'].sum(axis=1).rolling(7).mean(),
    name='7-Day Average (All)',
    mode='lines',
    line=dict(
        color='black'
    )
))
fig.update_layout(
    title=dict(
        text='Daily Doses by Residency'
    ),
    barmode='stack',
    xaxis=dict(
        showspikes=False,
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        orientation='h',
        x=.5,
        y=-.2,
        xanchor='center'
    )
)
fig.write_html('./chart_htmls/daily_vaccinations.html')


fig = go.Figure(layout=layout)
residency=vax.loc[:,['Cumulative Partial Doses: Residents','Cumulative Partial Doses: Non-Residents']].dropna()
delivered = vax.loc[:,'Total Delivered'].dropna()
fig.add_trace(go.Scatter(
    x = residency.index,
    y = residency['Cumulative Partial Doses: Residents'],
    name = 'Residents',
    line=dict(
        color='lightgreen',
        width=0
    ),
    mode='lines',
    stackgroup='group1',
    text=residency['Cumulative Partial Doses: Residents'].divide(residency.sum(axis=1))*100,
    hovertemplate='Total: %{y:.0i}<br>% of All 1st Doses: %{text:.1f}%'
))
fig.add_trace(go.Scatter(
    x = residency.index,
    y = residency['Cumulative Partial Doses: Non-Residents'],
    name = 'Non-Residents',
    line=dict(
        color='skyblue',
        width=0
    ),
    mode='lines',
    stackgroup='group1',
    text=residency['Cumulative Partial Doses: Non-Residents'].divide(residency.sum(axis=1))*100,
    hovertemplate='Total: %{y:.0i}<br>% of All 1st Doses: %{text:.1f}%'
))

fig.add_trace(go.Scatter(
    x = delivered.index,
    y = delivered,
    name = 'Total First Doses Delivered',
    mode='lines',
    line=dict(
        color='grey',
        width=4
    ),
    hovertemplate='%{y:.0i}',
    text = residency.sum(axis=1).divide(delivered)
))
fig.update_layout(
    title=dict(
        text='Cumulative First Doses Administered by Residency'
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
    )
)
fig.write_html('./chart_htmls/all_vaccinations.html')

new_vax = vax.loc[:,'New Partial Doses: Residents':'New Full Doses: Non-residents']
new_vax_breakdown = new_vax.rolling(7).sum().divide(new_vax.sum(axis=1).rolling(7).sum(),axis=0)
new_vax_first = vax.loc[:,'New Partial Doses: Residents':'New Partial Doses: Non-Residents']
new_vax_first_breakdown = new_vax_first.rolling(7).sum().divide(new_vax_first.sum(axis=1).rolling(7).sum(),axis=0)

colors = ['lightgreen','skyblue','green','blue']
fig = make_subplots(rows=2,cols=1,shared_xaxes=True,subplot_titles=['All Doses','Partial Doses'],vertical_spacing=0.07,)
i = 0
for vax_cat in new_vax_breakdown.columns:
    fig.add_trace(go.Scatter(
        x=new_vax_breakdown.index,
        y=new_vax_breakdown[vax_cat],
        line=dict(
            color=colors[i],
            width=0
        ),
        stackgroup='one',
        legendgroup='group'+str(i+1),
        mode='lines',
        name=vax_cat
    ),row=1,col=1)
    i+=1

i = 0
for vax_cat in new_vax_first_breakdown.columns:
    fig.add_trace(go.Scatter(
        x=new_vax_first_breakdown.index,
        y=new_vax_first_breakdown[vax_cat],
        line=dict(
            color=colors[i],
            width=0
        ),
        stackgroup='one',
        legendgroup='group'+str(i+1),
        showlegend = False,
        mode='lines',
        name=vax_cat
    ),row=2,col=1)
    i+=1

fig.update_yaxes(
    tickformat='.1%',
)
fig.update_xaxes(
    showspikes=True,
    spikedash = 'solid',
    spikemode  = 'across',
    spikesnap = 'cursor',
    spikecolor = 'black',
    spikethickness = 1,
    ticks='outside',
    range=['2020-12-18',vax.index[-1]]
)
fig.update_yaxes(
    tickformat='.1%',
    showgrid=True,
    gridcolor='grey',
)
fig.update_layout(
    spikedistance =  -1,
    legend=dict(
        x=0.5,
        y=-.1,
        xanchor='center',
        bgcolor='rgba(0,0,0,0)',
        orientation='h'
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    title = dict(
        x=0.5,
        text="Breakdown of New Doses<br>7-Day Average"
    ),
)
fig.update_traces(xaxis="x2")
fig.write_html('./chart_htmls/vaccinations_breakdown.html')

hood_vax = vax.loc[:,'16th St Heights':'Capitol Hill'].dropna()
cumulative = hood_vax.iloc[-1,:]
cumulative_pc = hood_vax.iloc[-1,:].divide(hood_demos['Population (2019 ACS)'])
new = hood_vax.diff().iloc[-1,:]
new_pc = new.divide(hood_demos['Population (2019 ACS)'])*10000
vax_this_week = pd.concat([cumulative,cumulative_pc,new,new_pc,hood_demos['Population (2019 ACS)'],hood_demos['Population age 65+ (2019 ACS)'].divide(hood_demos['Population (2019 ACS)']),hood_demos['OBJECTID']],axis=1)
vax_this_week.columns = ['Total Vaccinations','% Vaccinated','New Vaccinations','New Vaccinations per 10k','Population','% Population 65+','OBJECTID']
vax_this_week['Neighborhood'] = vax_this_week.index

fig = px.choropleth_mapbox(
    vax_this_week,
    geojson=hood_map,
    color=vax_this_week['% Vaccinated'],
    locations="OBJECTID",
    featureidkey="properties.OBJECTID",
    center={"lat": 38.91,
       "lon": -77.03
       },
    color_continuous_scale="Greens",
    opacity=0.5,
    mapbox_style="carto-positron",
    zoom=10,
    hover_name='Neighborhood',
    hover_data={'Neighborhood':False,
           'OBJECTID':False,
           'Total Vaccinations':True,
           'New Vaccinations':':.0f',
           'New Vaccinations per 10k':':.1f',
           '% Vaccinated':':.2%',   
           'Population':':.0f',
           '% Population 65+':':.1%',
            
           }
)
fig.update_layout(margin={
    "r":0,
    "t":0,
    "l":0,
    "b":0
    },
    coloraxis=dict(
        colorbar = dict(
            tickformat = "%.2f",
#                 ticksuffix = '+',
#                 showticksuffix = 'last',
            title = dict(
                text = '% Fully Vaccinated'
            )

        )

    )
)
fig.write_html('./chart_htmls/vaccination_map_cumulative.html')

fig = px.choropleth_mapbox(
    vax_this_week,
    geojson=hood_map,
    color=vax_this_week['New Vaccinations per 10k'],
    locations="OBJECTID",
    featureidkey="properties.OBJECTID",
    center={"lat": 38.91,
       "lon": -77.03
       },
    color_continuous_scale="Greens",
    opacity=0.5,
    mapbox_style="carto-positron",
    zoom=10,
    hover_name='Neighborhood',
    hover_data={'Neighborhood':False,
           'OBJECTID':False,
           'Total Vaccinations':True,
           'New Vaccinations':':.0f',
           'New Vaccinations per 10k':':.1f',
           '% Vaccinated':':.2%',   
           'Population':':.0f',
           '% Population 65+':':.1%',
            
           }
)
fig.update_layout(margin={
    "r":0,
    "t":0,
    "l":0,
    "b":0
    },
    coloraxis=dict(
        colorbar = dict(
            tickformat = ".0f",
#                 ticksuffix = '+',
#                 showticksuffix = 'last',
            title = dict(
                text = 'New Full<br>Vaccinations<br>per 10k'
            )

        )

    )
)
fig.write_html('./chart_htmls/vaccination_map_new_pc.html')

fig = px.choropleth_mapbox(
    vax_this_week,
    geojson=hood_map,
    color=vax_this_week['New Vaccinations'],
    locations="OBJECTID",
    featureidkey="properties.OBJECTID",
    center={"lat": 38.91,
       "lon": -77.03
       },
    color_continuous_scale="Greens",
    opacity=0.5,
    mapbox_style="carto-positron",
    zoom=10,
    hover_name='Neighborhood',
    hover_data={'Neighborhood':False,
           'OBJECTID':False,
           'Total Vaccinations':True,
           'New Vaccinations':':.0f',
           'New Vaccinations per 10k':':.1f',
           '% Vaccinated':':.2%',   
           'Population':':.0f',
           '% Population 65+':':.1%',
            
           }
)
fig.update_layout(margin={
    "r":0,
    "t":0,
    "l":0,
    "b":0
    },
    coloraxis=dict(
        colorbar = dict(
            tickformat = ".0f",
#                 ticksuffix = '+',
#                 showticksuffix = 'last',
            title = dict(
                text = 'New Full<br>Vaccinations<br>'
            )

        )

    )
)
fig.write_html('./chart_htmls/vaccination_map_new.html')

fig = go.Figure(layout=layout)
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Rail Change'],
    name='Rail',
    mode='lines'
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Bus Change'],
    name='Bus',
    mode='lines'
))
fig.update_yaxes(tickformat=".0%")
fig.update_layout(
    title=dict(
        text='Ridership Relative to Equivalent Day in 2019'
    )
)
fig.write_html('./chart_htmls/wmata_comparison.html')

fig = go.Figure(layout=layout)
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Rail Ridership'],
    name='Rail',
))
fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Bus Ridership'],
    name='Bus',
))
fig.update_layout(
    title=dict(
        text='Number of Riders'
    ),
    barmode='stack',
    legend=dict(
        x=0.95,
        y=0.95,
        bgcolor='rgba(0,0,0,0)'
    )
)
fig.write_html('./chart_htmls/wmata_ridership.html')


snf_cases['Date'] = pd.to_datetime(snf_cases['Date'])
snf_cases['Skilled Nursing Facility'] = snf_cases['Skilled Nursing Facility'].map(dict(zip(snf_keys['Name'],snf_keys['Data Name'])))
snf_pivot_cases = snf_cases.pivot(index='Date',columns='Skilled Nursing Facility',values='Total Resident Positive Cases')

fig = go.Figure(layout=layout)
i=0
snf_pivot_cases_daily = snf_pivot_cases.diff().replace(to_replace=0,value=np.nan)
for snf in snf_pivot_cases.columns:
    fig.add_trace(go.Bar(
        x=snf_pivot_cases_daily.index,
        y=snf_pivot_cases_daily[snf],
        name=snf,
        marker_color=LIGHT24[i],
    ))
    i+=1
fig.update_layout(
    barmode='stack',
    legend=dict(
        orientation='h',
        y=-.2,
        x=.5,
        xanchor='center',
        bgcolor='rgba(0,0,0,0)',
    ),
    xaxis=dict(
        showspikes=False
    ),
    title=dict(
        text='Weekly Cases at Select Skilled Nursing Facilities'
    )
)
fig.write_html('./chart_htmls/snf_cases.html')

al_cases['Date'] = pd.to_datetime(al_cases['Date'])
al_cases['Assisted Living Residence'] = al_cases['Assisted Living Residence'].map(dict(zip(al_keys['Data Name'],al_keys['Name'])))
al_pivot_cases = al_cases.pivot(index='Date',columns='Assisted Living Residence',values='Total Resident Positive Cases')
fig = go.Figure(layout=layout)
i=0
al_pivot_cases_daily = al_pivot_cases.diff().replace(to_replace=0,value=np.nan)
for al in al_pivot_cases.columns:
    fig.add_trace(go.Bar(
        x=al_pivot_cases_daily.index,
        y=al_pivot_cases_daily[al],
        name=al,
        marker_color=LIGHT24[i],
    ))
    i+=1
fig.update_layout(
    barmode='stack',
    legend=dict(
        orientation='h',
        y=-.2,
        x=.5,
        xanchor='center',
        bgcolor='rgba(0,0,0,0)',
    ),
    xaxis=dict(
        showspikes=False
    ),
    title=dict(
        text='Weekly Cases at Select Assisted Living Residences'
    )
)
fig.write_html('./chart_htmls/alr_cases.html')

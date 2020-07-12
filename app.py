import numpy as np
import csv
import pandas as pd
import plotly.io as pio
pio.templates.default = "seaborn"
# Standard plotly imports
from chart_studio.plotly import plot, iplot
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
# Using plotly + cufflinks in offline mode
import cufflinks
cufflinks.go_offline(connected=True)
import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# loading drug use dataset
drug_use = pd.read_csv('data/drug-use-by-age.csv')

# '-' spotted, replaced with 0 as linked to use value which equals zero in this instance
drug_use.replace('-','0',inplace=True)

# Range in age replaced with means of range values to enable use in calculation
# as object type not accepted
drug_use.age.replace({'22-23':'22.5','24-25':'24.5','26-29':'27.5','30-34':'32',
                      '35-49':'42','50-64':'57','65+':'65'},inplace=True)


# set variable types
for col in drug_use.select_dtypes(include=['object']).columns:
    drug_use[col] = drug_use[col].astype('float')

drug_use.set_index('age',inplace=True) 


## Creating a DF with the use, setting 'age' as index and removing -use in column names

usage = drug_use[(drug_use.columns.values[drug_use.columns.str.contains('use')])]
usage.columns = usage.columns.str.replace('-use','')

usage_transformed = usage.apply(lambda x: x/100)

## Creating a DF with the frequency, removing -frequency in column names

frequency = drug_use[(drug_use.columns.values[drug_use.columns.str.contains('freq')])]

frequency.columns = frequency.columns.str.replace('-frequency','')

for col in frequency.columns:
    frequency[col] = frequency[col].astype('int')


layout_us_bar={
        "xaxis":{
            "showgrid":False,
            "showline":True,
            "showticklabels":True,
            "domain":[0, 1],
            "gridcolor":'lightgray',
            "gridwidth":0.5,
            "linecolor":'lightgray',
            "linewidth":2,
            "mirror":True,
            "nticks":4,
            "type":'log',
            "range":[-3,0]
        },
        "yaxis":{
            "showline":True,
            "showticklabels":True,
            "linecolor":'lightgray',
            "linewidth":2,
            "mirror":True,
            "ticks":'outside'
        },
        "paper_bgcolor":'#F5F6F9',
        "plot_bgcolor":'#F5F6F9',
        "margin":{'l':120, 'r':10, 't':20, 'b':80},
        "font_color":'rgb(13,48,100)',
        "annotations" : [{
            'x':0,
            'y':-0.16,
            'xref':'paper',
            'yref':'paper',
            'text':'Source: <a href="https://github.com/fivethirtyeight/data/tree/master/drug-use-by-age">\
                How Baby Boomers Get High </a>',
            'showarrow':False}]
 }

##read them into pandas

big_df=pd.read_csv('data/global_df.csv')

## slider marks design

visible={1990:'1990',2017:'2017'}
invisible={str(i):'' for i in big_df['year'].unique()[1:-1]}

visible.update(invisible)

layout={
    'title':'<b>Death rates from drug use disorders in 1990</b> <br><sub>measured per 100,000 individuals</sub>',
    'paper_bgcolor':'#F5F6F9',
    'plot_bgcolor':'#F5F6F9',
    'font_color':'#505050',
    'geo':{
        'showframe':False,
        'showcoastlines':True,
        'projection_type':'equirectangular',
        'lataxis_range':[-60,90],
        'domain':{'y':[0,1]}},
    'yaxis_fixedrange':True,
    'xaxis_fixedrange':True,
    'dragmode':False,
    'autosize':True,
    'margin':{'autoexpand':True},
    'height':600,
    'annotations':[{
        'x':0,
        'y':-0.1,
        'xref':'paper',
        'yref':'paper',
        'text':'Source: <a href="http://ghdx.healthdata.org/gbd-results-tool">\
            IHME, Global Burden of Disease </a>',
        'showarrow':False}]}

## mental health df
mental_health = pd.read_csv('data/mental-health-as-risk-for-drug-dependency.csv')

trace_mh = [go.Bar(
                y=mental_health['Entity'],
                x=mental_health.iloc[:,3],
                name='Odds ratio',
                orientation='h',
                marker=dict(color=[np.log(x + 0.1) for x in mental_health.iloc[:,3]],
                                colorscale='PuBu',
                                line=dict(color='DarkBlue')
                                ),
                hovertemplate="%{x}"
            )]

layout_mh={
	'xaxis':{
        'showgrid':True,
        'showline':True,
        'showticklabels':True,
        'domain':[0, 1],
        'gridcolor':'lightgray',
        'gridwidth':0.1,
        'linecolor':'lightgray',
        'linewidth':2,
        'mirror':True,
        'title':'Odds Ratio'
    },
    'yaxis':{
        'showline':True,
        'showgrid':False,
        'showticklabels':True,
        'linecolor':'lightgray',
        'linewidth':2,
        'mirror':True,
        'ticks':'outside',
        'type':'category',
        'categoryorder':'total ascending'
    },
    'paper_bgcolor':'#F5F6F9',
    'plot_bgcolor':'#F5F6F9',
    'font_color':'#505050',
    'font_size':10,
    'autosize':True,
    'margin':{'autoexpand':True,'t':20},
    'annotations':[{
        'x':-0.2,
        'y':-0.16,
        'xref':'paper',
        'yref':'paper',
        'text':'Source: <a href="https://ourworldindata.org/mental-health-disorders-as-risk-for-substance-use">\
            Our World in Data </a>',
        'showarrow' : False}]

}
	

fig_mh = go.Figure(data=trace_mh,layout=layout_mh)

#. http://ghdx.healthdata.org/gbd-results-tool?params=gbd-api-2017-permalink/3c5c2b8846e4b1ecae4a9eb461e9a193

disorder_age_sex = pd.read_csv('data/my_data.csv')
disorder_age_sex = disorder_age_sex[['location','sex','age','year','val']]
disorder_age_sex.replace('Global','World',inplace=True)
disorder_age_sex = disorder_age_sex.replace('5-14 years','05-14').replace('70+ years','70+').sort_values(by='age')


layout_prev={
    'xaxis' : {
        'showgrid':True,
        'showline':True,
        'showticklabels':True,
        'domain':[0, 1],
        'gridcolor':'lightgray',
        'gridwidth':0.1,
        'linecolor':'lightgray',
        'linewidth':2,
        'mirror':True,
        'hoverformat':'.3%',
        'tickformat':'.1%'
    },
    'yaxis' : {
        'showline':True,
        'showgrid':False,
        'showticklabels':True,
        'linecolor':'lightgray',
        'linewidth':2,
        'mirror':True,
        'ticks':'outside',
        'autorange':'reversed'

    },
    'paper_bgcolor' : '#F5F6F9',
    'plot_bgcolor' : '#F5F6F9',
    'font_color' : '#505050',
    'font_size' : 10,
    'autosize' : True,
    'margin':{'autoexpand': True, 't': 20},
    'barmode':'group',
    'annotations':[{
        'x':0,
        'y':-0.18,
        'xref':'paper',
        'yref':'paper',
        'text':'Source: <a href="http://ghdx.healthdata.org/gbd-results-tool">\
            IHME, Global Burden of Disease </a>',
        'showarrow':False}]
}



regions_dict = [{'label':i,'value':i} for i in disorder_age_sex.location.unique()]


# Navbar

EA_LOGO = 'https://i.ibb.co/tBrybcK/mylogo.png'

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=EA_LOGO, height="45px",className="logo"),md=2),
                    dbc.Col(
                        dbc.NavbarBrand("Global Drug Epidemic",
                                        className="ml-2",style={'color':'#F0FFFF','font-weight':'bold',
                                                               'font-size':'x-large'})
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://github.com/emilieallen",
        )
    ],
    color="#778899",
    sticky="top"
)


# In[18]:


MARKDOWN = dbc.Col(
    dcc.Markdown('''

_The main groups of illicit drugs used in the following statistics are opioids, cocaine,amphetamine, and cannabis._
_Illicit drugs refer to drugs that have been prohibited under international drug control treaties._

_Drug dependence is defined by the International Classification of Diseases as the presence of three or more indicators_
_of dependence for at least a month within the previous year. Drug dependency includes all illicit drugs._

_For more information go to [Our World in Data](https://ourworldindata.org/illicit-drug-use)._
''',style={'font-size':'small','paddingLeft':15,'marginTop':10,
          'border-left-style':'dotted'})
)



# In[19]:


DEATH_RATES_PLOT = [
    dbc.CardHeader(html.H5("Deaths from drug use disorders")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-death_rates",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try\
                        loading this page again if problem persists.",
                        id="no-data-alert-death_rates",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Select the region and drug type:"),
                                    md=12),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="region-dropdown",
                                        options=[
                                            {'label': u'World',
                                                'value': 'world'},
                                            {'label': 'Europe',
                                                'value': 'europe'},
                                            {'label': 'USA', 'value': 'usa'},
                                            {'label': 'Asia', 'value': 'asia'},
                                            {'label': 'Africa',
                                                'value': 'africa'},
                                            {'label': 'North America',
                                                'value': 'north america'},
                                            {'label': 'South America',
                                                'value': 'south america'}
                                            ],
                                        value='world',
                                        clearable=False
                                    )
                                ],
                                md=6,
                            ),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="drug_type-dropdown",
                                        options=[
                                            {'label': u'Drug Disorder',
                                             'value': 'ALL'},
                                            {'label': 'Cocaine', 'value': 'C'},
                                            {'label': 'Amphetamine',
                                             'value': 'AMP'},
                                            {'label': 'Opioid', 'value': 'OP'}
                                            ],
                                        value='ALL',
                                        clearable=False
                                    )
                                ],
                                md=6,
                            ),
                        ]
                    ),
                    html.Br(),
                    dcc.Graph(id="death-rates-graph"),
                    html.Br(),
                    dcc.Slider(
                        id="death-rates-year-slider",
                        min=big_df['year'].unique()[0],
                        max=big_df['year'].unique()[-1],
                        value=big_df['year'].unique()[0],
                        marks=visible,
                        included=False
                        ),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


# In[20]:


MENTAL_HEALTH_PLOT = [
    dbc.CardHeader(html.H5("Risk factor: mental health & substance abuse")),
    dbc.CardBody(
        [
            html.P(
                "The ADHD value of 5.2 indicate that individuals with ADHD are 5.2 times as likely to\
                 develop drug dependency relative to those without.",
                style={"fontSize": 13},
                className="mb-0",
            ),

            html.Br(),

            dcc.Graph(id="mental-health", figure=fig_mh)
        ],
        style={"marginTop": 10, "marginBottom": 0},
    )
]


# In[21]:


LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H6(children="Data Selection",style={'fontSize':15}),
        html.Hr(className="my-2"),
        html.Label("Select a year", style={'fontSize':'small'}),
        dcc.Slider(
            id="prevalence-year-slider",
            min=big_df['year'].unique()[0],
            max=big_df['year'].unique()[-1],
            value=big_df['year'].unique()[0],
            marks=visible,
            included=False
            ),
        html.Label("Select a region", style={"marginTop": 10,'fontSize':'small'}),
        dcc.Dropdown(
            id="prevalence-region",
            options=regions_dict,
            value='World',
        )
    ], style={'padding':'20px 10px'}
)


# In[22]:


PREVALENCE_PLOT = [
    dbc.CardHeader(html.H5("Prevalence of drug use disorders")),
    dbc.CardBody(
        [
            html.H6(children=["Share of 18 year old who admitted using the following drugs in the past year"],
                    className="card-title",style={'text-align':'center'},
                    id='prevalence-title'),
            dbc.Row([
                dbc.Col(LEFT_COLUMN,md=3),
                dbc.Col(dcc.Graph(id="prevalence-graph"),md=9)
            ])
        ]
    )

]


# In[23]:


age_dict={x:str(round(i)) for x,i in enumerate(drug_use.index)}

US_DRUG_USE = [
    dbc.CardHeader(html.H5("How Americans get high")),
    dbc.CardBody([
        html.H6(className="card-title",style={'text-align':'center'},id='drug-use-title'),
        html.P(className="card-subtitle",style={'text-align':'center',"fontSize": 13,'marginBottom':10},
                    id='drug-use-subtitle'),
        dbc.Row([
            dbc.Col([html.P("Select age:"),
                     dcc.Slider(id="age-slider",
                               min=0,
                               max=16,
                               value=6,
                               marks=age_dict,
                               vertical=True,
                               included=False)],md=3,style={'display': 'flex','align_items':'center',
                                                               'flex-direction':'col','padding':'15px',
                                                              'justify-content':'space-around'}),
            dbc.Col(dcc.Graph(id="drug_use"),style={'marginLeft':10})])
    ])
]


# In[24]:


# body

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(MARKDOWN))], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(DEATH_RATES_PLOT))], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(MENTAL_HEALTH_PLOT))], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(PREVALENCE_PLOT))], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(US_DRUG_USE))], style={"marginTop": 30})

    ],
    className="mt-12",
)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,external_stylesheets])
server = app.server  # for Heroku deployment

app.layout = html.Div(children=[NAVBAR,BODY])

@app.callback(
    dash.dependencies.Output('death-rates-graph', 'figure'),
    [dash.dependencies.Input('drug_type-dropdown', 'value'),
     dash.dependencies.Input('death-rates-year-slider', 'value'),
     dash.dependencies.Input('region-dropdown', 'value'),
     dash.dependencies.Input('region-dropdown', 'options'),])
def update_death_rates_figure(selected_drug, selected_year, selected_scope, options):
    title = {'all_rate': 'drug use disorders',
             'cocaine_rate': 'cocaine overdoses',
             'amphetamine_rate': 'amphetamine overdoses',
             'opioid_rate': 'opioid overdoses'}
    lexique = {'ALL': 'all_rate',
               'C': 'cocaine_rate',
               'AMP': 'amphetamine_rate',
               'OP': 'opioid_rate'}
    col = lexique.get(selected_drug)
    tl = title.get(col)

    trace = [go.Choropleth(
                visible=True,
                locations=big_df.code[big_df.year == selected_year],
                z=big_df[col][big_df.year == selected_year],
                zmin=0,
                zmid=1,
                zmax=big_df[col].max(),
                text=big_df.country[big_df.year == selected_year],
                name=str(selected_year),
                hoverinfo="z+text",
                colorscale=["#f7fbff", "#c6dbef", "#85bcdb", "#6baed6",
                            "#57a0ce", "#4292c6", "#3082be", "#2171b5",
                            "#1361a9", "#08519c", "#0b4083", "#08306b"],
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar={'x': 1, 'thickness': 15, 'nticks': 5, 'len': 0.95}
            )]

    lb = [options[i]['label'] for i in range(len(options))
          if options[i]['value'] == selected_scope]

    layout['geo'] = dict(showframe=False, showcoastlines=True,
                         lataxis_range=[-60, 90], projection_type='equirectangular',
                         scope=selected_scope)

    layout['title'] = '<b>Death rates from {} in {}, {}</b> <br><sub>measured per 100,000 individuals</sub>'.format(tl, selected_year, lb[0])

    return {'data': trace, 'layout': layout}

@app.callback(
    [dash.dependencies.Output('prevalence-graph', 'figure'),
    dash.dependencies.Output('prevalence-title','children')],
    [dash.dependencies.Input('prevalence-region', 'value'),
     dash.dependencies.Input('prevalence-year-slider', 'value')])
def update_prevalence_figure(selected_region, selected_year):
    disorder_age_sex_female = disorder_age_sex[(disorder_age_sex.sex == 'Female')
                                               & (disorder_age_sex.year == selected_year)
                                               & (disorder_age_sex.location == selected_region)]

    disorder_age_sex_male = disorder_age_sex[(disorder_age_sex.sex == 'Male')
                                             & (disorder_age_sex.year == selected_year)
                                             & (disorder_age_sex.location == selected_region)]

    trace = [go.Bar(x=disorder_age_sex_female.val,
                    y=disorder_age_sex_female.age,
                    name='Female',
                    orientation='h',
                    marker=dict(color='rgb(146,197,222)',
                    line=dict(color='Darkblue'))),

            go.Bar(x= disorder_age_sex_male.val,
                   y= disorder_age_sex_male.age,
                   name='Male',
                   orientation ='h',
                   marker=dict(color='rgb(8,64,129)',
                   line=dict(color='DarkBlue')))]

    title = "Share of population within each age category suffering from drug use disorders in {}, {}".format(selected_year, selected_region)

    return {'data': trace, 'layout': layout_prev}, title

@app.callback(
    [dash.dependencies.Output('drug_use', 'figure'),
     dash.dependencies.Output('drug-use-title','children'),
     dash.dependencies.Output('drug-use-subtitle','children')],
    [dash.dependencies.Input('age-slider', 'value')])
def update_drug_use(selected_age):
    #bar chart
    age = [i for v,i in age_dict.items() if v==selected_age][0]
    i = usage.index[min(range(len(usage.index)),key = lambda i: abs(sorted(usage.index)[i]-float(age)))]

    trace_bar=[go.Bar(
                    x=usage_transformed.loc[i, :].sort_values(),
                    y=usage_transformed.loc[i, :].sort_values().keys(),
                    name='{} yrs'.format(i),
                    orientation='h',
                    marker=dict(color=[np.log(x + 0.1) for x in
                                usage.loc[i, :].sort_values().values],
                                colorscale='PuBu',
                                line=dict(color='DarkBlue',width=0.8)
                                ),
                    hovertemplate="%{x:.1%} | %{y}"
                )]
    x = drug_use.iloc[selected_age,0]
    title = "Share of {} year old who admitted using the following drugs in the past year ".format(int(i))

    subtitle = "% of {:,} surveyee in the US, 2012".format(x)

    return {'data':trace_bar,'layout':layout_us_bar}, title, subtitle

if __name__ == "__main__":
    app.run_server(debug=True)

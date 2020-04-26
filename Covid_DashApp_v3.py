#!/usr/bin/env python
# coding: utf-8

# In[2]:


### SETUP ###

import pandas as pd
import urllib

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

import plotly.graph_objs as go

#import dash
from dash.dependencies import Input, Output

### INPUT ###

datasource_url = 'https://brasil.io/dataset/covid19/caso?place_type=state&format=csv'

flag=[{'info':'teste','valor':'-'} for x in range(6)]

# In[3]:


### CUSTOM FUNCTIONS ###

###### TITLE VARIABLE CUSTOMIZATION ######

title_id = "title-container"

title_text_id = "title-text"
title_text = "Covid Data in Brazil"


###### TITLE DISPLAY FUNCTION ######

def build_title():
    return html.Div(
        id=title_id,
        className=title_id,
        style={'background-color': '#000000', 'margin-bottom' : '20px', 'width': '90%', 'margin-left': '50px'},
        children=[
            html.Div(
                id=title_text_id,
                children=[
                    html.Div(title_text, style={'font-family': 'Roboto','color': '#ffffff', 'fontSize': 36, 'font-weight': 'bold'}),
                ],
            ),
            
        ],
    )


###### DROPDOWN DISPLAY FUNCTION ######

def build_dropdown(dropdown_container_id, dropdown_text, dropdown_id, dropdown_options):
    return html.Div(
        id = dropdown_container_id,
        className = dropdown_container_id,
        style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'left', 'width': '90%', 'margin-left': '50px'},
        children=[
            html.Div(dropdown_text, style={'font-family': 'Roboto','color': '#000000', 'fontSize': 18, 'font-weight': 'bold'}),
            dcc.Dropdown(
                id=dropdown_id,
                options = [{'label': x, 'value': x} for x in dropdown_options],
                value = dropdown_options[0],
                style={'width': '300px'}
            ),
            
        ],
    )



###### GRAPH DISPLAY FUNCTION ######

def build_graph(graph_container_id, graph_id):
    return html.Div(
        id = graph_container_id,
        className = graph_container_id,
        style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'left', 'width': '50%' , 'margin-left': '50px', 'float':'left'},
        children=[

            dcc.Graph(
                id= graph_id
                )
            
        ],
    )


###### TABLE DISPLAY FUNCTION ######


def build_table(table_container_id,data_table):
    return html.Div(
    [
        dt.DataTable(
            id = table_container_id,
            data=data_table,#.to_dict('rows'),
            columns=[{'id': 'info', 'name': 'Info'},{'id':'valor','name':'Value'}],
            #style_as_list_view=True,
            #selected_rows=[],
            style_cell={#'padding': '5px',
                        'whiteSpace': 'no-wrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        #'maxWidth': 0,
                        'width':'auto',
                        'height': 'auto',
                        'textAlign': 'left'},
#            style_header={
#                'backgroundColor': 'white',
#                'fontWeight': 'bold',
#                'color': 'black'
#            },
            #style_cell_conditional=[],
            #virtualization=True
            )])

# In[4]:


### RETRIEVE DATA ###

response = urllib.request.urlopen(datasource_url)
dataset = pd.read_csv(response,header=0)
#dataset.head()

dataset = dataset.drop(columns=['city','place_type'])


#print(list(set(list(dataset.Estado))))


# In[5]:


### DASH APP ###

external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Open+Sans|Roboto&display=swap',
    dbc.themes.BOOTSTRAP
]

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "CogniSteward", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets
)

app.title = 'Covid19 in Brazil'


app.layout = html.Div(children=[
    build_title(),
    build_dropdown(dropdown_container_id = 'Estado_dropdown_container', dropdown_text='Select a state:', dropdown_id = 'Estado_dropdown', dropdown_options = list(set(list(dataset.state)))),
    html.Div(style={'height':'50%'},
            children=[build_graph(graph_container_id='Estado_graph_container', graph_id = 'Estado_graph'),
                       html.Div(id="div_table" , style = {#'margin-top': '35',
                                           #'margin-left': '15',
                                           #'border': '1px solid #C6CCD5',
                                           'padding-top': '100px',
                                           'padding-right': '50px',
                                           'float':'right',
                                           'width':'40%',
                                           'height':'auto'},
                                children=[build_table('Estado_table',flag)])
                       ])
    ]   
)


###########################################   REACTIVE FUNCTIONS   #####################################################


@app.callback(
    Output('Estado_graph', 'figure'),
    [Input('Estado_dropdown', 'value')])

def update_graph(estado_selection):
    
    filtered_data = dataset[dataset.state==estado_selection]
    
    #print(estado_selection)
    #print(filtered_data)
    #print(list(filtered_data.Casos))
    #print(list(filtered_data.Data))
    
    trace_1 = go.Scatter(x = list(filtered_data.date), y = list(filtered_data.confirmed),
                        name = 'Confirmed Cases',
                        line = dict(width = 2,
                                    color = 'blue'))
    
    trace_2 = go.Scatter(x = list(filtered_data.date), y = list(filtered_data.deaths),
                        name = 'Confirmed Deaths',
                        line = dict(width = 2,
                                    color = 'red'))
    
    layout =  go.Layout(title = 'Covid19 Graph in ' + estado_selection,
                   hovermode = 'closest')
    
    figure = go.Figure(data = [trace_1, trace_2], layout = layout)
   
    
    return figure

@app.callback(
    Output('Estado_table', 'data'),
    [Input('Estado_dropdown', 'value')])

def update_table(estado_selection):
    filtered_data = dataset[dataset.state==estado_selection]
    filtered_data=filtered_data[filtered_data.is_last==True]
    filtered_data=filtered_data.drop(columns=['state','is_last','city_ibge_code'])

    return [{'info':x,'valor':filtered_data[x].values} for x in filtered_data]
    





#############################################   SERVER SETTINGS   #####################################################

if __name__ == '__main__':
    app.run_server(debug=False)


#######################################################################################################################   


# In[ ]:






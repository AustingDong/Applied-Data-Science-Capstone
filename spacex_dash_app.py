# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

ls = []
ls.append({'label': 'All Sites', 'value': 'All Sites'})
dist_ls = spacex_df['Launch Site'].unique().tolist()
for site in dist_ls:
    ls.append({'label': site, 'value': site})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(
                                        id='site-dropdown',
                                        options=ls,
                                        value='All Sites',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                           2500: '2500',
                                           5000: '5000',
                                           7500: '7500',
                                        10000: '10000'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                                            [Input(component_id='site-dropdown', component_property='value')])
def get_pie_chart(site_dropdown):
    if site_dropdown == 'All Sites' or site_dropdown == 'None':
        data = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(data, names = 'Launch Site', 
                    title='Total Success Launches By Site')
        return fig
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(data, names = 'class',
        title=f'Total Success Launches for {site_dropdown}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                                            [Input(component_id='site-dropdown', component_property='value'),
                                             Input(component_id='payload-slider', component_property='value')])
def get_payload_scatter_chart(site_dropdown, payload_slider):
    l, r = payload_slider
    if site_dropdown == 'All Sites' or site_dropdown == 'None':
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(l, r)]
        fig = px.scatter(data, 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation between Payload and Success for all Sites',
                color = "Booster Version Category")
        return fig
    else:
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(l, r)]
        data = data[data['Launch Site'] == site_dropdown]
        fig = px.scatter(data, 
                x = "Payload Mass (kg)", 
                y = "class",
                title = f'Correlation between Payload and Success for {site_dropdown}',
                color = "Booster Version Category")
        return fig
    
# Run the app
if __name__ == '__main__':
    app.run_server()

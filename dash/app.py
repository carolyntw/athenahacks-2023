# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import os
import dash
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px


app = Dash(__name__)
# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read data and clean it
gh_data = pd.read_csv('historical_emissions.csv')
gh_data.drop(['Data source', 'Sector', 'Gas', 'Unit'], axis=1, inplace=True)
for x in range(1990, 1998):
    gh_data.drop([f'{x}'], axis=1, inplace=True)
df = gh_data.set_index('Country').T
df.reset_index(inplace=True)
df.rename(columns={'index': 'Year'}, inplace=True)
df.sort_values(by=['Year'], inplace=True)
df.reset_index(drop=True, inplace=True)
    
year_list = [i for i in range(1998, 2018+1, 1)]
country_list = df.columns[1:]

fig = px.line(df, x='Year', y='World', 
              labels={"Year": "Year (1998-2018)", "World": "World CO2 Emission (in MtCO₂e)"}, 
              title='World CO2 Emission from 1998-2018')
fig.update_layout(title_x=0.5, title_y=0.85)

# Application layout
app.layout = html.Div(children=[ 
                                # Add title to the dashboard
                                html.H1('Carbon Footprint Tracker',
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
                                
                                # Add a division for World CO2 emission data
                                dcc.Graph(figure=fig),
                                
                                # Dropdown creation, create an outer division 
                                html.Div([
                                    # Add an division
                                    html.Div([
                                        # Create an division for adding dropdown helper text for report type
                                        html.Div(
                                            [
                                            html.H2('Country:', style={'margin-right': '2em'}),
                                            ]
                                        ),
                                        # Add a dropdown for country selection
                                        dcc.Dropdown(id='input-type', 
                                            options=[{'label': i, 'value': i} for i in country_list],
                                            placeholder='Select a country',
                                            style={'width': '80%', 'padding': '3px', 'font-size': '18px', 'text-align-last': 'center'}
                                        )
                                    # Place them next to each other using the division style
                                    ], style={'display':'flex'}),
                                    
                                   # Add next division 
                                   html.Div([
                                       # Create an division for adding dropdown helper text for choosing year
                                        html.Div(
                                            [
                                            html.H2('Choose Year:', style={'margin-right': '2em'})
                                            ]
                                        ),
                                        dcc.Dropdown(id='input-year', 
                                                     # Update dropdown values using list comphrehension
                                                     options=[{'label': i, 'value': i} for i in year_list],
                                                     placeholder="Select a year",
                                                     style={'width':'80%', 'padding':'3px', 'font-size': '18px', 'text-align-last' : 'center'}),
                                            # Place them next to each other using the division style
                                            ], style={'display': 'flex'}),  
                                          ]),
                                # more graphs to be added with callbacks functions...
                                
                                ])


if __name__ == '__main__':
    app.run_server(debug=True)

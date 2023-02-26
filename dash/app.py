# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import os
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
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
df['Year'] = df['Year'].astype(int)
    
year_list = [i for i in range(1998, 2018+1, 1)]
country_list = df.columns[2:]

world_fig = px.line(df, x='Year', y='World', 
              labels={"Year": "Year (1998-2018)", "World": "World CO2 Emission (in MtCO₂e)"}, 
              title='World CO2 Emission from 1998-2018')
world_fig.update_layout(title_x=0.5, title_y=0.85)

# Application layout
app.layout = html.Div(children=[ # Add title to the dashboard
                                html.H1('Carbon Footprint Tracker',
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
                                
                                # Add a division for World CO2 emission data
                                dcc.Graph(figure=world_fig),
                                
                                # Dropdown creation, create an outer division 
                                html.Div([
                                    # Add an division
                                    html.Div([
                                        # Add dropdown
                                        html.Div(
                                            [html.H2('Country:', style={'margin-right': '2em'}),]),
                                        dcc.Dropdown(id='input-country',
                                                       options=[{'label': i, 'value': i} for i in country_list],
                                                       multi=True,
                                                       placeholder="Select a country here",
                                                       searchable=True),

                                        # Add slider
                                        html.Div([html.Label("Choose Year:"),
                                            dcc.RangeSlider(id='year-slider',
                                                        min=1998, max=2018, step=1,
                                                        marks={1998: '1998', 2000: '2000', 2002: '2002', 2004: '2004', 2006: '2006', 2008: '2008', 
                                                                 2010: '2010', 2012: '2012', 2014: '2014', 2016: '2016', 2018: '2018'},
                                                        value=[1998, 2018]),
                                            dcc.Graph(id='country_plot')]),
                                    ])])])

@app.callback(Output(component_id='country_plot', component_property='figure'),
            Input(component_id='input-country', component_property='value'),
            Input(component_id='year-slider', component_property='value'),
            prevent_initial_call = True)

def get_line(country, year):
    year_df = df[df['Year'].between(year[0], year[1], inclusive='both')]['Year']
    country_df = df[df['Year'].between(year[0], year[1], inclusive='both')][country]
    filtered_df = pd.concat([year_df, country_df], axis=1)
    fig = px.line(filtered_df, x='Year', y=country, labels={"value": "CO2 Emission (in MtCO₂e)", "variable": "Country"},
                  title=f'CO2 Emission (in MtCO₂e) between {year[0]} and {year[1]}')
    fig.update_layout(title_x=0.5, title_y=0.85)
    return fig
        

if __name__ == '__main__':
    app.run_server(debug=True)

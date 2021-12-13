"""Generate a heatmap given p-index data."""

import plotly.express as px
import pandas as pd
import json
from crime_data import CrimeData
import dash
from dash import dcc
from dash import html


def generate_heatmap(data: CrimeData) -> None:
    """Generate an animated heatmap for the pindexes of the CrimeData,
    data, with a dropdown menu to switch between crime type."""
    # open the geojson file of the neighbourhood boundaries
    with open('local-area-boundary.geojson') as file:
        regions = json.load(file)

    # Create a pandas dataframe with all the necessary data
    unpacked_data = unpack_data(data)
    df = pd.DataFrame({'date': unpacked_data[0],
                       'region': unpacked_data[1],
                       'p-index': unpacked_data[2],
                       'crime-type': unpacked_data[3]})

    # extract a list containing the names of all crime types
    crime_types = list(data.crime_pindex.keys())

    # Create a dash app with a dropdown menu so that we can switch between graphs
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Dropdown(
            id='crime-type-dropdown',
            options=[{'label': crime, 'value': crime} for crime in crime_types],
            value=crime_types[0]
        ),
        dcc.Graph(id='choropleth-graph')])

    # this function is called every time the dropdown menu is updated.
    @app.callback(
        dash.dependencies.Output('choropleth-graph', 'figure'),
        [dash.dependencies.Input('crime-type-dropdown', 'value')])
    def update_output(crime: str):
        """Update which graph is shown in our app by returning the pertinent figure."""
        fig = px.choropleth_mapbox(df[df['crime-type'] == crime], geojson=regions,
                                   locations='region',
                                   color='p-index',
                                   color_continuous_scale=['LawnGreen', 'LightBlue', 'DarkRed'],
                                   range_color=(-100, 100),
                                   featureidkey="properties.name",
                                   mapbox_style="carto-positron",
                                   opacity=0.5,
                                   center={"lat": 49.24200376111951, "lon": -123.13312355113719},
                                   zoom=11,
                                   animation_frame='date',
                                   height=750)

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title=f'<b>P-index graph for {crime}</b>')
        return fig

    # start the dash server (port will be printed in console automatically)
    app.run_server()


def unpack_data(data: CrimeData) -> tuple[list[str], list[str], list[float], list[str]]:
    """Unpack the data in CrimeData into three lists, one corresponding to the dates, one to the
    regions, one to the pindexes, and one for the crime types.
    
    (It's hard to create a doctest because the CrimeData object cannot be created/built simply)
    """
    dates = []
    regions = []
    pindexes = []
    crime_types = []

    # loop through every crime type
    for crime in data.crime_pindex:
        # loop through each NeighbourhoodCrimePIndex object
        for obj in data.crime_pindex[crime].values():
            # get all the years in chronological order
            years = sorted(list(obj.p_index_dict.keys()))
            
            for year in years:
                # get all the months in order
                months = list(obj.p_index_dict[year].keys())
                
                for month in months:
                    # append the pertinent data to the lists
                    dates.append(month_year_to_str(month, year))
                    regions.append(obj.neighbourhood)
                    pindexes.append(obj.get_data(year, month))
                    crime_types.append(crime)

    return dates, regions, pindexes, crime_types


def month_year_to_str(month: int, year: int) -> str:
    """Given the month and year as ints, return the datestring in the form 'month year'
    (months are indexed starting at 1).
    
    >>> month_year_to_str(10, 2021)
    Oct 2021
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return f'{months[month - 1]} {year}'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['plotly', 'pandas', 'json', 'crime_data', 'dash'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
    
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

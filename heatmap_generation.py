"""Generate a heatmap given p-index data."""

import plotly.express as px
import pandas as pd
import json
from crime_data import CrimeData


def generate_heatmap(data: CrimeData, crime: str) -> None:
    """Generate an animated heatmap for the pindexes of the crime over time given the CrimeData,
    data."""
    with open('local-area-boundary.geojson') as file:
        regions = json.load(file)

    unpacked_data = unpack_data(data, crime)

    df = pd.DateFrame({'date': unpacked_data[0],
                       'region': unpacked_data[1],
                       'p-index': unpacked_data[2]})

    fig = px.choropleth_mapbox(df, geojson=regions,
                               locations='region',
                               color='p-index',
                               color_continuous_scale="Viridis",
                               range_color=(-100, 100),
                               featureidkey="properties.name",
                               mapbox_style="carto-positron",
                               opacity=0.5,
                               center={"lat": 0, "lon": 0},
                               zoom=1,
                               animation_frame='date')

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, )

    fig.show()


def unpack_data(data: CrimeData, crime: str) -> tuple[list[str], list[str], list[float]]:
    """Unpack the data in CrimeData into three lists, one corresponding to the dates, one to the
    regions, and one to the pindexes."""
    dates = []
    regions = []
    pindexes = []
    pindex_data = data.crime_pindex[crime]

    for neighbourhood in pindex_data:
        for obj in pindex_data[neighbourhood]:
            years = sorted(list(obj.p_index_dict.keys()))
            for year in years:
                months = list(obj.p_index_dict[year].keys())
                for month in months:
                    dates.append(month_year_to_str(month, year))
                    regions.append(obj.neighbourhood)
                    pindexes.append(obj.get_data(year, month))

    return dates, regions, pindexes


def month_year_to_str(month: int, year: int) -> str:
    """Given the month and year as ints, return the datestring in the form 'month year'"""

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return f'{months[month]} {year}'

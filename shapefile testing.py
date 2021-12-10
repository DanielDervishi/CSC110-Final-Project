"""
a
"""
import geopandas as gpd
df = gpd.read_file('local-area-boundary.shp')


def create_plot(color: list[tuple], df: gpd.geodataframe.GeoDataFrame) -> None:
    """
    create plot
    """
    df['color'] = color
    df.plot(color=df['color'], column='mapid', legend=True)


def update_plot(color: list[tuple], df: gpd.geodataframe.GeoDataFrame) -> None:
    """
    update plot
    """
    df['color'] = color
    df.plot(color=df['color'], column='mapid', legend=True)

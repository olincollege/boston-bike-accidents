"""
Module for generating interactive maps using Folium.

This module provides functions to create interactive maps using Folium library,
overlaying GeoJson data, generating heat maps, and adding street data layers.

Dependencies:
    Folium: A Python wrapper for Leaflet.js mapping library.
    Pandas: A powerful data manipulation library.
    Geopandas: Extends pandas to allow spatial operations on geometric types.
    Folium.plugins.HeatMap: Plugin for creating heatmaps in Folium.

Functions:
    get_map(path, lat, lon, zoom): Generates a Folium map centered at the
    specified latitude and longitude with the given zoom level, and overlays a
    GeoJson file onto the map.

    get_heat_map(data: pd.DataFrame, m): Generates a heat map layer based on
    geographical data.

    get_street_data(path, m): Retrieves street data from a GeoJSON file and
    adds it as a GeoJson layer to a folium.Map.
"""

import folium
import pandas as pd
from folium.plugins import HeatMap
import geopandas as gpd


def get_map(path, lat, lon, zoom):
    """
    Generates a Folium map centered at the specified latitude and longitude with
    the given zoom level, and overlays a GeoJson file onto the map.

    Parameters:
        path (str): The file path to the GeoJson data.
        lat (float): Latitude coordinate for the center of the map.
        lon (float): Longitude coordinate for the center of the map.
        zoom (int): Zoom level of the map (0-18, higher values for closer zoom).

    Returns:
        folium.Map: Folium map object with GeoJson overlay.s
    """
    folium_map = folium.Map(
        location=[lat, lon], zoom_start=zoom, tiles="CartoDB positron"
    )
    folium.GeoJson(path, name="boston").add_to(folium_map)
    return folium_map


def get_heat_map(data: pd.DataFrame, folium_map):
    """
    Generates a heat map layer based on geographical data.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame containing latitude and
        longitude coordinates.
        m (folium.Map): An instance of folium.Map to which the heat map layer
        will be added.

    Returns:
        folium.Map: The folium.Map instance with the heat map layer added.
    """
    points = [(row["lat"], row["long"]) for index, row in data.iterrows()]
    HeatMap(
        points,
        radius=15,
        opacity=0.6,
        blur=7,
        gradient={0.4: "blue", 0.65: "lime", 1: "red"},
        colormap="viridis",
    ).add_to(folium_map)
    return folium_map


def get_street_data(path, folium_map):
    """
    Retrieves street data from a GeoJSON file and adds it as a GeoJson layer to
    a folium.Map.

    Parameters:
        path (str): The file path to the GeoJSON file containing street data.
        m (folium.Map): An instance of folium.Map to which the street data layer
        will be added.

    Returns:
        folium.Map: The folium.Map instance with the street data layer added.
    """
    street_data = gpd.read_file(path)

    folium.GeoJson(
        street_data,
        name="Streets",
        style_function=lambda x: {"color": "blue", "weight": 1, "opacity": 0.6},
    ).add_to(folium_map)

    folium.LayerControl().add_to(folium_map)
    return folium_map

"""
Module for handling data retrieval and manipulation.

This module provides functions to pull data from a specified URL, save it as
JSON, load data from a JSON file, and retrieve filtered bike data from a
specified URL.

Dependencies:
    - json: Module for encoding and decoding JSON data.
    - urllib.request: Module for opening URLs.
    - Pandas: A powerful data manipulation library.

Functions:
    - pull_data(url, data_name="data"): Pulls data from a specified URL and
    saves it as a JSON file.
    - load_data(path): Loads data from a specified path and returns it as a
    pandas DataFrame.
    - get_bike_data(path): Retrieves bike data from a specified URL, filters
    records for mode type 'bike', and returns the filtered data as a pandas
    DataFrame.
"""

import json
import urllib.request
import pandas as pd


def pull_data(url, data_name="data"):
    """
    Pull data from a specified URL and save it as a JSON file.

    Parameters:
        url (str): The URL from which to pull the data.
        data_name (str): The name of the JSON file to be saved.

    Returns:
        None
    """
    fileobj = urllib.request.urlopen(url)
    response_dict = json.loads(fileobj.read())
    with open(f"data/{data_name}", "w", encoding="utf-8") as file:
        json.dump(response_dict, file)
    return data_name


def load_data(path):
    """
    Load data from a specified path and save it as a variable

    Parameters:
        path (str): The name of the file in the data folder

    Returns:
        The specified json file in pandas DataFrame format
    """
    return pd.read_json(f"data/{path}")["result"]


def get_bike_data(path):
    """
    Retrieves bike data from a specified URL, filters records for mode type
    'bike', and returns the filtered data as a pandas DataFrame.

    Parameters:
        URL (str): The URL from which to pull the data.

    Returns:
        pandas.DataFrame: DataFrame containing filtered bike data.
    """
    bike_data = pd.DataFrame(load_data(path)["records"])
    bike_data = bike_data[bike_data["mode_type"] == "bike"].reset_index()
    return bike_data

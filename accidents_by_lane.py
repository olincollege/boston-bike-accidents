"""
Description: This is a python script that organized bike accidents in Boston
                    based on where they occured. It then generates two graphs
                    to show the relative safety of each type of bike lane or no
                    bike lane.
Name: Kenneth Xiong + Toby Mallon
Class: SoftDes SP 24
"""

import warnings
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import helpers


def load_data(bike_accidents_url, bike_lane_url):
    """
    Loads data from API into two json files and converts them
    into Pandas Dataframs

    Parameters:
        bike_accidents_url: URL for bike accident data.
        bike_lane_url: URL for bike lane data

    Returns:
        bike_accident_df: Pandas Dataframe for bike accidents data
        bike_lane_df: Pandas Dataframe for bike lane data
    """
    bike_accidents_path = helpers.pull_data(
        bike_accidents_url, "bike_accident_df.json"
    )
    bike_lane_path = helpers.pull_data(bike_lane_url, "bike_lane_df.json")
    bike_accident_df = helpers.get_bike_data(bike_accidents_path)
    bike_lane_df = pd.DataFrame(helpers.load_data(bike_lane_path)["records"])
    return bike_accident_df, bike_lane_df


def abbreviate_street_names(bike_accident_df, bike_lane_df):
    """
    Abbreviates street names in two datasets for consistency.

    Parameters:
        bike_accident_df (pandas.DataFrame): Bike accident data.
        bike_lane_df (pandas.DataFrame): Bike lane data.

    Returns:
    Tuple (bike_accident_df, bike_lane_df):
        bike_accident_df (pandas.DataFrame): Data with abbreviated street names.
        bike_lane_df (pandas.DataFrame): Data with abbreviated street names.

    """
    bike_lane_df["STREET_NAM"] = bike_lane_df["STREET_NAM"].str.upper()
    bike_lane_df.head()
    abbreviations = {
        "NORTH": "N",
        "SOUTH": "S",
        "EAST": "E",
        "WEST": "W",
        "STREET": "ST",
        "ROAD": "RD",
        "AVENUE": "AVE",
        "PARKWAY": "PKWY",
        "BOULEVARD": "BLVD",
        "DRIVE": "DR",
    }
    # abbreviating street names in dataset to make them match
    for row_index in range(len(bike_lane_df["STREET_NAM"])):
        street_list = bike_lane_df["STREET_NAM"][row_index].split()
        for street_index, word in enumerate(street_list):
            if word in abbreviations:
                street_list[street_index] = abbreviations[word]
        bike_lane_df.at[row_index, "STREET_NAM"] = " ".join(street_list)
    # abbreviating street names in dataset to make them match
    for row_index in range(len(bike_accident_df["street"])):
        column_names = ["street", "xstreet1", "xstreet2"]
        for column in column_names:
            if bike_accident_df[column][row_index] is not None:
                street_list = bike_accident_df[column][row_index].split()
                for street_index, word in enumerate(street_list):
                    if word in abbreviations:
                        street_list[street_index] = abbreviations[word]
                bike_accident_df.at[row_index, column] = " ".join(street_list)

    return bike_accident_df, bike_lane_df


def find_non_street_accidents(lane_type_dict, bike_accident_df):
    """
    Finds accidents not occurring on streeets(i.e intersections).

    Parameters:
        lane_type_dict (dict): A dictionary to store accident counts.
        bike_accident_df (pandas.DataFrame): DataFrame with bike accident data.

    Returns:
        None
    """
    # we don't consider interaction to add to any bike lane category
    intersection_crash_df = bike_accident_df[
        bike_accident_df["location_type"] == "Intersection"
    ]
    other_crash_df = bike_accident_df[
        bike_accident_df["location_type"] == "Other"
    ]
    lane_type_dict["intersection"] = intersection_crash_df.shape[0]
    lane_type_dict["other"] = other_crash_df.shape[0]


def find_street_accidents(lane_type_dict, bike_accident_df, bike_lane_df):
    """
    Categorizes accidents that happened on streets

    Parameters:
        lane_type_dict (dict): A dictionary to store accident counts.
        bike_accident_df (pandas.DataFrame): DataFrame with bike accident data.
        bike_lane_df (pandas.DataFrame): DataFrame containing bike lane data.

    Returns:
        None
    """
    warnings.simplefilter(action="ignore", category=UserWarning)
    # read in geojson file of bike lanes
    bike_lanes = gpd.read_file("data/Existing_Bike_Network_2023.geojson")
    street_crash_df = bike_accident_df[  # sort by street accidents
        bike_accident_df["location_type"] == "Street"
    ].reset_index()
    # find indices of accidents on streets w/o bike lanes to remove
    remove_index_list = []
    for row_index in range(len(street_crash_df["street"])):
        if (
            street_crash_df["street"][row_index]
            not in bike_lane_df["STREET_NAM"].values
        ):
            lane_type_dict["none"] += 1
            remove_index_list.append(row_index)
    # remove those points
    filtered_street_crash_df = street_crash_df.drop(remove_index_list)
    # convert to geojson points/geopandas DF
    geometry = [
        Point(xy)
        for xy in zip(
            filtered_street_crash_df["long"], filtered_street_crash_df["lat"]
        )
    ]
    bike_crash_gdf = gpd.GeoDataFrame(
        filtered_street_crash_df, crs="EPSG:4326", geometry=geometry
    )
    # add a buffer to points to account for error
    bike_crash_gdf["geometry"] = bike_crash_gdf.geometry.buffer(0.000127)
    # overlap accidents with our  bike lanes data to find where they occured
    street_crash_gdf = gpd.sjoin(
        bike_lanes, bike_crash_gdf, how="inner", predicate="intersects"
    )
    # remove duplicates
    street_crash_gdf.drop_duplicates(subset=["STREET_NAM", "ExisFacil", "_id"])
    # count how many in each type of bike lane
    accident_occurences = street_crash_gdf["ExisFacil"].value_counts()
    for index, accident in enumerate(accident_occurences):
        lane_type_dict[accident_occurences.index[index]] = accident


def organize_by_lane(bike_accident_df, bike_lane_df):
    """
    Organizes crashes by where they occured.

    Parameters:
        bike_accident_df (pandas.DataFrame): DataFrame with bike accident data.
        bike_lane_df (pandas.DataFrame): DataFrame containing bike lane data.

    Returns:
        A dictionary organizing crashes by bike lane presence.
    """
    lane_type_dict = {
        "intersection": 0,
        "none": 0,
    }
    bike_accident_df, bike_lane_df = abbreviate_street_names(
        bike_accident_df, bike_lane_df
    )
    find_non_street_accidents(lane_type_dict, bike_accident_df)
    find_street_accidents(lane_type_dict, bike_accident_df, bike_lane_df)
    return lane_type_dict


def lanes_by_percent(bike_lane_df):
    """
    Calculates the percentage of each bike lane based on the len compared
    to the total length of all roads in Boston.

    Parameters:
        bike_lane_df (pandas.DataFrame): DataFrame containing bike lane data.

    Returns:
        a dictionary breaking down bike lanes by percent.
    """
    url = (
        "https://data.boston.gov/api/3/action/datastore_search?resource_id="
        + "6fa7932b-7bc8-42bc-9250-168d5f5dc1ad&limit=49000"
    )
    helpers.pull_data(url, "road_data.json")  # get all boston roads
    road_data = pd.DataFrame(helpers.load_data("road_data.json")["records"])
    # find the total length
    total_length = road_data["SHAPESTLength"].astype(float).sum()
    # find total length of bike lanes by type
    bike_lane_df["Shape_Leng"] = bike_lane_df["Shape_Leng"].astype(float)
    bike_lane_lengths = bike_lane_df.groupby("ExisFacil")["Shape_Leng"].sum()
    # convert to percentages
    bike_lane_percents = bike_lane_lengths / total_length

    return bike_lane_percents


def normalize_data(lane_type_dict, bike_lane_df):
    """
    Normalize accidents data to be percentages summing to one

    Parameters:
        lane_type_dict (dict): Dictionary with accident counts by lane type.
        bike_lane_df (pandas.DataFrame): DataFrame containing bike lane data.

    Returns:
    Tuple (lane_distr_dict, accident_percent_dict):
        lane_distr_dict (dict): A dictionary with normalized accident counts.
        accident_percent_dict (dict): A dictionary with percents of each lane.
    """
    bike_lane_percents = lanes_by_percent(bike_lane_df)
    lane_distr_dict = {}
    # calculate distribution of bike lanes in boston
    for index in bike_lane_percents.index:
        if index in lane_type_dict.keys():
            lane_distr_dict[index] = bike_lane_percents[index]
    # we consider non bike lane accidents to be in the same category
    non_bike_lane_sum = (
        lane_type_dict["intersection"]
        + lane_type_dict["none"]
        + lane_type_dict["other"]
    )
    non_bike_lane_percent = (
        1 - sum(bike_lane_percents.values)
    ) / non_bike_lane_sum
    # calculate percents based on the non bike lane percent
    lane_distr_dict["intersection"] = (
        lane_type_dict["intersection"] * non_bike_lane_percent
    )
    lane_distr_dict["none"] = lane_type_dict["none"] * non_bike_lane_percent
    lane_distr_dict["other"] = lane_type_dict["other"] * non_bike_lane_percent
    # calculate distribution of accidents in Boston
    accident_percent_dict = {}
    for key in lane_type_dict.keys():
        accident_percent_dict[key] = lane_type_dict[key] / sum(
            lane_type_dict.values()
        )
    # sort from greatest to least
    lane_distr_dict = dict(
        sorted(lane_distr_dict.items(), key=lambda item: item[1], reverse=True)
    )
    accident_percent_dict = {
        key: accident_percent_dict[key] for key in lane_distr_dict
    }
    # normalize to add up to 100 instead of one
    for key in lane_distr_dict:
        lane_distr_dict[key] *= 100
        accident_percent_dict[key] *= 100

    return lane_distr_dict, accident_percent_dict


def visualize_data(bike_accidents_url, bike_lane_url):
    """
    Creates two bar graphs which break down bike accidents by percent and number

    Parameters:
        bike_accidents_url: The url to load bike accident data from api.
        bike_lane_path: The url to load bike lane data from api.

    Returns:
        None
    """
    bike_accident_df, bike_lane_df = load_data(
        bike_accidents_url, bike_lane_url
    )
    lane_type_dict = organize_by_lane(bike_accident_df, bike_lane_df)
    lane_distr_dict, accident_percent_dict = normalize_data(
        lane_type_dict, bike_lane_df
    )
    # plot all the data
    plt.figure(figsize=(15, 15))
    accident_percents = plt.bar(
        list(lane_distr_dict.keys()),
        list(lane_distr_dict.values()),
        edgecolor="white",
    )
    bike_lane_percents = plt.bar(
        list(lane_distr_dict.keys()), list(accident_percent_dict.values())
    )

    plt.legend(["Distribution of Accidents", "Distribution of Bike Lanes"])
    for val in bike_lane_percents:
        yval = val.get_height()
        plt.text(
            val.get_x() + val.get_width() / 2,
            yval,
            round(yval, 1),
            ha="center",
            va="bottom",
        )
    for val in accident_percents:
        yval = val.get_height()
        plt.text(
            val.get_x() + val.get_width() / 2,
            yval,
            round(yval, 1),
            ha="center",
            va="top",
        )
    plt.title("Percentage of Bike Accidents by Category")
    plt.ylabel("Percent(%)")
    plt.xlabel("Lane Type")

    plt.show()

    plt.figure(figsize=(15, 15))
    bike_lane_counts = plt.bar(
        list(lane_type_dict.keys()), list(lane_type_dict.values())
    )
    for val in bike_lane_counts:
        yval = val.get_height()
        plt.text(
            val.get_x() + val.get_width() / 2,
            yval,
            round(yval, 3),
            ha="center",
            va="bottom",
        )
    plt.legend(["Number of Accidents"])
    plt.title("Number of Bike Accidents by Category")
    plt.ylabel("Count")
    plt.xlabel("Lane Type")
    plt.show()

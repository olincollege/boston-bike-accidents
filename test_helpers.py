"""
Test module for verifying the functionality of data processing functions.

This module contains test cases for testing the following functions:
- pull_data: Function to pull data from a specified URL and save it as a JSON
file.
- load_data: Function to load data from a JSON file.
- get_bike_data: Function to extract bike-related data from loaded data.

Each test case is designed to validate the correctness of these functions and
ensure they operate as expected.

Attributes:
    TEST_URL (str): The URL from which data is pulled for testing.
    TEST_DATA_NAME (str): The name of the test data file.
    TEST_PATH (str): The path to the test data file.

"""

import os
import pytest
import pandas as pd
from helpers import pull_data, load_data, get_bike_data

TEST_URL = (
    "https://data.boston.gov/api/3/action/datastore_search?resource_id"
    + "=e4bfe397-6bfc-49c5-9367-c879fac7401d&limit=49000"
)
TEST_DATA_NAME = "test_data.json"
TEST_PATH = f"data/{TEST_DATA_NAME}"


@pytest.fixture(scope="module")
def setup_teardown():
    """
    Teardown function to remove the file at TEST_PATH if it exists.
    """
    yield
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)


# pylint: disable=W0621
# pylint: disable=W0613
def test_pull_data(setup_teardown):
    """
    Test case to verify the correctness of the pull_data function.

    Parameters:
        setup_teardown (fixture): Fixture for setup and teardown of test
        environment.

    Raises:
        AssertionError: If the result returned by the pull_data function does
        not match the expected data name or if the JSON file at TEST_PATH does
        not exist.
    """
    expected_data_name = TEST_DATA_NAME

    result = pull_data(TEST_URL, data_name=TEST_DATA_NAME)

    assert result == expected_data_name
    assert os.path.exists(TEST_PATH)


def test_load_data(setup_teardown):
    """
    Test case to verify the correctness of the load_data function.

    Parameters:
        setup_teardown (fixture): Fixture for setup and teardown of test
        environment.

    Raises:
        AssertionError: If the result obtained from load_data function does not
        match the expected data.

    """
    pull_data(TEST_URL, data_name=TEST_DATA_NAME)

    expected_data = pd.read_json(TEST_PATH)["result"]

    result = load_data(TEST_DATA_NAME)

    assert result.equals(expected_data)


def test_get_bike_data(setup_teardown):
    """
    Test case to verify the correctness of the get_bike_data function.

    Parameters:
        setup_teardown (fixture): Fixture for setup and teardown of test
        environment.

    Raises:
        AssertionError: If the expected bike data does not match the filtered
        bike data.

    """
    pull_data(TEST_URL, data_name=TEST_DATA_NAME)
    expected_data = get_bike_data(TEST_DATA_NAME)

    bike_data = pd.DataFrame(load_data(TEST_DATA_NAME)["records"])
    bike_data = bike_data[bike_data["mode_type"] == "bike"].reset_index()

    assert expected_data.equals(bike_data)

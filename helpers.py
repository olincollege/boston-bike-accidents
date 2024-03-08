import json
import urllib.request


def load_data(url, data_name):
    """
    Load data from a specified URL and save it as a JSON file.

    Parameters:
        url (str): The URL from which to load the data.
        data_name (str): The name of the JSON file to be saved.

    Returns:
        None
    """
    fileobj = urllib.request.urlopen(url)
    response_dict = json.loads(fileobj.read())
    with open(f"data/{data_name}.json", "w", encoding="utf-8") as file:
        json.dump(response_dict, file)

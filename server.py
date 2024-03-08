import json
import urllib.request

URL = (
    "https://data.boston.gov/api/3/action/datastore_search?resource_id"
    "=e4bfe397-6bfc-49c5-9367-c879fac7401d"
)
fileobj = urllib.request.urlopen(URL)
response_dict = json.loads(fileobj.read())
with open(
    "boston-bike-accidents/data/bike_data.json", "w", encoding="utf-8"
) as file:
    json.dump(response_dict, file)

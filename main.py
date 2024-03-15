import folium
import pandas as pd

import helpers

URL = (
    "https://data.boston.gov/api/3/action/datastore_search?resource_id"
    + "=e4bfe397-6bfc-49c5-9367-c879fac7401d&limit=10000"
)

helpers.pull_data(URL, "bike_data")

data = pd.DataFrame(helpers.load_data("/bike_data.json")["records"])

GEOJSON_PATH = "data/City_of_Boston_Boundary_(Water_Excluded).geojson"

m = folium.Map(location=[0, 0], zoom_start=2)

folium.GeoJson(GEOJSON_PATH, name="boston").add_to(map)

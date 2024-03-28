# Boston Bike Accidents Project Documentation

This repository contains the notebook which explores bicycle related accidents in Boston categorized by bike lane. It included all the modules and data required to run the notebook

## Repository Contents

- `data/`: A folder containing all the datasets we used as JSON or geoJSON files.
- `accidents_by_lane.py`: A Python module which creates a two graphs showing bike accidents sorted by bike lanes.
- `comp_essay.ipynb`: A Jupyter notebook file with analyses and implementation of the modules.
- `heatmap.py`: A Python module which creates a heatmap of bike accidents in Boston.
- `helpers.py`: A Python module to help load in data.
- `test_helpers.py`: Unit tests for modules.
- `graphs/`: A directory containing graphs in JPG format that visualize various aspects of the robot's performance.
- `pyproject.toml`: Config file for pylint black
- `requirements.txt`: Required packages


## Usage

To use this repository, clone it to your local machine and run `pip install requirements.txt` to download the required packages. Then, run `comp_essay.ipynb` starting from the first cell.

## Data Source

All data was obtained from [https://data.boston.gov/](https://data.boston.gov/). The datasets are as follows:
- [Existing Bike Network 2023](https://data.boston.gov/dataset/existing-bike-network-2023), 
- [Vision Zero Crash Records](https://data.boston.gov/dataset/vision-zero-crash-records), 
- [Boston Street Segments](https://data.boston.gov/dataset/boston-street-segments),
- [City of Boston Boundary(Water Excluded)](https://data.boston.gov/dataset/city-of-boston-boundary-water-excluded). 

## Data Visualization

To create graphs shown in the notebook, run the following code. 

For the heatmap:

    import heatmap
    import helpers
    import geopandas as gpd
    import folium
    GEOJSON_PATH = "data/City_of_Boston_Boundary_(Water_Excluded).geojson"
    STREET_GEOJSON_PATH = "Boston_Street_Segments.geojson"

    bike_data = helpers.get_bike_data('/bike_data.json')

    m = heatmap.get_map(GEOJSON_PATH, 42.3601, -71.0589, 14)
    m = heatmap.get_heat_map(bike_data, m)
    m = heatmap.get_street_data(STREET_GEOJSON_PATH, m)

    m

For the bar graphs:
    
    import accidents_by_lane
    accidents_url = ("https://data.boston.gov/api/3/action/datastore_search?resource_id"
        + "=e4bfe397-6bfc-49c5-9367-c879fac7401d&limit=49000")
    bike_lane_url = ("https://data.boston.gov/api/3/action/datastore_search?resource_id" +
        "=14e7e1a7-ffe0-4ae7-a6b4-3975fa32e879&limit=49000")
    accidents_by_lane.visualize_data(accidents_url, bike_lane_url)
## Contributing

This project is an educational exercise, and contributions are not actively sought. However, feedback and suggestions are welcome.

## License

This project is provided for educational use only and is not licensed for commercial use.

## Contact

For any queries regarding this project, please reach out to the repository maintainer.
import pandas as pd
import os
import geopandas as gpd


def data_loader(path='../data/', city='London'):
    """Read data for a given city, put them in a dict
    with same key as file name.
    Example: london_underground_station_info.csv
    corresponds to the entry 'london_underground_station_info'.
    """
    full_path = path + city + '/'
    return dict(
        zip(
            [dataset.split('.')[0] for dataset in os.listdir(full_path)],
            [pd.read_csv(full_path + dataset, encoding='latin1', low_memory=False)
             for dataset in os.listdir(full_path)]
        )
    )


def load_satisfaction(path='../data/London_satisfaction/', transpose=True):
    """Load satisfaction poll for LDN (from London datastore).
    """
    dfs = dict(
        zip(
            [dataset.split('.')[0] for dataset in os.listdir(path)],
            [pd.read_csv(path + dataset, encoding='latin1', low_memory=False)
             for dataset in os.listdir(path)]
        )
    )

    if transpose:
        for key, df in dfs.items():
            df = df.T
            columns = df.loc['area'].to_list()
            df = df.iloc[1:]
            df.columns = columns
            dfs[key] = df
    return dfs

def load_pubs_data(global_path: str) -> (pd.DataFrame, pd.DataFrame):
    """
    Treat the data from  https://data.london.gov.uk/dataset/pubs-clubs-restaurants-takeaways-borough
    :param global_path: str, global path to the data
    :return: (pd.DataFrame, pd.DataFrame), (number of pubs in the borough, pubs employment in the borough)
    """
    # Load data
    pubs = pd.read_csv(global_path + 'london_data_pubs.csv')
    pubs_employment = pd.read_csv(global_path + 'london_data_pubs_employment.csv')

    # Treat the data
    for df in [pubs, pubs_employment]:
        df.set_index('area', inplace=True)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: int(x.replace(',', ''))).astype(int)

    return pubs, pubs_employment


def get_path_london_boroughs(global_path: str = '../data/') -> str:
    """
    Get the path to London boroughs. If the file doesn't exist, it will automatically make this file.
    :param global_path: str, path to the data directory
    :return: str, path to London boroughs (in GeoJSON)
    """
    path_london_borough = global_path + "london-borough.json"
    if not os.path.exists(path_london_borough):
        # Load json
        data_source = global_path + 'statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp'
        data = gpd.read_file(data_source)

        # Transform cordinates
        data['geometry'] = data['geometry'].to_crs(epsg=4326)
        data.to_file(path_london_borough, driver="GeoJSON")
        print("GeoJSON saved at: " + path_london_borough)
    return path_london_borough

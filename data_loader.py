import pandas as pd
import os


def data_loader(path='datasets_full/', city='London'):
    """Read data for a given city, put them in a dict
    with same key as file name.
    Example: london_underground_station_info.csv
    corresponds to the entry 'london_underground_station_info'.
    """
    full_path = path + city + '/'
    return dict(
        zip(
            [dataset.split('.')[0] for dataset in os.listdir(full_path)],
            [pd.read_csv(full_path + dataset, encoding='latin1')
             for dataset in os.listdir(full_path)]
        )
    )

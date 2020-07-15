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

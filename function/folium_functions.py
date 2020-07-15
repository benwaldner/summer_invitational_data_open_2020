import pandas as pd
from typing import Dict
import folium


def pipeline_stations(filename_stations: str, max_zone: int = None, current_map: folium.folium.Map = None) -> Dict[(float, float)]:
    """
    Map the stations if coordinates (latitude, longitude), if one provide a map, it will plot the station on it.
    :param filename_stations: str, the path to stations csv
    :param max_zone: int, zone max to take into account for the plot part
    :param current_map: folium.folium.Map, map
    :return: dict, map of the stations and coordinates (latitude, longitude)
    """
    # Load stations data
    df = pd.read_csv(filename_stations)
    df['Zone'].fillna('8', inplace=True)

    # Map station with coordinates
    unique_stations = df['Station'].unique()
    df.set_index('Station', inplace=True)
    map_station_to_coordinates = {station: (df.loc[station]['Latitude'],
                                            df.loc[station]['Longitude']) for station in unique_stations}

    # Plot the station on the provided map
    if current_map is not None:
        if max_zone is None:
            for station in unique_stations:
                folium.Marker(map_station_to_coordinates[station], popup=station,
                              icon=folium.Icon(icon='subway', prefix='fa')).add_to(current_map)
        else:
            mask_stations = [station for station in unique_stations
                             if int(df.loc[station]['Zone'].split(',')[0]) <= max_zone]
            for station in mask_stations:
                folium.Marker(map_station_to_coordinates[station], popup=station,
                              icon=folium.Icon(icon='subway', prefix='fa')).add_to(current_map)

    return map_station_to_coordinates


def pipeline_lines(filename_lines: str, filename_stations: str, current_map: folium.folium.Map = None):
    """
    Add to a provided folium map the tubes lines.
    :param filename_lines: str, path to lines csv
    :param filename_stations: str, path to stations csv
    :param current_map: folium.folium.Map, map
    :return: Nothing
    """
    # Load stations data
    df = pd.read_csv(filename_lines)
    dic_stations = pipeline_stations(filename_stations)

    # Get stations for each line
    unique_lines = df['Tube Line'].unique()
    df.set_index('Tube Line', inplace=True)

    # We create a feature group (layer) for each set line
    dic = {line: folium.FeatureGroup(name=line) for line in unique_lines}

    # Add trajectories
    for line in unique_lines:
        infos_line = df.loc[line]
        if len(infos_line) > 2:
            for index, row in infos_line.iterrows():
                # Find start and end stations
                start_station = row['From Station']
                end_station = row['To Station']

                # Add to the correct layer
                folium.PolyLine((dic_stations[start_station], dic_stations[end_station])).add_to(dic[line])

    # Add to current map
    for line in dic:
        dic[line].add_to(current_map)

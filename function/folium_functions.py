import pandas as pd
from typing import Dict
import io
from PIL import Image
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


def pipeline_venues(filename_venues: str, current_map: folium.folium.Map = None) -> Dict[(float, float)]:
    """
    Map the venues if coordinates (latitude, longitude), if one provide a map, it will plot the station on it.
    :param filename_stations: str, the path to stations csv
    :param current_map: folium.folium.Map, map
    :return: dict, map of the stations and coordinates (latitude, longitude)
    """
    # Load stations data
    df = pd.read_csv(filename_venues)

    # Map station with coordinates
    unique_venues = df['Venue'].unique()
    df.set_index('Venue', inplace=True)
    map_venue_to_coordinates = {venue: (df.loc[venue]['Latitude'],
                                            df.loc[venue]['Longitude']) for venue in unique_venues}

    # Plot the station on the provided map
    if current_map is not None:
        for venue in unique_venues:
            if venue == 'Olympic Park - Olympic Stadium':
                icon = 'glyphicon glyphicon-tower'
            else:
                icon = 'glyphicon glyphicon-screenshot'
            folium.Marker(map_venue_to_coordinates[venue], popup=venue,
                          icon=folium.Icon(icon=icon)).add_to(current_map)

    return map_venue_to_coordinates


def get_raw_map() -> folium.Map:
    """
    Make a folium map centered on London.
    :return: folium.Map
    """
    return folium.Map(location=[51.505453, -0.268839])


def save_map(m: folium.Map, filename: str='', render_time: int=5) -> None:
    """
    Wrapper to convert a folium map to .png and save itself.

    Warning: to install it, you need selenium (pip install selenium),
    and a browser specific executable. For firefox it is geckodriver.
    1) download the latest version
    2) make it executable: chmod +x geckodriver
    3) move it where it needs to be : sudo mv geckodriver /usr/local/bin/
    (adding the path to geckdriver to $PATH supposedly works too, but
    only the above worked for me).

    :param m: folium.Map,
    :param filename: str, path to save map as .png
    :param render_time: int, time to render as .png
    :return: None
    """
    img_data = m._to_png(render_time)
    img = Image.open(io.BytesIO(img_data))
    img.save(filename)

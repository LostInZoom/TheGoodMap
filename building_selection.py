import geopandas as gpd
from configparser import ConfigParser
import psycopg2

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def load_buildings(layername):
    # connect to the PostGIS database
    config = load_config()
    conn = connect(config)
    query = "SELECT * FROM public.\"{}\"".format(layername)
    df_buildings = gpd.GeoDataFrame.from_postgis(query, conn)

    return df_buildings

def building_selection(layername, area_threshold, output):
    df_buildings = load_buildings(layername)
    selected_buildings = []
    for idx, row in df_buildings.iterrows():
        geometry = row['geom']
        if(geometry.area >= area_threshold):
            selected_buildings.append(row)
    
    new_df = gpd.GeoDataFrame(selected_buildings,geometry='geom',columns=['geom','nature'])
    new_df.to_file(output)

building_selection("aggregated_buildings",15.0,"buildings_z18.shp")
building_selection("aggregated_buildings",30.0,"buildings_z17.shp")
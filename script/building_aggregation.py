import geopandas as gpd
from configparser import ConfigParser
import psycopg2
from shapely import wkb
from shapely.ops import unary_union
from shapely.geometry import Polygon, LineString

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

# for a 3d sequence of coordinates, returns the 2d sequence. Useful to convert 3d points to 2d points
def to_2d(x, y, z):
    return tuple(filter(None, [x, y]))


# for an array of 3d sequences of coordinates, returns an array containing the 2d sequences. Useful to convert 3d geometries to 2d geometries
def array_to_2d(array):
    array_2d = []
    for tuple in array:
       array_2d.append(to_2d(tuple[0],tuple[1],tuple[2]))
    return array_2d

def polygon_3d_to_2d(polygon):
    # outer ring
    coords_2d = array_to_2d(polygon.exterior.coords)
    # inner rings
    interiors = []
    for interior in polygon.interiors:
        interiors.append(array_to_2d(interior.coords))

    return Polygon(coords_2d,interiors)

def load_buildings(layername):
    # connect to the PostGIS database
    config = load_config()
    conn = connect(config)
    query = "SELECT * FROM public.\"{}\"".format(layername)
    df_buildings = gpd.GeoDataFrame.from_postgis(query, conn)

    return df_buildings

def aggregate_touching_buildings(grid_file, buildings_layer, output, i, j):
    config = load_config()
    conn = connect(config)
    grid = gpd.read_file(grid_file)

    # create the output table in the PostGIS database
    cursor = conn.cursor()
    if(i == 0):
        cursor.execute("CREATE TABLE public.\"{}\" (id serial PRIMARY KEY, geom geometry, nature character varying(34));".format(output))
    
    for idx, row in grid.iterrows():
        print(idx)
        if(idx < i):
            continue
        if(idx > j):
            continue
        clusters = []
        geometry = row['geometry']
        geom_text = geometry.wkt
        #print(geom_text)
        query = "SELECT * FROM public.\"{}\" x WHERE ST_Within(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(buildings_layer, geom_text)
        df_buildings = gpd.GeoDataFrame.from_postgis(query, conn)
        build_list = list(df_buildings["id_1"])
        while(len(build_list) > 0):
            #print("{} elements in the main stack".format(len(build_list)))
            building = build_list.pop(0)
            cluster = []
            stack = [building]
            while(len(stack) > 0):
                current = stack.pop(0)
                #print(current)
                cluster.append(current)
                cur = conn.cursor()
                query_geom = "SELECT * FROM public.\"{}\" x WHERE x.id_1={}".format(buildings_layer,current)
                cur.execute(query_geom)
                feature = cur.fetchone()
                geom = wkb.loads(feature[1], hex=True)
                geom_text = geom.wkt
                query = "SELECT * FROM public.\"{}\" x WHERE ST_Touches(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(buildings_layer,geom_text)
                neighbors = list(gpd.GeoDataFrame.from_postgis(query, conn)["id_1"])

                for element in stack:
                    if element in neighbors:
                        neighbors.remove(element)
                for element in cluster:
                    if element in neighbors:
                        neighbors.remove(element)

                for neighbor in neighbors:
                    stack.append(neighbor)

                cur.close()
            clusters.append(cluster)
            for element in cluster:
                if element in build_list:
                    build_list.remove(element)
        
        # Dissolve each cluster into a single building
        cur = conn.cursor()
        for cluster in clusters:
            # simple case with only one building
            if len(cluster) == 1:
                query = "SELECT * FROM public.\"{}\" x WHERE x.id_1={}".format(buildings_layer,cluster[0])
                cur.execute(query)
                feature = cur.fetchone()
                # keep only three fields id, geometry, nature
                geom = polygon_3d_to_2d(wkb.loads(feature[1], hex=True).geoms[0])
                nature = feature[4]
                q = "INSERT INTO public.\"{}\" (geom, nature) VALUES (ST_SetSRID(ST_GeomFromText('{}'),2154), '{}')".format(output, geom.wkt, nature)
                cur.execute(q)
            # case with several buildings to merge
            else:
                polygons = []
                nature = "Indifférenciée"
                for building in cluster:
                    query = "SELECT * FROM public.\"{}\" x WHERE x.id_1={}".format(buildings_layer,building)
                    cur.execute(query)
                    feature = cur.fetchone()
                    polygons.append(polygon_3d_to_2d(wkb.loads(feature[1], hex=True).geoms[0]))
                    nature_current = feature[4]
                    if nature_current != nature and nature_current != "Indifférenciée":
                        nature = nature_current
                print(polygons)
                geom = unary_union(polygons)
                cur.execute("INSERT INTO public.\"{}\" (geom, nature) VALUES (ST_SetSRID(ST_GeomFromText('{}'),2154), '{}')".format(output, geom.wkt, nature))
        cur.close()
    conn.commit()
    cursor.close()    
    conn.close()

def aggr_nature(series):
    nature1 = series.iloc[0]
    nature2 = series.iloc[1]
    if nature1 == "Indifférenciée":
        return nature2
    if nature2 == "Indifférenciée":
        return nature1
    else: 
        return nature1

def remove_duplicates(grid, building_layer):
    config = load_config()
    conn = connect(config)
    grid = gpd.read_file(grid)
    cursor = conn.cursor()

    for idx, row in grid.iterrows():
        print(idx)
        geometry = LineString(row['geometry'].exterior.coords)
        geom_text = geometry.wkt
        query = "SELECT * FROM public.\"{}\" x WHERE ST_Intersects(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(building_layer, geom_text)
        df_buildings = gpd.GeoDataFrame.from_postgis(query, conn)

        # delete those buildings from the database
        cursor.execute("DELETE FROM public.\"{}\" x WHERE ST_Intersects(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(building_layer, geom_text))

        # create a new column linking intersecting building
        df_buildings['cluster'] = -1
        cluster_id = 0
        for idy, row_b in df_buildings.iterrows():
            id = row_b['cluster']
            if id != -1:
                continue
            geom = row_b['geom']
            intersection = df_buildings['geom'].sindex.query(geom, predicate="intersects")
            row_b['cluster'] = cluster_id
            if len(intersection) > 0:
                df_buildings.at[intersection[0],'cluster'] = cluster_id
            cluster_id += 1


        # merge them two by two, then insert them back into the database
        #print(df_buildings)
        dissolved = df_buildings.dissolve(by='cluster', aggfunc='first')

        # loop on the aggregated dataframe to insert the data into the database
        for idy, row_agg in dissolved.iterrows():
            geom = row_agg['geom']
            nature = row_agg['nature']
            q = "INSERT INTO public.\"{}\" (geom, nature) VALUES (ST_SetSRID(ST_GeomFromText('{}'),2154), '{}')".format(building_layer, geom.wkt, nature)
            cursor.execute(q)
        
    conn.commit()
    cursor.close()    
    conn.close()

def restore_border_buildings(grid, building_layer, aggr_layer):
    config = load_config()
    conn = connect(config)
    grid = gpd.read_file(grid)
    cursor = conn.cursor()
    for idx, row in grid.iterrows():
        print(idx)
        geometry = LineString(row['geometry'].exterior.coords)
        geom_text = geometry.wkt
        query1 = "SELECT * FROM public.\"{}\" x WHERE ST_Intersects(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(building_layer, geom_text)
        query2 = "SELECT * FROM public.\"{}\" x WHERE ST_Intersects(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(aggr_layer, geom_text)
        df_buildings = gpd.GeoDataFrame.from_postgis(query1, conn)
        df_aggr = gpd.GeoDataFrame.from_postgis(query2, conn)
        for idy, row_b in df_buildings.iterrows():
            geom = row_b['geom']
            nature = row_b['nature']
            intersection = df_aggr['geom'].sindex.query(geom, predicate="intersects")
            if len(intersection) > 0:
                continue
            # arrived here, we have to add the current building to the database
            q = "INSERT INTO public.\"{}\" (geom, nature) VALUES (ST_SetSRID(ST_GeomFromText('{}'),2154), '{}')".format(aggr_layer, geom.wkt, nature)
            cursor.execute(q)
        conn.commit()


    conn.commit()
    cursor.close()    
    conn.close()

#aggregate_touching_buildings("zip://grid.zip","batiment_urbain","aggregated_buildings", 501, 557)
#remove_duplicates("zip://grid.zip","aggregated_buildings")
restore_border_buildings("zip://grid.zip","batiment_urbain","aggregated_buildings")

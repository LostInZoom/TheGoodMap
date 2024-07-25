import numpy as np
import geopandas as gpd
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from shapely.geometry import Point

from configparser import ConfigParser
import psycopg2


def geometry_flatten(geom):
  if hasattr(geom, 'geoms'):  # Multi<Type> / GeometryCollection
    for g in geom.geoms:
      yield from geometry_flatten(g)
  elif hasattr(geom, 'interiors'):  # Polygon
    yield geom.exterior
    yield from geom.interiors
  else:  # Point / LineString
    yield geom

def geometry_length(geom):
  return sum(len(g.coords) for g in geometry_flatten(geom))

def polygon_elongation(polygon):
    mbr = polygon.minimum_rotated_rectangle
    coords = mbr.exterior.coords
    length1 = Point(coords[0]).distance(Point(coords[1]))
    length2 = Point(coords[1]).distance(Point(coords[2]))
    if(length1 < length2):
        return length2 / length1
    else:
        return length1 / length2
    
def prepare_datasets(buildings, road_intersections, dataset):
   spatial_index = buildings.sindex
   road_index = road_intersections.sindex
   
   # create new columns
   area =[]
   perimeter = [] 
   vertices = []
   elongation = []
   adjacent = []
   neighbours = []
   road_inter = []
   for idx, row in dataset.iterrows():
      geometry = row['geometry']
      area.append(geometry.area)
      perimeter.append(geometry.length)
      vertices.append(geometry_length(geometry))
      elongation.append(polygon_elongation(geometry))
      adjacent.append(len(spatial_index.query(geometry,predicate="intersects")))
      neighbours.append(len(spatial_index.query(geometry.centroid.buffer(100), predicate="within")))
      road_inter.append(road_index.nearest(geometry,max_distance=250.0,return_all=False,return_distance=True)[1])

   dataset.insert(2, "Vertices", vertices, True)
   dataset.insert(2, "Neighbours", neighbours, True)
   dataset.insert(2, "Adjacent", adjacent, True)
   dataset.insert(2, "Elongation", elongation, True)
   dataset.insert(2, "Perimeter", perimeter, True)
   dataset.insert(2, "Area", area, True)
   dataset.insert(2, "Road_inter", road_inter, True)

   dataset = dataset.drop(['geometry','id','usage2','leger','etat','source','id_source','nb_logts','mat_murs','mat_toits','z_min_sol','z_min_toit','z_max_toit','z_max_sol','origin_bat'], axis = 1)
   dataset['nature'] = dataset['nature'].map({'Chapelle':0,'Château':1, 'Eglise':2, 'Indifférenciée':3, 'Industriel, agricole ou commercial':4, 'Serre':5, 'Silo':6, 'Tour, donjon':7, 'Tribune':8})
   dataset['usage1'] = dataset['usage1'].map({'Agricole':0,'Annexe':1, 'Commercial et services':2, 'Indifférencié':3, 'Industriel':4, 'Religieux':5, 'Résidentiel':6, 'Sportif':7})
   
   return dataset


def train_model(buildings_file, intersections):
  buildings = gpd.read_file(buildings_file)
  road_intersections = gpd.read_file(intersections)

  # get the buildings labelled as important
  important_df = buildings.loc[buildings['important'] == 1]
  nb = len(important_df)
  non_important_df = buildings.loc[buildings['important'] == 0]
  sampled = non_important_df.sample(n=3*nb)

  training = pd.concat([important_df,sampled])
  print(len(training))

  training = prepare_datasets(buildings, road_intersections, training)

  Y = training['important']
  X = training.drop('important', axis=1)

  x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
  rf = RandomForestClassifier(n_estimators=350)
  rf.fit(x_train, y_train)


  y_pred = rf.predict(x_test)
  accuracy = accuracy_score(y_test, y_pred)
  print("Accuracy:", accuracy)
  precision = precision_score(y_test, y_pred)
  print("Precision:", precision)
  recall = recall_score(y_test, y_pred)
  print("Recall:", recall)

  prediction = x_test.assign(Prediction=y_pred)
  print(len(prediction))
  joined = prediction.join(buildings, lsuffix='_caller', rsuffix='')
  print(len(joined))
  gdf = gpd.GeoDataFrame(joined, geometry="geometry",crs="EPSG:2154")

  #gdf.to_file("prediction.shp")
  joblib.dump(rf, "./random_forest.joblib")

def predict(buildings_file, intersections_file, model):
   
   loaded_rf = joblib.load(model)

   buildings = gpd.read_file(buildings_file)
   road_intersections = gpd.read_file(intersections_file)
   prediction_dataset = gpd.GeoDataFrame.copy(buildings)
   dataset = prepare_datasets(buildings, road_intersections, prediction_dataset)

   X = dataset.drop('important', axis=1)
   y = loaded_rf.predict(X)

   return y

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

def prepare_dataset_prediction(buildings, road_intersections, dataset):
   spatial_index = buildings.sindex
   road_index = road_intersections.sindex
   
   # create new columns
   area =[]
   perimeter = [] 
   vertices = []
   elongation = []
   adjacent = []
   neighbours = []
   road_inter = []
   for idx, row in dataset.iterrows():
      geometry = row['geom']
      area.append(geometry.area)
      perimeter.append(geometry.length)
      vertices.append(geometry_length(geometry))
      elongation.append(polygon_elongation(geometry))
      adjacent.append(len(spatial_index.query(geometry,predicate="intersects")))
      neighbours.append(len(spatial_index.query(geometry.centroid.buffer(100), predicate="within")))
      road_inter.append(road_index.nearest(geometry,max_distance=250.0,return_all=False,return_distance=True)[1])

   dataset.insert(2, "Vertices", vertices, True)
   dataset.insert(2, "Neighbours", neighbours, True)
   dataset.insert(2, "Adjacent", adjacent, True)
   dataset.insert(2, "Elongation", elongation, True)
   dataset.insert(2, "Perimeter", perimeter, True)
   dataset.insert(2, "Area", area, True)
   dataset.insert(2, "Road_inter", road_inter, True)
   id0 = dataset.loc[:, 'id_0']
   dataset = dataset.drop(['geom','acqu_plani','acqu_alti','id_1','prec_alti','prec_plani','app_ff','date_app','date_conf','date_maj','date_creat','id','id_0','usage2','leger','etat','source','id_source','nb_logts','mat_murs','mat_toits','z_min_sol','z_min_toit','z_max_toit','z_max_sol','origin_bat'], axis = 1)
   dataset['nature'] = dataset['nature'].map({'Chapelle':0,'Château':1, 'Eglise':2, 'Indifférenciée':3, 'Industriel, agricole ou commercial':4, 'Serre':5, 'Silo':6, 'Tour, donjon':7, 'Tribune':8})
   dataset['usage1'] = dataset['usage1'].map({'Agricole':0,'Annexe':1, 'Commercial et services':2, 'Indifférencié':3, 'Industriel':4, 'Religieux':5, 'Résidentiel':6, 'Sportif':7})
   dataset.insert(0, "id_0", id0, True)
   return dataset

def process_the_good_map(buildings_layer, intersections_layer, cities_file, model):
   loaded_rf = joblib.load(model)
   cities = gpd.read_file(cities_file)
   # connect to the PostGIS database
   config = load_config()
   conn = connect(config)

   important_buildings = []
   for idx, row in cities.iterrows():
    print("id cities: {}".format(idx))
    # city with id #47 crashes so we do not process it
    if idx==47 or idx==54 or idx==64 or idx==86:
       continue
    
    geometry = row['geometry']
    geom_text = geometry.wkt
    query1 = "SELECT * FROM public.\"{}\" x WHERE ST_Within(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(buildings_layer,geom_text)
    query2 = "SELECT * FROM public.\"{}\" x WHERE ST_Within(x.geom, ST_SetSRID(ST_GeomFromText('{}'),2154))".format(intersections_layer,geom_text)
    df_buildings = gpd.GeoDataFrame.from_postgis(query1, conn)
    df_roads = gpd.GeoDataFrame.from_postgis(query2, conn)
    #cur.execute(query1)
    #rows_buildings = cur.fetchall()
    #print(len(rows_buildings))
    #cur.execute(query2)
    #rows_inter = cur.fetchall()
    prediction_dataset = gpd.GeoDataFrame.copy(df_buildings)
    dataset = prepare_dataset_prediction(df_buildings, df_roads, prediction_dataset)

    X = dataset.drop('important', axis=1)
    print(X)
    y = loaded_rf.predict(X)
    print(y)
    i = 0
    for important in y:
       if important == 1:
          building = df_buildings.iloc[i]
          important_buildings.append(building)
       i += 1
       
   # export the important buildings as a shapefile
   gdf = gpd.GeoDataFrame(important_buildings, geometry='geom', crs='2154').drop(['date_app','date_conf','date_maj','date_creat'], axis = 1)
   gdf.to_file("prediction.shp")


#train_model("zip://batiment.zip", "zip://road_intersections_train.zip")
process_the_good_map("batiment_urbain","road_intersections","zip://cities.zip","random_forest.joblib")

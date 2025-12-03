import geopandas as gpd
from cartagen4py.processes.agent.core import *
from cartagen4py.processes.agent.actions import *
from cartagen4py.processes.agent.constraints import *
from cartagen4py.processes.agent.agents import *
from shapely.geometry import LineString
import matplotlib as plt

def test_block_agents(final_scale):
    buildings = [loads('Polygon ((426178.6 6252642.8, 426182.8 6252643.4, 426183.1 6252641.3, 426186 6252641.5, 426186.7 6252636.4, 426189.3 6252636.7, 426189.8 6252632.7, 426195.9 6252631.4, 426202.5 6252632.2, 426201.6 6252639.9, 426199.1 6252639.6, 426198.3 6252646, 426189.3 6252645.3, 426189.1 6252648.8, 426178.1 6252647.7, 426178.6 6252642.8))'),
        loads('Polygon ((426177.6 6252652.2, 426189 6252653.3, 426188.4 6252659.3, 426194 6252659.8, 426193.4 6252664.1, 426176.2 6252661.9, 426177.6 6252652.2))'),
        loads('Polygon ((426172 6252668.9, 426182.8 6252670.2, 426181.9 6252675.1, 426184 6252675.3, 426183 6252681.7, 426179.4 6252681.2, 426179.6 6252678.7, 426170.7 6252677.7, 426172 6252668.9))'),
        loads('Polygon ((426167 6252690.3, 426179.3 6252691.8, 426178.1 6252700.4, 426166 6252698.8, 426167 6252690.3))'),
        loads('Polygon ((426163.6 6252681.3, 426169.2 6252682, 426168.8 6252685, 426163.2 6252684.4, 426163.6 6252681.3))'),
        loads('Polygon ((426164.9 6252665.1, 426165.5 6252660.2, 426171.7 6252661.1, 426171 6252665.8, 426164.9 6252665.1))'),
        loads('Polygon ((426162.3 6252647.3, 426160.7 6252659.7, 426149.6 6252658.3, 426150.6 6252647.5, 426150.8 6252645.9, 426154.5 6252646.3, 426162.3 6252647.3))'),
        loads('Polygon ((426143.6 6252672.5, 426143.2 6252674.6, 426138.9 6252674.1, 426139.6 6252669.8, 426129.7 6252668.8, 426130.9 6252658.7, 426135.8 6252659.1, 426135.6 6252661.2, 426144.7 6252662.4, 426143.6 6252672.5))'),
        loads('Polygon ((426147.2 6252684.6, 426146.8 6252689.1, 426154.4 6252690.5, 426153.4 6252699.7, 426145.7 6252698.9, 426146.1 6252696.1, 426142 6252695.6, 426141.8 6252697.6, 426141.6 6252698.9, 426137.7 6252698.5, 426137.7 6252698.1, 426126.8 6252696.9, 426127.7 6252687.4, 426139 6252688.7, 426138.8 6252689.8, 426142.6 6252690.1, 426143.2 6252684.2, 426147.2 6252684.6))'),
        loads('Polygon ((426120.2 6252676.9, 426121.2 6252670.9, 426124.5 6252671.4, 426124.3 6252673.2, 426123.8 6252677.3, 426120.2 6252676.9))'),
        loads('Polygon ((426117.5 6252691.9, 426105.1 6252690.5, 426105.3 6252689.2, 426106.3 6252680, 426118.8 6252681.5, 426117.6 6252690.6, 426117.5 6252691.9))'),
        loads('Polygon ((426108.5 6252657.9, 426121.9 6252659.5, 426120.7 6252667.4, 426108 6252665.9, 426108.5 6252657.9))'),
        loads('Polygon ((426102.7 6252669.1, 426106.1 6252669.3, 426105.2 6252675.2, 426102 6252674.9, 426102.7 6252669.1))'),
        loads('Polygon ((426093.6 6252687.2, 426090.9 6252686.8, 426084.5 6252686.1, 426086.2 6252674.7, 426094 6252675.7, 426094.5 6252673.6, 426098.5 6252674.1, 426097.1 6252685.5, 426093.9 6252685.3, 426093.6 6252687.2))'),
        loads('Polygon ((426077.1 6252691.1, 426066.1 6252689.8, 426067.4 6252679.3, 426067.5 6252678.3, 426078.3 6252679.8, 426078.2 6252680.8, 426077.1 6252691.1))'),
        loads('Polygon ((426054.2 6252688.5, 426032.5 6252686, 426033.9 6252680.3, 426063.3 6252671.3, 426061 6252689.4, 426054.2 6252688.5))')]
    
    roads = [loads('LineString (426217.6 6252616, 426093 6252652.2, 426000.8 6252678)'),
        loads('LineString (426004.7 6252691.6, 426001.8 6252686.9, 426000.9 6252682.5, 426000.8 6252678)'),
        loads('LineString (426167.5 6252709.8, 426166.1 6252709.8, 426125.7 6252705.1, 426018.7 6252693.3, 426004.7 6252691.6)'),
        loads('LineString (426183.5 6252710.1, 426167.5 6252709.8)'),
        loads('LineString (426217.6 6252616, 426214.8 6252624.7, 426205.3 6252655.9, 426193 6252693.8, 426190 6252701.6, 426186.7 6252706.4, 426183.5 6252710.1)')]
    
    p1 = gpd.GeoSeries(buildings)
    p3 = gpd.GeoSeries(roads)
    buildinggdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(p1))
    roadgdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(p3))
    # print(roadgdf)

    # Create micro building agents
    final_scale = final_scale / 1000.0
    agents = []
    building_agents = []
    for index, feature in buildinggdf.iterrows():
        agent = BuildingAgent(feature)
        agent.clean()
        # add constraints (the values correspond to 1:35k with classical IGN specs)
        squareness = BuildingSquarenessConstraint(1,agent)
        size = BuildingSizeConstraint(1, agent, 0.2 * final_scale * final_scale)
        granularity = BuildingGranularityConstraint(1, agent, 0.1 * final_scale)
        agent.constraints.append(size)
        agent.constraints.append(squareness)
        agent.constraints.append(granularity)
        agents.append(agent)
        building_agents.append(agent)

    # create the block from the roads
    blocks = polygonize(roads)
    blockgdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(blocks))

    road_sizes = []
    for road in roads:
        # 0.5 map mm symbol for all roads
        road_sizes.append(0.5 * final_scale)

    # create the block agent
    agents_to_activate = []
    for index, feature in blockgdf.iterrows():
        block_agent = BlockAgent(feature, building_agents, roadgdf)
        # add constraints
        activatemicros = ComponentsSatisfactionConstraint(1,block_agent)
        block_agent.constraints.append(activatemicros)
        proxi = BlockProximityConstraint(1,block_agent, 0.1 * final_scale, road_sizes)
        density = BlockDensityConstraint(1,block_agent, 0.25 * final_scale * final_scale, 0.75, road_sizes)
        block_agent.constraints.append(proxi)
        block_agent.constraints.append(density)
        agents.append(block_agent)
        agents_to_activate.append(block_agent)
    run_agents(agents_to_activate,verbose=1)

    geoms_gen = []
    for agent in agents:
        if agent.deleted:
            continue
        geoms_gen.append(agent.feature['geometry'])
    base = p1.plot()
    p2 = gpd.GeoSeries(geoms_gen)
    p2.plot(ax=base, facecolor='none', edgecolor='red')
    p3.plot(ax=base, facecolor='none', edgecolor='red', linewidth=4)
    plt.show()

# both layers should be shapefiles
def create_faces(road_layer, urban_area_layer):
    roads_df = gpd.read_file(road_layer)
    series = roads_df['geometry']
    # add the urban areas as lines in the series
    urban_area_df = gpd.read_file(urban_area_layer)
    for index, feature in urban_area_df.iterrows():
        geom = LineString(feature['geometry'].exterior.coords)
        series.add(geom)
    return series.polygonize()

def create_agents(faces_gdf, building_gdf, road_gdf, road_sizes, final_scale, building_min_size = 0.25, min_sep = 0.1, density_ratio = 0.75):
    agents_to_activate = []
    agents = []
    building_agents = []
    for index, feature in building_gdf.iterrows():
        agent = BuildingAgent(feature)
        agent.clean()
        # add constraints (the values correspond to 1:35k with classical IGN specs)
        squareness = BuildingSquarenessConstraint(1,agent)
        size = BuildingSizeConstraint(1, agent, 0.2 * final_scale * final_scale)
        granularity = BuildingGranularityConstraint(1, agent, 0.1 * final_scale)
        agent.constraints.append(size)
        agent.constraints.append(squareness)
        agent.constraints.append(granularity)
        agents.append(agent)
        building_agents.append(agent)

    for index, feature in faces_gdf.iterrows():
        block_agent = BlockAgent(feature, building_agents, road_gdf)
        # add constraints
        activatemicros = ComponentsSatisfactionConstraint(1,block_agent)
        block_agent.constraints.append(activatemicros)
        proxi = BlockProximityConstraint(1,block_agent, min_sep * final_scale, road_sizes)
        density = BlockDensityConstraint(1,block_agent, building_min_size * final_scale * final_scale, density_ratio, road_sizes)
        block_agent.constraints.append(proxi)
        block_agent.constraints.append(density)
        agents.append(block_agent)
        agents_to_activate.append(block_agent)

    return agents, agents_to_activate

def run_generalisation(agents, output_file):
    run_agents(agents,verbose=1)

    gen_buildings = []
    for agent in agents:
        if agent.deleted:
            continue
        gen_buildings.append([agent.feature['geometry'],agent.feature['nature']])
    
    new_df = gpd.GeoDataFrame(gen_buildings,geometry='geometry',columns=['geometry','nature'])
    new_df.to_file(output_file)
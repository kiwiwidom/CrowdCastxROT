import geopandas as gpd
import pandas as pd
import os
from shapely.geometry import Point
import warnings

warnings.filterwarnings('ignore')

stations_coords = {
    "Fernando Poe Jr.": (14.6575596, 121.0211401), "Balintawak": (14.6574221, 121.0038959),
    "Monumento": (14.6543138, 120.9838375), "5th Avenue": (14.6444204, 120.9835539),
    "R. Papa": (14.6360484, 120.9823434), "Abad Santos": (14.6305383, 120.9814967),
    "Blumentritt": (14.6226554, 120.9828902), "Tayuman": (14.6166782, 120.9827646),
    "Bambang": (14.6111375, 120.9824361), "Doroteo Jose": (14.605296, 120.9821343),
    "Carriedo": (14.5991725, 120.9813638), "Central Terminal": (14.5927991, 120.9816188),
    "United Nations": (14.5825457, 120.9846145), "Pedro Gil": (14.5765746, 120.988066),
    "Quirino": (14.570339, 120.9915173), "Vito Cruz": (14.5636587, 120.9946644),
    "Gil Puyat": (14.554059, 120.9971608), "Libertad": (14.5477375, 120.9986184),
    "EDSA": (14.5388064, 121.0006313), "Baclaran": (14.5344077, 120.9984558),
    "Redemptorist-Aseana": (14.5302727, 120.9929386), "MIA Road": (14.5185406, 120.993),
    "PITX": (14.5081487, 120.9912389), "Ninoy Aquino Avenue": (14.4989388, 120.9943729),
    "Dr. Santos": (14.4852658, 120.9896408), "Recto": (14.6034944, 120.9835891),
    "Legarda": (14.600877, 120.9925685), "Pureza": (14.6016716, 121.0050967),
    "V. Mapa": (14.6042216, 121.0172471), "J. Ruiz": (14.6105686, 121.0260986),
    "Gilmore": (14.6134607, 121.034016), "Betty Go-Belmonte": (14.6186484, 121.0427949),
    "Araneta Center-Cubao (LRT-2)": (14.6228569, 121.052964), "Anonas": (14.6279509, 121.064602),
    "Katipunan": (14.6310843, 121.0727829), "Santolan": (14.6221137, 121.0859809),
    "Marikina-Pasig": (14.6204035, 121.1005493), "Antipolo": (14.580278, 121.121111),
    "North Avenue": (14.6521641, 121.0322409), "Quezon Avenue": (14.6422956, 121.0387658),
    "GMA Kamuning": (14.6353731, 121.043265), "Araneta Center-Cubao (MRT-3)": (14.6228569, 121.052964),
    "Santolan-Annapolis": (14.6080352, 121.0563699), "Ortigas": (14.5878938, 121.0567297),
    "Shaw Boulevard": (14.5810649, 121.0534794), "Boni": (14.5738302, 121.0482154),
    "Guadalupe": (14.5672248, 121.0456233), "Buendia": (14.5542118, 121.0340531),
    "Ayala": (14.5491978, 121.027902), "Magallanes": (14.5419456, 121.0193504),
    "Taft Avenue": (14.5375565, 121.0013065)
}

shp_path = './data/manila/hotosm_phl_points_of_interest_points_shp.shp'
poi_gdf = gpd.read_file(shp_path).to_crs(epsg=3123)

l1_keys = ['supermarket', 'department_store', 'bus_station', 'ferry_terminal', 'hospital', 'university', 'college', 'mall']
l2_keys = ['restaurant', 'fast_food', 'bank', 'school', 'cafe', 'atm', 'clinic', 'dentist', 'police', 'electronics', 'computer', 'mobile_phone']
l3_keys = ['convenience', 'bakery', 'pawnbroker', 'laundry', 'place_of_worship', 'fuel', 'hairdresser', 'beauty']

W1, W2, W3 = 100, 10, 1

results = []

for name, (lat, lon) in stations_coords.items():
    station_gdf = gpd.GeoDataFrame([{'name': name}], geometry=[Point(lon, lat)], crs="EPSG:4326").to_crs(epsg=3123)
    station_point = station_gdf.geometry.iloc[0]
    nearby = poi_gdf[poi_gdf.distance(station_point) <= 500]
    
    if not nearby.empty:
        text = nearby[['amenity', 'shop']].astype(str).apply(lambda x: ' '.join(x).lower(), axis=1)
        l1 = sum(text.str.contains('|'.join(l1_keys)))
        l2 = sum(text.str.contains('|'.join(l2_keys)))
        l3 = sum(text.str.contains('|'.join(l3_keys)))
    else:
        l1 = l2 = l3 = 0

    s1, s2, s3 = l1*W1, l2*W2, l3*W3
    max_score = max(s1, s2, s3)
    

    if l1 >= 3:
        label = "Level 1"
    elif l1 > 0 or l2 >= 40:
        label = "Level 2"
    else:
        label = "Level 3"
    
    results.append({'station': name, 'Level 1': l1, 'Level 2': l2, 'Level 3': l3, 'soc_func': label})
    print(f" {name:<30} | L1:{l1:>3}, L2:{l2:>3}, L3:{l3:>3} -> {label}")

pd.DataFrame(results).to_csv('./data/manila/social_function.csv', index=False)

import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

stations = {
    "LRT1": ["Fernando Poe Jr.", "Balintawak", "Monumento", "5th Avenue", "R. Papa", "Abad Santos", "Blumentritt", "Tayuman", "Bambang", "Doroteo Jose", "Carriedo", "Central Terminal", "United Nations", "Pedro Gil", "Quirino", "Vito Cruz", "Gil Puyat", "Libertad", "EDSA", "Baclaran", "Redemptorist-Aseana", "MIA Road", "PITX", "Ninoy Aquino Avenue", "Dr. Santos"],
    "LRT2": ["Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz", "Gilmore", "Betty Go-Belmonte", "Araneta Center-Cubao (LRT-2)", "Anonas", "Katipunan", "Santolan", "Marikina-Pasig", "Antipolo"],
    "MRT3": ["North Avenue", "Quezon Avenue", "GMA Kamuning", "Araneta Center-Cubao (MRT-3)", "Santolan-Annapolis", "Ortigas", "Shaw Boulevard", "Boni", "Guadalupe", "Buendia", "Ayala", "Magallanes", "Taft Avenue"]
}

coords = {
    "Fernando Poe Jr.": (14.6575596, 121.0211401), "Balintawak": (14.6574221, 121.0038959), "Monumento": (14.6543138, 120.9838375), "5th Avenue": (14.6444204, 120.9835539), "R. Papa": (14.6360484, 120.9823434), "Abad Santos": (14.6305383, 120.9814967), "Blumentritt": (14.6226554, 120.9828902), "Tayuman": (14.6166782, 120.9827646), "Bambang": (14.6111375, 120.9824361), "Doroteo Jose": (14.605296, 120.9821343), "Carriedo": (14.5991725, 120.9813638), "Central Terminal": (14.5927991, 120.9816188), "United Nations": (14.5825457, 120.9846145), "Pedro Gil": (14.5765746, 120.988066), "Quirino": (14.570339, 120.9915173), "Vito Cruz": (14.5636587, 120.9946644), "Gil Puyat": (14.554059, 120.9971608), "Libertad": (14.5477375, 120.9986184), "EDSA": (14.5388064, 121.0006313), "Baclaran": (14.5344077, 120.9984558), "Redemptorist-Aseana": (14.5302727, 120.9929386), "MIA Road": (14.5185406, 120.993), "PITX": (14.5081487, 120.9912389), "Ninoy Aquino Avenue": (14.4989388, 120.9943729), "Dr. Santos": (14.4852658, 120.9896408),
    "Recto": (14.6034944, 120.9835891), "Legarda": (14.600877, 120.9925685), "Pureza": (14.6016716, 121.0050967), "V. Mapa": (14.6042216, 121.0172471), "J. Ruiz": (14.6105686, 121.0260986), "Gilmore": (14.6134607, 121.034016), "Betty Go-Belmonte": (14.6186484, 121.0427949), "Araneta Center-Cubao (LRT-2)": (14.6228569, 121.052964), "Anonas": (14.6279509, 121.064602), "Katipunan": (14.6310843, 121.0727829), "Santolan": (14.6221137, 121.0859809), "Marikina-Pasig": (14.6204035, 121.1005493), "Antipolo": (14.580278, 121.121111),
    "North Avenue": (14.6521641, 121.0322409), "Quezon Avenue": (14.6422956, 121.0387658), "GMA Kamuning": (14.6353731, 121.043265), "Araneta Center-Cubao (MRT-3)": (14.6228569, 121.052964), "Santolan-Annapolis": (14.6080352, 121.0563699), "Ortigas": (14.5878938, 121.0567297), "Shaw Boulevard": (14.5810649, 121.0534794), "Boni": (14.5738302, 121.0482154), "Guadalupe": (14.5672248, 121.0456233), "Buendia": (14.5542118, 121.0340531), "Ayala": (14.5491978, 121.027902), "Magallanes": (14.5419456, 121.0193504), "Taft Avenue": (14.5375565, 121.0013065)
}

def haversine(p1, p2):
    lat1, lon1 = map(radians, p1); lat2, lon2 = map(radians, p2)
    dlat = lat2 - lat1; dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 6371000

speeds = {"LRT1": 16.67, "LRT2": 16.67, "MRT3": 16.67}
DWELL_TIME = 30 # seconds

results = []

for line, station_list in stations.items():
    v = speeds[line]
    for i in range(len(station_list) - 1):
        s1, s2 = station_list[i], station_list[i+1]
        dist = haversine(coords[s1], coords[s2])
        
        # Time = (Distance / Speed) + Dwell
        travel_time = (dist / v) + DWELL_TIME
        
        results.append({
            'line': line,
            'origin': s1,
            'destination': s2,
            'distance_m': round(dist, 2),
            'ideal_duration_sec': round(travel_time, 0)
        })

df = pd.DataFrame(results)
df.to_csv('./data/manila/manila_segment_baselines.csv', index=False)

mrt3_total = df[df['line'] == 'MRT3']['ideal_duration_sec'].sum() / 60
print(f"Total calculated journey: {mrt3_total:.1f} minutes (Target was 50m)")
print(f"Created ./data/manila/manila_segment_baselines.csv")
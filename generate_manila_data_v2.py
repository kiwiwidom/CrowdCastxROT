import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

lines = {
    "LRT1": [
        ("Fernando Poe Jr.", 14.6575596, 121.0211401), ("Balintawak", 14.6574221, 121.0038959),
        ("Monumento", 14.6543138, 120.9838375), ("5th Avenue", 14.6444204, 120.9835539),
        ("R. Papa", 14.6360484, 120.9823434), ("Abad Santos", 14.6305383, 120.9814967),
        ("Blumentritt", 14.6226554, 120.9828902), ("Tayuman", 14.6166782, 120.9827646),
        ("Bambang", 14.6111375, 120.9824361), ("Doroteo Jose", 14.605296, 120.9821343),
        ("Carriedo", 14.5991725, 120.9813638), ("Central Terminal", 14.5927991, 120.9816188),
        ("United Nations", 14.5825457, 120.9846145), ("Pedro Gil", 14.5765746, 120.988066),
        ("Quirino", 14.570339, 120.9915173), ("Vito Cruz", 14.5636587, 120.9946644),
        ("Gil Puyat", 14.554059, 120.9971608), ("Libertad", 14.5477375, 120.9986184),
        ("EDSA", 14.5388064, 121.0006313), ("Baclaran", 14.5344077, 120.9984558),
        ("Redemptorist-Aseana", 14.5302727, 120.9929386), ("MIA Road", 14.5185406, 120.993),
        ("PITX", 14.5081487, 120.9912389), ("Ninoy Aquino Avenue", 14.4989388, 120.9943729),
        ("Dr. Santos", 14.4852658, 120.9896408)
    ],
    "LRT2": [
        ("Recto", 14.6034944, 120.9835891), ("Legarda", 14.600877, 120.9925685),
        ("Pureza", 14.6016716, 121.0050967), ("V. Mapa", 14.6042216, 121.0172471),
        ("J. Ruiz", 14.6105686, 121.0260986), ("Gilmore", 14.6134607, 121.034016),
        ("Betty Go-Belmonte", 14.6186484, 121.0427949), ("Araneta Center-Cubao (LRT-2)", 14.6228569, 121.052964),
        ("Anonas", 14.6279509, 121.064602), ("Katipunan", 14.6310843, 121.0727829),
        ("Santolan", 14.6221137, 121.0859809), ("Marikina-Pasig", 14.6204035, 121.1005493),
        ("Antipolo", 14.580278, 121.121111)
    ],
    "MRT3": [
        ("North Avenue", 14.6521641, 121.0322409), ("Quezon Avenue", 14.6422956, 121.0387658),
        ("GMA Kamuning", 14.6353731, 121.043265), ("Araneta Center-Cubao (MRT-3)", 14.6228569, 121.052964),
        ("Santolan-Annapolis", 14.6080352, 121.0563699), ("Ortigas", 14.5878938, 121.0567297),
        ("Shaw Boulevard", 14.5810649, 121.0534794), ("Boni", 14.5738302, 121.0482154),
        ("Guadalupe", 14.5672248, 121.0456233), ("Buendia", 14.5542118, 121.0340531),
        ("Ayala", 14.5491978, 121.027902), ("Magallanes", 14.5419456, 121.0193504),
        ("Taft Avenue", 14.5375565, 121.0013065)
    ]
}

def generate_full_system_telemetry(filename, num_trips=800):
    all_pings = []
    base_date = datetime(2026, 6, 1, 5, 0, 0)
    print(f"Simulating {num_trips} trips across LRT-1, LRT-2, and MRT-3...")

    for t_id in range(num_trips):
        line_name = np.random.choice(list(lines.keys()))
        station_list = lines[line_name]
        
        trip_start = base_date + timedelta(minutes=15 * t_id)
        is_raining = 1 if np.random.random() < 0.3 else 0
        
        for i in range(len(station_list)-1):
            s1_name, s1_lat, s1_lon = station_list[i]
            s2_name, s2_lat, s2_lon = station_list[i+1]
            
            for _ in range(3):
                all_pings.append({
                    'trip_id': f"{line_name}_{t_id}", 'timestamp': trip_start,
                    'latitude': s1_lat, 'longitude': s1_lon, 'is_gps_valid': 1,
                    'rain': is_raining, 'arrivalDelay': 0, 'congestionLevel': 2
                })
                trip_start += timedelta(seconds=20)

            steps = 5
            for step in range(1, steps):
                inter_lat = s1_lat + (s2_lat - s1_lat) * (step/steps)
                inter_lon = s1_lon + (s2_lon - s1_lon) * (step/steps)
                all_pings.append({
                    'trip_id': f"{line_name}_{t_id}", 'timestamp': trip_start,
                    'latitude': inter_lat, 'longitude': inter_lon, 'is_gps_valid': 1,
                    'rain': is_raining, 'arrivalDelay': 0, 'congestionLevel': 1
                })
                trip_start += timedelta(seconds=40)

        all_pings.append({
            'trip_id': f"{line_name}_{t_id}", 'timestamp': trip_start,
            'latitude': station_list[-1][1], 'longitude': station_list[-1][2],
            'is_gps_valid': 1, 'rain': is_raining, 'arrivalDelay': 0, 'congestionLevel': 1
        })

    df = pd.DataFrame(all_pings)
    
    cols_to_fix = ['arrivalDelay', 'departureDelay', 'dwellTime_sec', 'temperature_2m', 
                   'is_slowdown', 'is_congested', 'is_slow_speed', 'travel_time_sec']
    for c in cols_to_fix:
        if c not in df.columns: df[c] = 0
            
    df.to_csv(filename, index=False)

os.makedirs('./data/manila', exist_ok=True)
generate_full_system_telemetry('./data/manila/train_data.csv', num_trips=1200)
generate_full_system_telemetry('./data/manila/test_data.csv', num_trips=200)
generate_full_system_telemetry('./data/manila/validation_data.csv', num_trips=100)
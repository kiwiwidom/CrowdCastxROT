import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from math import radians, cos, sin, asin, sqrt

stations_data = {
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

speeds = {"LRT1": 16.67, "LRT2": 16.67, "MRT3": 16.67}

def haversine_dist(p1, p2):
    lat1, lon1 = map(radians, p1); lat2, lon2 = map(radians, p2)
    a = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
    return 2 * asin(sqrt(a)) * 6371000

def get_headway(current_time):
    time_val = current_time.hour + (current_time.minute / 60)
    if 4.5 <= time_val <= 7.0: return 5.5 # Morning
    if 7.0 < time_val <= 9.0: return 3.5 # AM Peak
    if 9.0 < time_val <= 17.0: return 5.2 # Off Peak
    if 17.0 < time_val <= 19.0: return 3.5 # PM Peak
    return 10.0 # Extended/Night

def generate_dataset(filename, num_trips=1000):
    data = []
    base_date = datetime(2026, 6, 1, 4, 30, 0)

    for t_id in range(num_trips):
        line = np.random.choice(["LRT1", "LRT2", "MRT3"])
        station_list = stations_data[line]
        v_limit = speeds[line]
        
        start_node = np.random.randint(0, len(station_list)-5)
        trip_path = station_list[start_node : start_node + np.random.randint(5, 12)]
        
        start_time = base_date + timedelta(minutes=10 * t_id)
        is_raining = 1 if np.random.random() < 0.25 else 0
        
        for i in range(len(trip_path)-1):
            s1_name, s1_lat, s1_lon = trip_path[i]
            s2_name, s2_lat, s2_lon = trip_path[i+1]
            dist = haversine_dist((s1_lat, s1_lon), (s2_lat, s2_lon))
            
            base_time = dist / v_limit
            headway = get_headway(start_time)
            
            hour = start_time.hour
            is_peak = 1 if (7 <= hour <= 9 or 17 <= hour <= 20) else 0
            
            delay = 0
            if is_peak: delay += np.random.randint(60, 300) # +1-5 min rush
            if is_raining: delay += np.random.randint(30, 120) # +0.5-2 min rain
            
            actual_duration = base_time + delay + 30 # +30s Dwell
            
            data.append({
                'trip_id': f"MNL_{line}_{t_id}",
                'timestamp': start_time,
                'originStopName': s1_name, 'originLat': s1_lat, 'originLon': s1_lon,
                'destinationStopName': s2_name, 'destinationLat': s2_lat, 'destinationLon': s2_lon,
                'duration_sec': actual_duration,
                'arrivalDelay': delay,
                'departureDelay': delay + 5,
                'dwellTime_sec': 30 + (20 if is_peak else 0),
                'distance_m': dist,
                'speed_mps': dist / actual_duration,
                'rain': is_raining,
                'congestionLevel': 4 if (is_peak and is_raining) else (3 if is_peak else 1),
                'is_peak_hour': is_peak,
                'is_weekend': 1 if start_time.weekday() >= 5 else 0,
                'latitude': s1_lat, 'longitude': s1_lon
            })
            start_time += timedelta(seconds=actual_duration + 30)

    df = pd.DataFrame(data)
    all_cols = ['trip_id', 'vehicle_id', 'vehicleLabel', 'vehicleLicencePlate', 'trip_stop_sequence', 
                'vehicle_stop_sequence', 'originStopID', 'originStopName', 'originLat', 'originLon', 
                'destinationStopID', 'destinationStopName', 'destinationLat', 'destinationLon', 
                'speed_kph', 'speed_mps', 'distance_m', 'delta_t_sec', 'travel_time_sec', 'dwellTime_sec', 
                'total_travel_time_sec', 'total_distance_m', 'congestionLevel', 'odometer', 'bearing', 
                'temperature_2m', 'apparent_temperature', 'precipitation', 'rain', 'snowfall', 
                'windspeed_10m', 'windgusts_10m', 'winddirection_10m', 'is_slow_speed', 'is_long_dwell', 
                'is_delayed', 'is_congested', 'is_slowdown', 'slowdown_lat', 'slowdown_lon', 'segment', 
                'currentLoc', 'timestamp', 'latitude', 'longitude', 'currentStatus', 'is_weekend', 
                'arrivalDelay', 'arrivalTime', 'departureDelay', 'departureTime', 'tripScheduleRelationship', 
                'is_peak_hour', 'has_prev_stop', 'service_date']
    
    for c in all_cols:
        if c not in df.columns: df[c] = 0
            
    df.to_csv(filename, index=False)
    print(f"✅ Saved {filename} with {len(df):,} rows.")

os.makedirs('./data/manila', exist_ok=True)
generate_dataset('./data/manila/train_data.csv', num_trips=2000)
generate_dataset('./data/manila/test_data.csv', num_trips=400)
generate_dataset('./data/manila/validation_data.csv', num_trips=200)
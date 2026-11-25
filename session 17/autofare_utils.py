import math

def calculate_fare(distance_km, waiting_minutes=0):
    if distance_km <= 1.5:
        base_and_dist = 25.0
    else:
        base_and_dist = 25.0 + (distance_km - 1.5) * 13.0
    total = base_and_dist + waiting_minutes * 1.0
    return math.ceil(total)

def night_fare(distance_km, start_hour, waiting_minutes=0):
    fare = calculate_fare(distance_km, waiting_minutes=waiting_minutes)
    if start_hour < 5 or start_hour >= 22:
        return math.ceil(fare * 1.25)
    return fare

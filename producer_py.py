# -*- coding: utf-8 -*-
"""producer.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xEbmi6LGeyuL677GoeTis3snfYdv2N8A
"""

import json
import requests
from kafka import KafkaProducer
import time
# OpenWeatherMap API details
API_KEY = 'b76302824cad264286cb504f7ff4e9d8'
CITY = 'Chennai'  # City name
LAT, LON = 13.0827, 80.2707  # Latitude and Longitude of Chennai

# API URL to fetch air quality data
URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat=12.9716&lon=77.5946&appid={API_KEY}"

# Kafka Producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka server
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Convert data to JSON
)

def fetch_air_quality_data():
    """Fetch real-time air quality data from OpenWeatherMap API"""
    try:
        response = requests.get(URL)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Send data to Kafka at regular intervals
while True:
    air_data = fetch_air_quality_data()
    if air_data:
        producer.send('air-quality-data', value=air_data)
        print("✅ Data sent to Kafka:", air_data)
        time.sleep(10)  # Fetch data every 10 second
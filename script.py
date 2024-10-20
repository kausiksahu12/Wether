import random
import datetime
from pymongo import MongoClient
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client.weather_db

# Cities for which you want to generate data
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Hyderabad']

# Weather conditions to choose from
WEATHER_CONDITIONS = ['Clear', 'Clouds', 'Rain', 'Thunderstorm', 'Mist', 'Haze']

# Function to generate realistic weather data for a city
def generate_weather_data(city, date):
    # Generate realistic temperatures
    min_temp = round(random.uniform(20.0, 28.0), 2)
    max_temp = round(random.uniform(min_temp + 2.0, min_temp + 10.0), 2)
    avg_temp = round((min_temp + max_temp) / 2, 2)
    
    # Select a dominant weather condition
    dominant_condition = random.choice(WEATHER_CONDITIONS)
    
    # Create the data structure
    weather_data = {
        "city": city,
        "date": date,
        "avg_temp": avg_temp,
        "dominant_condition": dominant_condition,
        "max_temp": max_temp,
        "min_temp": min_temp
    }
    
    return weather_data

# Function to insert data into MongoDB
def insert_data_into_db(weather_data):
    db.daily_summaries.insert_one(weather_data)
    print(f"Inserted weather data for {weather_data['city']} on {weather_data['date']} into MongoDB.")

# Main function to generate and insert fake weather data for the past 30 days
def generate_and_store_fake_weather_data():
    start_date = datetime.datetime(2024, 8, 15)
    
    for city in CITIES:
        for day in range(30):
            date = start_date - datetime.timedelta(days=day)
            weather_data = generate_weather_data(city, date)
            insert_data_into_db(weather_data)

if __name__ == "__main__":
    generate_and_store_fake_weather_data()
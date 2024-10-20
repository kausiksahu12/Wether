import requests
import datetime
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from config import OPENWEATHER_API_KEY, MONGO_URI


client = MongoClient(MONGO_URI)
db = client.weather_db

CITIES = ["Delhi", "Mumbai", "Chennai", "Bengaluru", "Kolkata", "Hyderabad"]

#************************************************************************************************
consecutiveCount = {
    city: {
        'count' : 0
    }
    for city in CITIES
}

threshold = 20

running_totals = {
    city: {
        'count': 0,
        'total_temp': 0,
        'max_temp': float('-inf'),
        'min_temp': float('inf'),
        'condition_counts': {}  
    }
    for city in CITIES
}

#~?functions --------------------------------
def update_threshold(new_threshold):
    global threshold, consecutiveCount
    threshold = new_threshold
    for city in CITIES:
        consecutiveCount[city]['count'] = 0

def get_count(city):
    return consecutiveCount[city]['count']

def get_threshold():
    return threshold


def fetch_current_data(city):
    now = datetime.datetime.utcnow()
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    return response

def fetch_and_store_weather_data():
    global consecutiveCount

    now = datetime.datetime.utcnow()
    for city in CITIES:
        response = fetch_current_data(city)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            max_temp = weather_data['main']['temp_max']
            min_temp = weather_data['main']['temp_min']
            condition = weather_data['weather'][0]['main']
            timestamp = datetime.datetime.utcnow()

            if(temperature > threshold):
                consecutiveCount[city]['count'] +=1
            else:
                consecutiveCount[city]['count'] = 0

            city_metrics = running_totals[city]
            city_metrics['count'] += 1
            city_metrics['total_temp'] += temperature
            city_metrics['max_temp'] = max(city_metrics['max_temp'], max_temp)
            city_metrics['min_temp'] = min(city_metrics['min_temp'], min_temp)

            if condition in city_metrics['condition_counts']:
                city_metrics['condition_counts'][condition] += 1
            else:
                city_metrics['condition_counts'][condition] = 1

            print(running_totals)
        else:
            print(f"Failed to fetch data for {city}: {response.status_code}")

def calculate_daily_summary():
    global running_totals
    print("Calculating daily summaries...")
    now = datetime.datetime.utcnow()
    start_of_day = datetime.datetime(now.year, now.month, now.day)

    for city in CITIES:
        city_metrics = running_totals.get(city, {})
        count = city_metrics.get('count', 0)
        total_temp = city_metrics.get('total_temp', 0)
        max_temp = city_metrics.get('max_temp', float('-inf'))
        min_temp = city_metrics.get('min_temp', float('inf'))

        if count > 0:
            avg_temp = total_temp / count

            dominant_condition = max(city_metrics['condition_counts'], key=city_metrics['condition_counts'].get)

            daily_summary = {
                "city": city,
                "date": now,  # Use datetime.datetime for MongoDB
                "avg_temp": avg_temp,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "dominant_condition": dominant_condition
            }
            db.daily_summaries.update_one(
                {"city": city, "date": now},
                {"$set": daily_summary},
                upsert=True
            )
            print(f"Daily summary for {city} calculated and stored.")
        else:
            print(f"No data found for {city} on {start_of_day.isoformat()}.")

    running_totals = {
        city: {
            'count': 0,
            'total_temp': 0,
            'max_temp': float('-inf'),
            'min_temp': float('inf'),
            'condition_counts': {}  
        }
        for city in CITIES
    }

def start_scheduler():
    print("Starting scheduler...")
    scheduler = BackgroundScheduler()

    def job_listener(event):
        if event.exception:
            print(f"Job {event.job_id} failed.")
        else:
            print(f"Job {event.job_id} completed successfully.")
    
    scheduler.add_job(fetch_and_store_weather_data, 'interval', seconds=10, id='fetch_weather_data')
    scheduler.add_job(calculate_daily_summary, 'cron', hour=22, minute=38, id='calculate_daily_summary')

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()
    print("Scheduler started. Jobs:")
    for job in scheduler.get_jobs():
        print(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}")


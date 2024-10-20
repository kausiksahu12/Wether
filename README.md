# Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates

![Screenshot 2024-08-16 005934](https://github.com/user-attachments/assets/eaa1f5bf-1293-4351-b541-14f6df41e8b9)

## NOTE:

1. I have inserted dummy data for the past 30 days because for past dates, data requires a premium version of the OpenWeather API.

- To insert the dummy data into your MongoDB database, run the script.py file:

```python
python script.py
```

2. The fetch timer is set to 10 seconds instead of 5 minutes for testing purposes. We can increase the fetch time in the code.
3. To check whether the summary of the day is inserted into the database, we can set the time just a minute ahead of the current time so that you don't have to wait for the entire day. This way, you will see at least one entry in the database, which will be shown in the graph.
   Change the time at which data rolled up data will be aggregated In /weather_scheduler.py:
   ```py
   scheduler.add_job(calculate_daily_summary, 'cron', hour=22, minute=38, id='calculate_daily_summary')
   ```

## Video Explanation

https://drive.google.com/file/d/1JB9QS93gOlv38UFhkLZfPIS2kVYXtNNH/view?usp=sharing

## Objective

Develop a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system will utilize data from the OpenWeatherMap API.

## Prerequisites

### Frontend

- Node.js (v20+)

### Backend

- Python 3.10.12

## Setup Instructions

### Clone the Repository

````sh
git clone https://github.com/Harshit-65/Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates.git

cd Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates


## Frontend Setup
1. Navigate to the frontend directory:
    ```sh
    cd frontend/myapp
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

3. Start the frontend application:
    ```sh
    npm start
    ```

4. Alternatively, you can use the build folder:
    ```sh
    npm run build
    npm install -g serve
    serve -s build
    ```

## Backend Setup
1. Install Python 3.10.12 and pip.

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the backend application:
    ```sh
    python3 app.py
    ```

4. Alternatively, set up a virtual environment to avoid version conflicts:
    ```bash
    https://www.hostinger.in/tutorials/how-to-create-a-python-virtual-environment?utm_campaign=Generic-Tutorials-DSA|NT:Se|LO:IN-t5&utm_medium=ppc&gad_source=1&gclid=Cj0KCQjwzva1BhD3ARIsADQuPnWREvbLPCI0vnp8tRtz6xTvHUNxhvP_jq42g9mHMo0nCX2Xk_faXLMaAtB0EALw_wcB
    ```

5. Set up MongoDB Atlas:
    - Sign up for a free MongoDB Atlas account.
    - Create a new cluster.
    - Get the connection string for your cluster.
    - Replace the `MONGO_URI` in the `config.py` file with your actual MongoDB Atlas connection string.

## Configuration
Update the `config.py` file with your actual API keys and MongoDB URI:
```python
# Replace with your actual OpenWeatherMap API key
OPENWEATHER_API_KEY = 'your_actual_openweather_api_key'
MONGO_URI = 'your_actual_mongodb_atlas_connection_string'
````

        ```

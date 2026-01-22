import boto3
import json
import requests
import psycopg2
import time
import os


print("1. Fetching 24-hour data from API...")
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&past_days=1&forecast_days=1"
response = requests.get(url)
data = response.json()

times = data['hourly']['time']
temps = data['hourly']['temperature_2m']
rows_to_insert = list(zip(times, temps))
print(f"   -> Found {len(rows_to_insert)} data points to insert.")

print("2. Connecting to Postgres...")
conn = None
for i in range(5):
    try:
        conn = psycopg2.connect(
            host="postgres-db",
            database="warehouse",
            user="admin",
            password="password"
        )
        print("   -> Connection successful!")
        break
    except psycopg2.OperationalError:
        print(f"   -> Database not ready yet... waiting 2 seconds (Attempt {i+1}/5)")
        time.sleep(2)

if not conn:
    print("ERROR: Could not connect to Postgres.")
    exit(1)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS weather_log (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    log_time TIMESTAMP,
    CONSTRAINT unique_weather UNIQUE (city, log_time)
);
""")

print("3. Inserting Batch Data...")

insert_query = """
INSERT INTO weather_log (city, temperature, log_time) 
VALUES (%s, %s, %s)
ON CONFLICT (city, log_time) DO NOTHING;
"""

for time_entry, temp_entry in rows_to_insert:
    cur.execute(insert_query, ('Berlin', temp_entry, time_entry))

conn.commit()
cur.close()
conn.close()

print("SUCCESS: Data loaded (Duplicates ignored)!")
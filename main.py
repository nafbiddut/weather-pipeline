import boto3
import requests
import json
import os

# 1. Connect to MinIO
s3 = boto3.client('s3',
    endpoint_url='http://minio-server:9000',
    aws_access_key_id='admin',
    aws_secret_access_key='password'
)

# 2. GET Real Data (Open-Meteo API - Berlin Weather)
print("Fetching Real-Time Weather Data for Berlin...")
# This API is stable, free, and does not require keys or headers
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"

try:
    response = requests.get(url)
    
    # Check status
    if response.status_code == 200:
        data = response.json()
        
        # 3. Save locally as JSON
        file_name = "berlin_weather.json"
        with open(file_name, "w") as f:
            json.dump(data, f)
        
        # 4. Upload to MinIO
        bucket_name = "datalake"
        s3.upload_file(file_name, bucket_name, file_name)
        
        print("------------------------------------------------")
        print(f"SUCCESS: Weather data uploaded to {bucket_name}!")
        print(f"Temperature in Berlin: {data['current_weather']['temperature']} C")
        print("------------------------------------------------")
        
    else:
        print(f"FAILURE: Status Code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"CRASH: {e}")
import time
import random
import requests
import sys

URL = "http://127.0.0.1:5000/sensor"

DEVICE_ID = "ESP32_SIM_001"
WIFI_SSID = "IoT_Network"

def generate_fake_data():
    temperature = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(40.0, 60.0), 2)
    wifi_rssi = random.randint(-80, -50)
    
    return {
        "temperature": temperature,
        "humidity": humidity,
        "device_id": DEVICE_ID,
        "wifi_ssid": WIFI_SSID,
        "wifi_rssi": wifi_rssi
    }

def main():
    print("Starting ESP32 simulation. Press Ctrl+C to stop.", flush=True)
    count = 0
    while True:
        data = generate_fake_data()
        try:
            response = requests.post(URL, json=data, timeout=5)
            print(f"Sent data: {data} | Status: {response.status_code}", flush=True)
            count += 1
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}", flush=True)
        
        # In a real scenario we'd use time.sleep(5)
        # We will loop exactly as asked. 
        time.sleep(5)

if __name__ == "__main__":
    main()

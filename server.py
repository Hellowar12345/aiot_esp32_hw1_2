import sqlite3
import datetime
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "aiotdb.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            device_id TEXT,
            wifi_ssid TEXT,
            wifi_rssi INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/sensor', methods=['POST'])
def sensor_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    timestamp = datetime.datetime.now().isoformat()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    device_id = data.get("device_id", "Unknown")
    wifi_ssid = data.get("wifi_ssid", "Unknown")
    wifi_rssi = data.get("wifi_rssi", 0)

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensors (timestamp, temperature, humidity, device_id, wifi_ssid, wifi_rssi)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, temperature, humidity, device_id, wifi_ssid, wifi_rssi))
        conn.commit()
        conn.close()
        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000)

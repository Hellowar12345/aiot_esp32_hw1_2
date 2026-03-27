import streamlit as st
import sqlite3
import pandas as pd
import time
import os

DB_NAME = "aiotdb.db"

def load_data():
    if not os.path.exists(DB_NAME):
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(DB_NAME)
        # Use a timeout to avoid locking issues
        conn.execute("PRAGMA journal_mode=WAL;") 
        df = pd.read_sql_query("SELECT * FROM sensors ORDER BY id DESC LIMIT 100", conn)
        conn.close()
        return df
    except Exception as e:
        # In case DB is locked or other errors
        return pd.DataFrame()

st.set_page_config(page_title="AIoT Dashboard", layout="wide")
st.title("ESP32 Sensor AIoT Dashboard")

placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        if not df.empty:
            latest = df.iloc[0]
            
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="Latest Temperature (°C)", value=f"{latest['temperature']:.2f}")
            with col2:
                st.metric(label="Latest Humidity (%)", value=f"{latest['humidity']:.2f}")
            with col3:
                st.metric(label="Device ID", value=latest['device_id'])
            with col4:
                st.metric(label="WiFi RSSI (dBm)", value=latest['wifi_rssi'])
                
            st.divider()
            
            # Charts
            df_plot = df.copy()
            df_plot['timestamp'] = pd.to_datetime(df_plot['timestamp'])
            df_plot = df_plot.sort_values(by='timestamp')
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("Temperature Trend")
                st.line_chart(data=df_plot, x='timestamp', y='temperature', use_container_width=True)
                
            with col_chart2:
                st.subheader("Humidity Trend")
                st.line_chart(data=df_plot, x='timestamp', y='humidity', use_container_width=True)
                
            st.divider()
            
            # Table
            st.subheader("Raw Data Table")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No data available yet. Waiting for ESP32 simulator to send data...")
            
    time.sleep(2)

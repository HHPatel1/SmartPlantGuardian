
# 🌱 Smart Plant Guardian — Project Overview

## 1. Introduction
Smart Plant Guardian is an IoT-based environmental monitoring system built to track the health and growing conditions of a Peace Lily plant. Using a Nicla Sense ME environmental sensor paired with an MKR WiFi 1010 microcontroller, the system performs real-time measurements of:

- Temperature  
- Relative Humidity  
- Barometric Pressure  
- VOCs (Volatile Organic Compounds)

Data is transmitted via MQTT, logged into an SQLite database, and displayed on a live dashboard.

---

## 2. Project Motivation
Many indoor plants suffer not from neglect, but from invisible environmental stress (humidity changes, poor air quality, overheating, under-ventilation). This project aims to:

- Make plant health **quantifiable**  
- Allow continuous **24-hour data acquisition**  
- Provide actionable insights for improving the indoor environment  

---

## 3. System Architecture
The full pipeline is:

1. **Nicla Sense ME** measures raw environmental data  
2. Environmental data sent to **MKR WiFi 1010** via Serial1  
3. MKR pushes the readings to an **MQTT broker (Cedalo Cloud)**  
4. A Python MQTT subscriber stores messages into **SQLite**  
5. The dashboard (Plotly Dash) reads from SQLite and displays:
   - Live graphs  
   - Health score  
   - Email alert preferences  
   - Plant profile  

---

## 4. Key Technical Features
- Full 24-hour real-time acquisition  

- FAIR-compliant data storage  
- Identified metadata schema  
- Portable dashboard with automatic refreshing  
- SQLite + CSV hybrid data storage  
- Email alert module  
- Health score model using weighted environmental factors  

---

## 5. Deliverables
- Full GitHub repository  
- SQLite database containing real collected data  
- 24-hour continuous dataset  
- Accompanying documentation and risk assessment  
- Live dashboard code

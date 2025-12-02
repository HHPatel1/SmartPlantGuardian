🌿 Smart Plant Guardian 🌿 - OVERVIEW 
A fully automated, data-driven environmental monitoring system for Peace Lily health assessment.

Smart Plant Guardian is an end-to-end IoT system for monitoring Peace Lily plant health using real sensors (Nicla Sense ME), wireless data transfer (MKR WiFi 1010 via MQTT), structured storage (SQLite + CSV), and a live analytical dashboard (Dash / Plotly).

The system captures:
- Temperature (°C)
- Humidity (%)
- VOC gas index (BSEC)
- Pressure (hPa)

Data is captured every 15 seconds for experimental analysis.

Research Question:
How do environmental fluctuations inside a typical apartment (temperature, humidity, VOC levels, pressure) influence the health and stress response of a Peace Lily over 24 hours?

This repo includes:
- Full Arduino firmware for Nicla and MKR WiFi
- MQTT subscriber
- SQLite database builder
- Dash dashboard
- Machine-learning ready data
- Documentation, metadata, and test suite


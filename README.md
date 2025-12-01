Smart Plant Guardian 🌿
A fully automated, data-driven environmental monitoring system for Peace Lily health assessment.

Project Overview
Smart Plant Guardian is an end-to-end environmental sensing and analytics system designed to measure and interpret the real-time health conditions of a Peace Lily (Spathiphyllum) in a typical apartment environment. Using an Arduino Nicla Sense ME (or MKR WiFi), the system continuously records:

Temperature,
Humidity,
VOC concentration and 
Atmospheric pressure

Data is streamed via MQTT or serial, stored following FAIR data principles, processed using Python, and visualised on an interactive Plotly Dash dashboard with a continuously updated plant Health Score.

Research Question:
How do environmental fluctuations inside a typical apartment (temperature, humidity, VOC levels, pressure) influence the health and stress response of a Peace Lily over 24 hours?


Repositery Structure Tree (BREAKDOWN)

README.md
'Main project description, setup instructions, features, and documentation links'

LICENSE
'Defines how the project can be used, modified, and shared'

.gitignore
'Specifies which files Git should ignore (e.g., temporary files, logs, build artefacts)'

📘 docs/

project_overview.md
'Explains the purpose, hypothesis, research question, and scientific motivation'

data_structure_and_metadata.md
'Documents how data is stored, formatted, labelled, and organised following FAIR principles'

risk_assessment.pdf
'A safety-oriented risk assessment for using electronics, sensors, and indoor plant experiments'

system_diagram.png
'Diagram showing how sensors, Arduino, MQTT/serial pipeline, Python processing, and the dashboard interact'

dashboard_screenshots/
'Images of the Plotly Dash interface demonstrating graphs, health score, and layout'

calibration_notes.md
'Detailed notes on how each sensor was calibrated (temperature, humidity, VOC, pressure)'

peace_lily_care_profile.md
'Scientific and horticultural profile of the Peace Lily, including optimal environmental conditions'

📊 data/

raw/
'Unmodified CSV files pulled directly from sensors'
Example:
 readings_2025-03-10.csv
 readings_2025-03-11.csv

processed/
'Cleaned data ready for analysis, including feature sets for modelling'
 cleaned_data.csv
 features_for_analysis.csv

database/
'Structured storage for long-term data access'
 plant_data.sqlite

🗂️ metadata/

experiment_info.json
 'Describes the experiment setup: location, dates, sensor type, plant ID, environment notes'

sensor_calibration.json
 'Holds calibration offsets and scale factors used by the acquisition code'

plant_profile_peacelily.json
 'Machine-readable environmental preferences (temp/humidity ranges, VOC sensitivity, etc.) used by the health-score algorithm'

🧠 src/

acquisition/
 'Code responsible for collecting sensor data from Arduino via MQTT or Serial'

 mqtt_subscriber.py – Receives sensor values published via WiFi/MQTT.
 serial_subscriber.py – Reads data from USB serial connection.
 arduino sketches (.ino files) – Firmware that runs on the Nicla Sense ME / MKR WiFi boards.

dashboard/
'Code for the interactive Plotly Dash web dashboard'

 dashboard.py – Main Dash app entry point.
 components/ – Modular UI elements (graph panel, plant image display, health card, email tab).
 assets/style.css – Custom CSS for layout and styling.

analysis/
'Notebooks and scripts used to interpret and visualise the data'

 exploratory_analysis.ipynb – Initial data exploration and graphs.
 health_score.py – Algorithm calculating plant health based on environmental factors.

utils/
'Supporting functions used across the project'

 compute_health_score.py – Reusable version of the health scoring logic.
 db_helpers.py – Tools for reading/writing SQLite data.
 email_sender.py – Sends alert emails when environment conditions exceed thresholds.
 real_data_helpers.py – Helpful functions for reading, cleaning, and validating time-series data.

📈 results/
'All generated outputs from analysis'

 figures/
'Plots created from the data - temperature, humidity, VOC, pressure graphs'

 analysis_reports/
'PDFs summarising findings, such as 24-hour Environmental Summary Report'

 trends/
'CSV summaries of long-term time series'

🔍 tests/

'Automated tests ensuring that all major components work correctly'
'Covers database operations, health score accuracy, dashboard UI components, and real sensor acquisition'


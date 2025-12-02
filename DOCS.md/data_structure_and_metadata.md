
# Data Structure & Metadata Description

## Data files
`data/raw/*.csv`  
Daily raw logs. Each row includes:
timestamp, temperature, humidity, voc, pressure, experiment_id

`data/database/plant_data.sqlite`  
Master SQL table:
readings(id, timestamp, temperature, humidity, voc, pressure, experiment_id)

## Metadata
### experiment_info.json
Records:
- experiment_id
- plant species
- location
- sampling rate
- hardware IDs

### sensor_calibration.json
Stores baseline calibration offsets.

### plant_profile_peacelily.json
Defines “ideal ranges” for health computation.

All metadata conforms to FAIR: human-readable, machine-readable, versioned.


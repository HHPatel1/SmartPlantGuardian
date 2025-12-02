
#include "Arduino.h"
#include "Arduino_BHY2.h"

// NICLA Sense ME real sensors
SensorXYZ accel(SENSOR_ID_ACC);
SensorBSEC bsec(SENSOR_ID_BSEC);

void setup() {
  Serial.begin(115200);
  while(!Serial);

  BHY2.begin();
  accel.begin();
  bsec.begin();

  Serial.println("Nicla Sense ME Plant Sensor - DATA");
}

void loop() {
  BHY2.update();

  float temperature = bsec.temperature;
  float humidity    = bsec.humidity;
  float voc         = bsec.gas;        // Bosch BSEC gas resistance in ohm
  float pressure    = bsec.pressure;   // in hPa

  String json = "{";
  json += "\"temperature\":" + String(temperature, 2) + ",";
  json += "\"humidity\":" + String(humidity, 2) + ",";
  json += "\"voc\":" + String(voc, 2) + ",";
  json += "\"pressure\":" + String(pressure, 2) + ",";
  json += "\"device_id\":\"NICLA-001\",";
  json += "\"experiment_id\":\"SPG-REAL-001\"";
  json += "}";

  Serial.println(json);
  delay(15000);
}


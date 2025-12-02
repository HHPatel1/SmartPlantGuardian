
#include <WiFiNINA.h>
#include <ArduinoMqttClient.h>

char ssid[] = "HomeNetwork";
char pass[] = "HomePassword";

const char broker[] = "test.mosquitto.org";
int port = 1883;
const char topic[] = "smartplant/readings";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  // Connect WiFi
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(2000);
  }

  // Connect MQTT
  while (!mqttClient.connect(broker, port)) {
    delay(5000);
  }

  Serial.println("MKR WiFi MQTT Publisher Ready");
}

void loop() {
  if (!mqttClient.connected()) {
    mqttClient.connect(broker, port);
  }

  // Forward serial JSON from NICLA
  if (Serial.available()) {
    String json = Serial.readStringUntil('\n');
    mqttClient.beginMessage(topic);
    mqttClient.print(json);
    mqttClient.endMessage();
  }
}


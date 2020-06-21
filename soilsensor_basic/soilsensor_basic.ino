#include <ArduinoMqttClient.h>
#include "Adafruit_seesaw.h"
Adafruit_seesaw ss;

#include "wifi.h"
#include "mqtt_settings.h"

MqttClient mqttClient(wifiClient);

// mqtt settings
char* broker = BROKER;
int   port = PORT;
char* topic = TOPIC;

// sensor settings
char* sensorId = "sensor1";
const int capLen = 60;  // number of readings in average
const int loopDelay = 500;  // milliseconds
// time between messages = capLen * loopDelay

void connectMqtt(char* clientId) {
  mqttClient.setId(clientId);

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  delay(100);

  connectWifi();
  connectMqtt(sensorId);

  if (!ss.begin(0x36)) {
    Serial.println("ERROR! seesaw not found");
    while (1);
  } else {
    Serial.print("seesaw started! version: ");
    Serial.println(ss.getVersion(), HEX);
  }
}

void sendMessage(uint16_t avg, float temp) {
  // send a json like message to the broker
  // {"moisture": 0, "temperature": 0.0, "sid": "1"}
  mqttClient.beginMessage(topic);
  mqttClient.print("{\"moisture\": ");
  mqttClient.print(avg);
  mqttClient.print(", \"temperature\": ");
  mqttClient.print(temp);
  mqttClient.print(", \"sid\": \"");
  mqttClient.print(sensorId);
  mqttClient.print("\"}");
  mqttClient.endMessage();
  Serial.println("message sent");
}

int count = 0;
uint16_t capacitanceSum = 0;

void loop() {
  mqttClient.poll();  // keep connection to broker alive

  uint16_t capread = ss.touchRead(0);

  if (count == capLen) {
    uint16_t avg = capacitanceSum / capLen;
    float tempC = ss.getTemp();
    Serial.print("Temperature: "); Serial.print(tempC); Serial.println("*C");
    Serial.print("Avgerage Capacitance: "); Serial.println(avg);
    sendMessage(avg, tempC);
    count = 0;
    capacitanceSum = 0;
  }
  capacitanceSum += capread;

  delay(loopDelay);
  count += 1;
}

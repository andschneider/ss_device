#include <ArduinoMqttClient.h>
#include "Adafruit_seesaw.h"
Adafruit_seesaw ss;

#include "wifi.h"

MqttClient mqttClient(wifiClient);

const char broker[] = "192.168.1.189";
int        port     = 1883;
const char topic[]  = "arduino/test";

// sensor settings
const int capLen = 60;
uint16_t capVals[capLen];
char* sensorId = "sensor1";
const int loopDelay = 2000;  // milliseconds

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

uint16_t capAvg(uint16_t vals[]) {
  uint16_t sum = 0;
  for (int i = 0; i < capLen; i++) {
    sum += vals[i];
  }
  uint16_t avg = sum / capLen;
  return avg;
}

void sendMessage(uint16_t avg, float temp) {
  // send a json like message to the broker
  // {moisture: 0, temperature: 0.0, sid: "1"}
  mqttClient.beginMessage(topic);
  mqttClient.print("{moisture: ");
  mqttClient.print(avg);
  mqttClient.print(", temperature: ");
  mqttClient.print(temp);
  mqttClient.print(", sid: ");
  mqttClient.print(sensorId);
  mqttClient.print("}");
  mqttClient.endMessage();
  Serial.println("message sent");
}

int count = 0;

void loop() {
  mqttClient.poll();  // keep connection to broker alive

  uint16_t capread = ss.touchRead(0);

  if (count == capLen) {
    uint16_t avg = capAvg(capVals);
    float tempC = ss.getTemp();
    Serial.print("Temperature: "); Serial.print(tempC); Serial.println("*C");
    Serial.print("Avgerage Capactitance: "); Serial.println(avg);
    sendMessage(avg, tempC);
    count = 0;
  }
  capVals[count] = capread;

  delay(loopDelay);
  count += 1;
}

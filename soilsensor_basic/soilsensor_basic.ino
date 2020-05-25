#include "Adafruit_seesaw.h"

Adafruit_seesaw ss;

void setup() {
  Serial.begin(115200);

  Serial.println("seesaw Soil Sensor example!");

  if (!ss.begin(0x36)) {
    Serial.println("ERROR! seesaw not found");
    while (1);
  } else {
    Serial.print("seesaw started! version: ");
    Serial.println(ss.getVersion(), HEX);
  }
}

const int capLen = 60;
uint16_t capVals[capLen];
int count = 0;

uint16_t capAvg(uint16_t vals[]) {
  uint16_t sum = 0;
  for (int i = 0; i < capLen; i++) {
    sum += vals[i];
    Serial.print("avg i: "); Serial.println(i);
  }
  uint16_t avg = sum / capLen;
  return avg;
}

void loop() {
  uint16_t capread = ss.touchRead(0);

  if (count == capLen) {
    uint16_t avg = capAvg(capVals);
    float tempC = ss.getTemp();
    Serial.print("Temperature: "); Serial.print(tempC); Serial.println("*C");
    Serial.print("Capacitive: "); Serial.println(capread);
    Serial.print("Avgerage: "); Serial.println(avg);
    //      sendMessage(avg, tempC);
    count = 0;
  }
  capVals[count] = capread;

  delay(500);
  count += 1;
  Serial.println(count);
}

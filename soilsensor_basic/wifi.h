#include <ESP8266WiFi.h>

#include "wifi_creds.h"

char* ssid = SECRET_SSID;
char* pass = SECRET_PASS;

WiFiClient wifiClient;

void connectWifi() {
  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();
}

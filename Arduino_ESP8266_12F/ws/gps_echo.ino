#include "HardwareSerial.h"
// what's the name of the hardware serial port?

// HardwareSerial Serial_Port0(UART0);

#define GPS_PORT Serial
#define DEBUG_PORT Serial1


uint32_t timer = millis();
char led_onoff = true;

void setup() {
  // GPIO Settings
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)

  
  // make this baud rate fast enough to we aren't waiting on it
  DEBUG_PORT.begin(115200);

  // wait for hardware serial to appear
  while (!DEBUG_PORT) delay(10);

  // 9600 baud is the default rate for the Ultimate GPS
  GPS_PORT.begin(115200);
}


void loop() {
  if (GPS_PORT.available()) {
    char c = GPS_PORT.read();
    DEBUG_PORT.write(c);
  }

  // Blinking
  if (millis() - timer > 1000){
    timer = millis();
    led_onoff = !led_onoff;
    digitalWrite(LED_BUILTIN, led_onoff);  // turn the LED on (HIGH is the voltage level)
  }
}
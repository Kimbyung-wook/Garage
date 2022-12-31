#include "Servo.h"

// #define GPIO_S3 10
// #define GPIO_S2  9
#define GPIO_D0 16 // PWM
#define GPIO_D3  0 // PWM
// #define GPIO_D4  2
#define GPIO_D5 14
#define GPIO_D6 12
#define GPIO_D7 13 // PWM
#define GPIO_D8 15 // PWM


Servo PWM1;
Servo PWM2;
int angle = 10;
int duty_us = 600;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)


  PWM1.attach(GPIO_D7, 600, 2100);
  PWM2.attach(GPIO_D8, 600, 2100);
  PWM1.writeMicroseconds(20);
  PWM2.writeMicroseconds(20);

  
}

// the loop function runs over and over again forever
void loop() {
  // angle = angle + 30;
  // if(angle > 180)
  //   angle = 0;
  // PWM1.write(angle);
  // PWM2.write(angle);

  duty_us = duty_us + 200;
  if(duty_us > 2100)
    duty_us = 400;
  PWM1.writeMicroseconds(duty_us);
  PWM2.writeMicroseconds(duty_us);

  delay(100);
}

/************************************/
// Include Headers
/************************************/
// #include "addon.h"
#define GPIO_S1  8
#define GPIO_S2  9
#define GPIO_S3 10
#define GPIO_D0 16 // PWM
#define GPIO_D3  0 // PWM
// #define GPIO_D4  2
#define GPIO_D5 14
#define GPIO_D6 12
#define GPIO_D7 13 // PWM
#define GPIO_D8 15 // PWM

#include "oled.h"
// #include "rotary_button.h"
// #include "mpu9250_custom.h"
#include "gps.h"
#include "tictok_us.h"

/************************************/
// Define Devices
/************************************/
#define GPS_PORT Serial
// #define DEBUG_PORT Serial1

Tictok_us* health_main  = new Tictok_us();
OLED* monitor           = new OLED();
GPS* gps                = new GPS(&GPS_PORT);
// ROTARY *Button = new ROTARY();

Tictok_us* health_rest  = new Tictok_us();
unsigned long last_loop_time = micros();
unsigned long now_loop_time = micros();
unsigned long size_loop_time = 100*1000;



int delay_ms = 100;
char led_onoff = true;
int cnt = 1;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, led_onoff);

  // DEBUG_PORT.begin(115200);

  monitor->setup_display();
  // Button->setupRotaryButton(GPIO_D7, GPIO_D6, GPIO_D5);
  gps->setup_gps();
}

void loop() {
  health_main->tic();
  
  led_onoff = !led_onoff;
  digitalWrite(LED_BUILTIN, led_onoff);
	
  gps->read_all();
  /************************************/
  // Display
  /************************************/
  // sprintf(monitor->msg[0], "T%5d - %4d %d", cnt++, Button->getRotateCnt(), Button->getButtonPress());
  sprintf(monitor->msg[0], "T%5d", cnt++);
  sprintf(monitor->msg[1], "C %7d R %7d", health_main->getdt(), health_rest->getdt());
  sprintf(monitor->msg[2], "Dsp %6d/Gps %6d", monitor->health_print.getdt(), gps->health_read.getdt());

  // GPS
  sprintf(monitor->msg[4], "Date: %02d/%02d/20%02d",     gps->gps_device->day, gps->gps_device->month, gps->gps_device->year);
  sprintf(monitor->msg[5], "Time: %02d:%02d:%02d.%03d",  gps->gps_device->hour, gps->gps_device->minute, gps->gps_device->seconds, gps->gps_device->milliseconds);
  sprintf(monitor->msg[6], "Fix %d Qual %d Sat %2d",      (int)gps->gps_device->fix, (int)gps->gps_device->fixquality, (int)gps->gps_device->satellites);
  sprintf(monitor->msg[7], "%c%9.6f%c%10.6f",            gps->gps_device->lat, gps->gps_device->latitudeDegrees,gps->gps_device->lon, gps->gps_device->longitudeDegrees);


  // DEBUG_PORT.println(monitor->msg[0]);
  // DEBUG_PORT.println(monitor->msg[1]);

  monitor->print();

	// Put in a slight delay to help debounce the reading
  health_main->toc();
  
  health_rest->tic();
  while(1){
    now_loop_time = micros();
    if(now_loop_time - last_loop_time > size_loop_time){
      last_loop_time = last_loop_time + size_loop_time;
      break;
    }
  }
  health_rest->toc();
  
}
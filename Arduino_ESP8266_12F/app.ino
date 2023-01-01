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
#include "mpu6500.h" // 6.0.3

/************************************/
// Define Devices
/************************************/
#define GPS_PORT Serial
// #define DEBUG_PORT Serial1

Tictok_us* perform_main = new Tictok_us();
OLED* monitor           = new OLED();
GPS* gps                = new GPS(&GPS_PORT);
bfs::Mpu6500* imu       = new bfs::Mpu6500();

Tictok_us* perform_rest  = new Tictok_us();
Tictok_us* perform_imu  = new Tictok_us();
unsigned long last_loop_time = micros();
unsigned long now_loop_time = micros();
unsigned long size_loop_time = 100*1000;

const int delay_ms = 100;
char led_onoff = true;
int cnt = 1;

/************************************/
// Rotary Button 
/************************************/
// Rotary Encoder Inputs
#define BUTTON_KEY  GPIO_D5
#define BUTTON_S1   GPIO_D6
#define BUTTON_S2   GPIO_D7

volatile int button_counter = 0;
volatile int button_s2 = 0;
volatile unsigned long last_rotary = 0;

volatile int button_clicked = false;
volatile unsigned long last_button_press = 0;

#define SHOW_GPS 1
#define SHOW_IMU 2
#define SHOW_PERFORM 3

int menu_mode = SHOW_GPS;

void setup() {
  int system_on = true;
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, led_onoff);

  Wire.setClock(400*1000);
  /************************************/
  // Display Initialization
  /************************************/
  int monitor_on  = monitor->setup_display();
  system_on = system_on & monitor_on;
  sprintf(monitor->msg[2], "1. Display is ON");
  monitor->print();


  /************************************/
  // Display Initialization
  /************************************/
  sprintf(monitor->msg[3], "2. Intialize IMU");
  monitor->print();
  /* I2C bus,  0x68 address */
  imu->Config(&Wire, bfs::Mpu6500::I2C_ADDR_PRIM);
  int imu_on =  imu->Begin()
                  // Set the accel range to 16G by default
                && imu->ConfigAccelRange(bfs::Mpu6500::ACCEL_RANGE_4G)
                  // Set the gyro range to 2000DPS by default
                && imu->ConfigGyroRange(bfs::Mpu6500::GYRO_RANGE_250DPS)
                  // Set the DLPF to 184HZ by default
                && imu->ConfigDlpfBandwidth(bfs::Mpu6500::DLPF_BANDWIDTH_92HZ)
                  // Set the sample rate divider
                && imu->ConfigSrd(19);                              
  system_on = system_on & imu_on;
  if(imu_on == true)    sprintf(monitor->msg[3], "2. IMU is ON");
  else                  sprintf(monitor->msg[3], ">> IMU failed");
  monitor->print();


  /************************************/
  // GPS Initialization
  /************************************/
  sprintf(monitor->msg[4], "Intialize GPS");
  monitor->print();
  int gps_on      = gps->setup_gps();
  system_on = system_on & gps_on;
  if(gps_on == true)    sprintf(monitor->msg[4], "3. GPS is ON");
  else                  sprintf(monitor->msg[4], ">> GPS is timeout");
  monitor->print();


  /************************************/
  // Rotary Button Settings
  /************************************/
	// Set encoder pins as inputs
  sprintf(monitor->msg[5], "4. Intialize Buttons");
  monitor->print();
	pinMode(BUTTON_S1,  INPUT);
	pinMode(BUTTON_S2,  INPUT);
	pinMode(BUTTON_KEY, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_S1),  isr_rotary_counter, RISING);
  attachInterrupt(digitalPinToInterrupt(BUTTON_KEY), isr_button_click,   CHANGE);
  sprintf(monitor->msg[5], "4. Buttons are ON");
  monitor->print();


  // Finalize system set-up
  if(system_on == false){
    while(1){
      sprintf(monitor->msg[1], "System failed %d", (int)led_onoff);
      monitor->print();
      led_onoff = !led_onoff;
      delay(delay_ms);
    }
  }
  delay(1000);
}





void loop() {
  perform_main->tic();
  
  led_onoff = !led_onoff;
  digitalWrite(LED_BUILTIN, led_onoff);
	
  // Read Data
  int gps_health = gps->read_all();
  perform_imu->tic();
  int imu_health = imu->Read();
  perform_imu->toc();

  // Menu Selection
  int button = button_clicked;
  button_clicked = false;
  if (button == true){
    menu_mode++;
    if(menu_mode > SHOW_PERFORM)
      menu_mode = SHOW_GPS;
  }

  /************************************/
  // Display
  /************************************/
  sprintf(monitor->msg[1], "C  %6d/R  %6d", perform_main->getdt(), perform_rest->getdt());
  switch(menu_mode){
    case SHOW_GPS:
      sprintf(monitor->msg[0], "T%5d   GPS %6d", cnt++, gps->perform_read.getdt());
      sprintf(monitor->msg[2], "Dsp%6d/Gps%6d", monitor->perform_print.getdt(), gps->perform_read.getdt());
      sprintf(monitor->msg[3], "Cnt %4d / Button %d", button_counter, button);
      sprintf(monitor->msg[4], "Date: %02d/%02d/20%02d",     gps->gps_device->day, gps->gps_device->month, gps->gps_device->year);
      sprintf(monitor->msg[5], "Time: %02d:%02d:%02d.%03d",  gps->gps_device->hour, gps->gps_device->minute, gps->gps_device->seconds, gps->gps_device->milliseconds);
      sprintf(monitor->msg[6], "Fix %d Qual %d Sat %2d",      (int)gps->gps_device->fix, (int)gps->gps_device->fixquality, (int)gps->gps_device->satellites);
      sprintf(monitor->msg[7], "%c%9.6f%c%10.6f",            gps->gps_device->lat, gps->gps_device->latitudeDegrees,gps->gps_device->lon, gps->gps_device->longitudeDegrees);
    break;
    case SHOW_IMU:
      sprintf(monitor->msg[0], "T%5d   IMU %6d", cnt++, perform_imu->getdt());
      sprintf(monitor->msg[2],"Ax %10.5f", imu->accel_x_mps2());
      sprintf(monitor->msg[3],"Ay %10.5f", imu->accel_y_mps2());
      sprintf(monitor->msg[4],"Az %10.5f", imu->accel_z_mps2());
      sprintf(monitor->msg[5],"Wx %10.5f", imu->gyro_x_radps());
      sprintf(monitor->msg[6],"Wy %10.5f", imu->gyro_y_radps());
      sprintf(monitor->msg[7],"Wz %10.5f", imu->gyro_z_radps());
    break;
    case SHOW_PERFORM:
      sprintf(monitor->msg[0], "T%5d   PERFORM", cnt++);
      sprintf(monitor->msg[2], "MAIN %6d", perform_main->getdt());
      sprintf(monitor->msg[2], "DISP %6d", monitor->perform_print.getdt());
      sprintf(monitor->msg[3], "GPS  %6d", gps->perform_read.getdt());
      sprintf(monitor->msg[4], "IMU  %6d", perform_imu->getdt());
      sprintf(monitor->msg[5]," ");
      sprintf(monitor->msg[6]," ");
      sprintf(monitor->msg[7]," ");
    break;
  }

  monitor->print();

	// Put in a slight delay to help debounce the reading
  perform_main->toc();
  
  perform_rest->tic();
  while(1){
    now_loop_time = micros();
    if(now_loop_time - last_loop_time > size_loop_time){
      last_loop_time = last_loop_time + size_loop_time;
      break;
    }
  }
  perform_rest->toc();
  
}


/************************************/
// Interrupt Service Routines
/************************************/
IRAM_ATTR void isr_rotary_counter(){
  if(last_rotary - millis() < 20)
    return;
  last_rotary = millis();
  
  button_s2 = digitalRead(BUTTON_S2);
  if (button_s2 == true)
    button_counter --;
  else // Encoder is rotating S2 so increment
    button_counter ++;
}

IRAM_ATTR void isr_button_click(){
  if(last_button_press - millis() < 500){
    button_clicked = true;
  }
  last_button_press = millis();
}
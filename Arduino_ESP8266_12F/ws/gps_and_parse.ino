// Test code for Ultimate GPS Using Hardware DEBUG_PORT (e.g. GPS Flora or FeatherWing)
//
// This code shows how to listen to the GPS module via polling. Best used with
// Feathers or Flora where you have hardware DEBUG_PORT and no interrupt
//
// Tested and works great with the Adafruit GPS FeatherWing
// ------> https://www.adafruit.com/products/3133
// or Flora GPS
// ------> https://www.adafruit.com/products/1059
// but also works with the shield, breakout
// ------> https://www.adafruit.com/products/1272
// ------> https://www.adafruit.com/products/746
//
// Pick one up today at the Adafruit electronics shop
// and help support open source hardware & software! -ada

#include <Adafruit_GPS.h>

// what's the name of the hardware serial port?
#define GPS_PORT Serial
#define DEBUG_PORT Serial1

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPS_PORT);
char connect_gps = false;

// Set GPSECHO to 'false' to turn off echoing the GPS data to the DEBUG_PORT console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t disp_timer = millis();
char led_onoff = true;

void setup()
{
  // GPIO Settings
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)


  // Debug Setting
  DEBUG_PORT.begin(115200);
  DEBUG_PORT.println("Adafruit GPS library basic parsing test!");


  // GPS Setting
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  // GPS.begin(9600);
  // GPS.sendCommand(PMTK_SET_BAUD_115200);

  GPS.begin(115200);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate

  delay(1000);
}

void loop() // run over and over again
{

  /************************************/
  // Frequency Manager
  // Outputs
  //   char disp_now : frequency indicator
  /************************************/
  int disp_now = false;
  if (millis() - disp_timer > 1000){
    disp_timer = millis();
    disp_now = true;
  }


  /************************************/
  // GPS Parser
  // Outputs
  //   Adafruit_GPS GPS : GPS Data
  //   connect_gps : GPS Connection status
  /************************************/
  char c = false;
  do{
    c = GPS.read();
  }while(c);

  // Verifying GPS Connection
  char get_new_gps = GPS.newNMEAreceived();
  connect_gps = connect_gps || get_new_gps;
  if ((connect_gps == false) && (disp_now == true))
    DEBUG_PORT.println("GPS is NOT connected...");

  // if a sentence is received, we can check the checksum, parse it...
  if (get_new_gps) {
    // DEBUG_PORT.print(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())){ // this also sets the newNMEAreceived() flag to false
      DEBUG_PORT.println("GPS Failed!!");
      return; // we can fail to parse a sentence in which case we should just wait for another
    }
  }

  // Disp GPS Data
  if((connect_gps == true) && (disp_now == true)){
    DEBUG_PORT.print("\nTime: ");
    if (GPS.hour < 10) { DEBUG_PORT.print('0'); }
    DEBUG_PORT.print(GPS.hour, DEC); DEBUG_PORT.print(':');
    if (GPS.minute < 10) { DEBUG_PORT.print('0'); }
    DEBUG_PORT.print(GPS.minute, DEC); DEBUG_PORT.print(':');
    if (GPS.seconds < 10) { DEBUG_PORT.print('0'); }
    DEBUG_PORT.print(GPS.seconds, DEC); DEBUG_PORT.print('.');
    if (GPS.milliseconds < 10) {
      DEBUG_PORT.print("00");
    } else if (GPS.milliseconds > 9 && GPS.milliseconds < 100) {
      DEBUG_PORT.print("0");
    }
    DEBUG_PORT.println(GPS.milliseconds);
    DEBUG_PORT.print("Date: ");
    DEBUG_PORT.print(GPS.day, DEC); DEBUG_PORT.print('/');
    DEBUG_PORT.print(GPS.month, DEC); DEBUG_PORT.print("/20");
    DEBUG_PORT.println(GPS.year, DEC);
    DEBUG_PORT.print("Fix: "); DEBUG_PORT.print((int)GPS.fix);
    DEBUG_PORT.print(" quality: "); DEBUG_PORT.println((int)GPS.fixquality);
    if (GPS.fix) {
      DEBUG_PORT.print("Location: ");
      DEBUG_PORT.print(GPS.latitude, 4); DEBUG_PORT.print(GPS.lat);
      DEBUG_PORT.print(", ");
      DEBUG_PORT.print(GPS.longitude, 4); DEBUG_PORT.println(GPS.lon);
      DEBUG_PORT.print("Speed (knots): "); DEBUG_PORT.println(GPS.speed);
      DEBUG_PORT.print("Angle: "); DEBUG_PORT.println(GPS.angle);
      DEBUG_PORT.print("Altitude: "); DEBUG_PORT.println(GPS.altitude);
      DEBUG_PORT.print("Satellites: "); DEBUG_PORT.println((int)GPS.satellites);
      DEBUG_PORT.print("Antenna status: "); DEBUG_PORT.println((int)GPS.antenna);
    }
  }
  


  /************************************/
  // Blinker
  /************************************/
  if(disp_now == true){
    digitalWrite(LED_BUILTIN, led_onoff);  // turn the LED on (HIGH is the voltage level)
    led_onoff = !led_onoff;
  }
}
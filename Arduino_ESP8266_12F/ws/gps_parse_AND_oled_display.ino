#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GPS.h>

#define GPS_PORT Serial
#define DEBUG_PORT Serial1

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPS_PORT);
char connect_gps = false;
char cnt_nc_gps = 0; // How many times didn't get data
const char cnt_nc_gps_max = 5;

uint32_t disp_timer = millis();
char led_onoff = true;


/************************************/
// Display Setting
/************************************/
#define DISP_LINE_ROW 21
#define DISP_LINE_COLUMN 5
char msg[DISP_LINE_COLUMN][DISP_LINE_ROW];

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup()
{
  /************************************/
  // GPIO Settings
  /************************************/
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)



  /************************************/
  // Debug Setting
  /************************************/
  DEBUG_PORT.begin(115200);
  DEBUG_PORT.println("Adafruit GPS library basic parsing test!");
  delay(500);


  /************************************/
  // Display Settings
  /************************************/
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    DEBUG_PORT.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  display.clearDisplay();

  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(0,0);             // Start at top-left corner
  display.println(F("Hello, world! TESTETSTESTET"));

  display.display();
  delay(500);


  /************************************/
  // GPS Setting
  /************************************/
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_BAUD_115200);
  GPS.sendCommand(PMTK_SET_BAUD_115200);
  delay(500);
  GPS.sendCommand(PMTK_SET_BAUD_115200);
  delay(500);

  GPS.begin(115200);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_5HZ); // 1 Hz update rate

  delay(500);

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
    cnt_nc_gps = 0;
    // DEBUG_PORT.print(GPS.lastNMEA());
    if (!GPS.parse(GPS.lastNMEA())){
      DEBUG_PORT.println("GPS Failed!!");
      return;
    }
  }
  else{ // Didn't get data now
    // If you cant get 5 times, GPS status change to N/C
    if(disp_now == true){
      // DEBUG_PORT.println("GPS Connection is weird");
      cnt_nc_gps++;
      if(cnt_nc_gps > cnt_nc_gps_max){
        cnt_nc_gps = cnt_nc_gps_max;
        connect_gps = false;
      }
    }
  }

  // Disp GPS Data
  if((connect_gps == true) && (disp_now == true)){
    DEBUG_PORT.print("Time: ");
    if (GPS.hour < 10) { DEBUG_PORT.print('0'); }                 DEBUG_PORT.print(GPS.hour, DEC); DEBUG_PORT.print(':');
    if (GPS.minute < 10) { DEBUG_PORT.print('0'); }               DEBUG_PORT.print(GPS.minute, DEC); DEBUG_PORT.print(':');
    if (GPS.seconds < 10) { DEBUG_PORT.print('0'); }              DEBUG_PORT.print(GPS.seconds, DEC); DEBUG_PORT.print('.');
    if (GPS.milliseconds < 10) {                                  DEBUG_PORT.print("00");
    } else if (GPS.milliseconds > 9 && GPS.milliseconds < 100) {  DEBUG_PORT.print("0");
    }
    DEBUG_PORT.println(GPS.milliseconds);
    
    DEBUG_PORT.print("Date: ");     DEBUG_PORT.print(GPS.day, DEC);
    DEBUG_PORT.print('/');          DEBUG_PORT.print(GPS.month, DEC);
    DEBUG_PORT.print("/20");        DEBUG_PORT.println(GPS.year, DEC);

    DEBUG_PORT.print("Fix: ");          DEBUG_PORT.print((int)GPS.fix);
    DEBUG_PORT.print(" quality: ");     DEBUG_PORT.println((int)GPS.fixquality);

    sprintf(msg[1],"Date: %02d/%02d/20%02d", GPS.day, GPS.month, GPS.year);
    sprintf(msg[0],"Time: %02d:%02d:%02d.%03d", GPS.hour, GPS.minute, GPS.seconds, GPS.milliseconds);
    sprintf(msg[2], "Fix %d Qual %d Sat %d", (int)GPS.fix, (int)GPS.fixquality, (int)GPS.satellites);

    if (GPS.fix) {
      DEBUG_PORT.print("Location: ");
      DEBUG_PORT.print(GPS.latitude, 4); DEBUG_PORT.print(GPS.lat);

      DEBUG_PORT.print(", ");
      DEBUG_PORT.print(GPS.longitude, 4); DEBUG_PORT.println(GPS.lon);

      DEBUG_PORT.print("Altitude: "); DEBUG_PORT.println(GPS.altitude);

      sprintf(msg[3], "%c%9.4f",GPS.lat, GPS.latitudeDegrees);
      sprintf(msg[4], "%c%10.4f",GPS.lon, GPS.longitudeDegrees);
      sprintf(msg[5], "Alt : %10.4f m",GPS.altitude);

    }
    display.clearDisplay();
    display.setCursor(0,0);             // Start at top-left corner
    for (int i = 0; i < DISP_LINE_COLUMN; i++){
      if((GPS.fix == false) && (i > 2))
        break;
      display.println(msg[i]);
    }
    display.display();
  }
  


  /************************************/
  // Blinker
  /************************************/
  if(disp_now == true){
    digitalWrite(LED_BUILTIN, led_onoff);  // turn the LED on (HIGH is the voltage level)
    led_onoff = !led_onoff;
  }
}
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

// Set GPSECHO to 'false' to turn off echoing the GPS data to the DEBUG_PORT console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();


void setup()
{
  //while (!DEBUG_PORT);  // uncomment to have the sketch wait until DEBUG_PORT is ready

  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  DEBUG_PORT.begin(115200);
  DEBUG_PORT.println("Adafruit GPS library basic parsing test!");

  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(115200);
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  // GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);

  // Ask for firmware version
  GPS_PORT.println(PMTK_Q_RELEASE);
}

void loop() // run over and over again
{
  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if (GPSECHO)
    if (c) DEBUG_PORT.print(c);
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trying to print out data
    DEBUG_PORT.print(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }

  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) {
    timer = millis(); // reset the timer
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
}
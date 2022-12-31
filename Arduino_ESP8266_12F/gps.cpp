#include "gps.h"

GPS::GPS(HardwareSerial* SerialPort){
  gps_device = new Adafruit_GPS(SerialPort);
  last_recv = 0;
  timeout_gps_failed = 3000;
  gps_connection = false;
}
GPS::~GPS(){
  delete(gps_device);
  gps_device = NULL;
}

void GPS::setup_gps(){
  /************************************/
  // GPS Setting
  /************************************/
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  gps_device->begin(9600);
  gps_device->sendCommand(PMTK_SET_BAUD_115200);
  gps_device->sendCommand(PMTK_SET_BAUD_115200);
  delay(300);
  gps_device->sendCommand(PMTK_SET_BAUD_115200);
  delay(300);

  gps_device->begin(115200);
  gps_device->sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  //gps_device->sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  gps_device->sendCommand(PMTK_SET_NMEA_UPDATE_5HZ); // 1 Hz update rate
  delay(300);
}

int GPS::read_all(){
  health_read.tic();
  /************************************/
  // GPS Parser
  // Outputs
  //   Adafruit_GPS GPS : GPS Data
  /************************************/
  char get_new_gps = false;
  char c = false;
  do{
    c = gps_device->read();
    get_new_gps = gps_device->newNMEAreceived();
    if(get_new_gps == true)
    {
      last_recv = millis();
      if (!gps_device->parse(gps_device->lastNMEA())){
        // DEBUG_PORT.println("GPS Failed!!");
        continue;
      }
    }
  }while(c);

  // Check GPS Timeout
  if(millis() - last_recv > timeout_gps_failed)
    gps_connection = true;
  else
    gps_connection = false;

  health_read.toc();

  return gps_connection;
}
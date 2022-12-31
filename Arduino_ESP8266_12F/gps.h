#ifndef _GPS_H_
#define _GPS_H_
#include <Adafruit_GPS.h>
#include "tictok_us.h"

class GPS{

public:
  GPS(HardwareSerial* SerialPort);
  ~GPS();

public:
  void setup_gps();
  int read_all();

public:
  Adafruit_GPS* gps_device;
  Tictok_us health_read;

private:
  int gps_connection;
  unsigned long last_recv;
  unsigned long timeout_gps_failed;

};

#endif // _GPS_H_
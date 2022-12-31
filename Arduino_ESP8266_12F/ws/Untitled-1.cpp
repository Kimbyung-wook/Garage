#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_AM2320.h>


int sec = 0;

/************************************/
// Built-In LED
/************************************/
char led_onoff = true;

/************************************/
// Display Setting
/************************************/
#define DISP_LINE_ROW 21
#define DISP_LINE_COLUMN 8
char msg[DISP_LINE_COLUMN][DISP_LINE_ROW];

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

/******************************************/
// Temperature and Humidity Sensor AM2320
/******************************************/
Adafruit_AM2320 am2320 = Adafruit_AM2320(&Wire);

void setup() {

  /************************************/
  // Built-In LED
  /************************************/
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)


  /************************************/
  // SSD1306 Display Setting
  /************************************/
  Serial.begin(115200);
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  display.clearDisplay();

  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(0,0);             // Start at top-left corner
  display.println(F("Hello, world! TESTETSTESTET"));

  display.display();

  /******************************************/
  // Temperature and Humidity Sensor AM2320
  /******************************************/
  am2320.begin();
}

void loop() {

  /************************************/
  // Built-In LED
  /************************************/
  led_onoff = !led_onoff;
  digitalWrite(LED_BUILTIN, led_onoff);  // turn the LED on (HIGH is the voltage level)


  // Displaying
  display.clearDisplay();
  display.setCursor(0,0);             // Start at top-left corner

  sprintf(msg[3], "Temp : %6.2f c", am2320.readTemperature());
  sprintf(msg[4], "Humi : %6.2f \%", am2320.readHumidity());
  for (int i = 0; i < DISP_LINE_COLUMN; i++){
    // sprintf(msg[i],"%d : Hello, world! %d",i+1, sec);
    display.println(msg[i]);
  }
  display.display();

  sec++;
  delay(1000);                      // wait for a second
}

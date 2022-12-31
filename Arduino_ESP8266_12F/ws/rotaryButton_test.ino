
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Display Setting
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

int delay_ms = 100;
char led_onoff = true;
int cnt = 1;

// Rotary Encoder Inputs
#define SW  GPIO_D5
#define CLK GPIO_D6
#define DT  GPIO_D7

int counter = 0;
int currentStateCLK;
int currentStateDT;
int lastStateCLK;
char currentDir = 'R';
unsigned long lastButtonPress = 0;

void setup() {
	
	// Set encoder pins as inputs
	pinMode(CLK, INPUT);
	pinMode(DT,  INPUT);
	pinMode(SW,  INPUT_PULLUP);

	// Read the initial state of CLK
	lastStateCLK = digitalRead(CLK);


  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, led_onoff);
  /************************************/
  // Display Settings
  /************************************/
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);
  display.clearDisplay();

  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(0,0);             // Start at top-left corner
  display.println(F("Hello, world! TESTETSTESTET"));

  display.display();
}

void loop() {
  led_onoff = !led_onoff;
  digitalWrite(LED_BUILTIN, led_onoff);
	
  sprintf(msg[0],"Pulse %4d -", cnt++);

	// Read the current state of CLK
	currentStateCLK = digitalRead(CLK);
  currentStateDT  = digitalRead(DT);
	// If last and current state of CLK are different, then pulse occurred
	// React to only 1 state change to avoid double count
	if (currentStateCLK != lastStateCLK  && currentStateCLK == 1){

		// If the DT state is different than the CLK state then
		// the encoder is rotating CCW so decrement
		if (currentStateDT != currentStateCLK) {
			counter --;
			currentDir = 'R';
		} else {
			// Encoder is rotating CW so increment
			counter ++;
			currentDir = 'L';
		}

    sprintf(msg[2], "Direction: %c", currentDir);
    sprintf(msg[3], "Counter: %d", counter);
	}

	// Remember last CLK state
	lastStateCLK = currentStateCLK;

	// Read the button state
	int btnState = digitalRead(SW);

	//If we detect LOW signal, button is pressed
	if (btnState == LOW) {
		//if 50ms have passed since last LOW pulse, it means that the
		//button has been pressed, released and pressed again
		if (millis() - lastButtonPress > 100) {
      sprintf(msg[4],"Button pressed!");
		}

		// Remember last button press event
		lastButtonPress = millis();
	}

  /************************************/
  // Display Settings
  /************************************/
  display.clearDisplay();
  display.setCursor(0,0);             // Start at top-left corner
  for (int i = 0; i < DISP_LINE_COLUMN; i++){
    display.println(msg[i]);
  }
  display.display();


	// Put in a slight delay to help debounce the reading
	delay(1);
}
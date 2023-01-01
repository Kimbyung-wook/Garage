#include "oled.h"

OLED::OLED()
{
  display_device = Adafruit_SSD1306(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
  for (int i = 0; i < DISP_LINE_COLUMN; i++){
    for (int j = 0; j < DISP_LINE_ROW; j++)
      msg[i][j] = '\0';
  }
  // memcpy(msg[0],'\0',DISP_LINE_ROW*DISP_LINE_COLUMN);
}

int OLED::setup_display()
{ /************************************/
  // Display Settings
  /************************************/
  display_device.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);
  display_device.clearDisplay();
  delay(100);

  display_device.setTextSize(1);             // Normal 1:1 pixel scale
  display_device.setTextColor(SSD1306_WHITE);        // Draw white text
  display_device.setCursor(0,0);             // Start at top-left corner
  display_device.println(F("Display Initialize"));

  delay(100);
  display_device.display();
  return true;
}

// void OLED::writeln(int line_in, char* text_in, unsigned int size_in){
//   int line = max(0, min(line_in, DISP_LINE_COLUMN-1));
//   size_t size = (size_t)min(size_in, (unsigned int)DISP_LINE_ROW);
//   strncpy(&msg[line][0], text_in, size);
// }

void OLED::print()
{
  perform_print.tic();
  /************************************/
  // Display Settings
  /************************************/
  display_device.clearDisplay();
  display_device.setCursor(0,0);             // Start at top-left corner
  for (int i = 0; i < DISP_LINE_COLUMN; i++){
    display_device.println(msg[i]);
  }
  display_device.display();

  perform_print.toc();
}
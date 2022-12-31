#pragma once
#define _H_MENU

#ifndef _H_OLED_DISPLAY
#include "oled_display.h"
#endif

#define MENU_SELECT 1
#define MENU_WAIT -1

class MenuDisplay{
  public:
    MenuDisplay(OLED_Display Display);
    ~MenuDisplay();
    void SetMenu(int RotaryCounter, int* ButtonPressed);
    int getMenuLevel();

  private:
    int menu_cursor = MENU_WAIT; // 
    int menu_cursor_max = 6;

  private:
    int menu_top_max = 6;
    char menu_top_string[menu_top_max][DISP_LINE_ROW] = {
      "  Main View",
      "  Motor Settings",
      "  Sensor Status",
      "  Filter Status",
      "  Sensor Calibration",
      "  Statics"
    };

    int menu_03_max = 9;
    char menu_03_string[menu_03_max][DISP_LINE_ROW] = {
     //123456789012345678901
      "  Show Acc Raw",
      "  Show Gyro Raw",
      "  Show Mag Raw",
      "  Show Acc Bias",
      "  Show Gyro Bias",
      "  Show Mag Calib",
      "  Calib Acc Bias",
      "  Calib Gyro Bias",
      "  Calib Mag Iron",
    }


    int menu_level[2] = {};
    unsigned int menu_level[2] = {0,0}; // hierarchy and case
    unsigned int menu_top_max = 10;
    unsigned int menu_min_max[2] = {0, DISP_LINE_COLUMN-3};
    unsigned int menu_line_max = 6;
    int counter_prev = 0;
    char menu_case[10][DISP_LINE_ROW] = { "  [Back]",     "  Menu02",  "  Menu03",  "  Menu04",  "  Menu05",
                                          "  [To Top] ",  "  Menu07",  "  Menu08",  "  Menu09",  "  Menu10" };

  private:
    char view_msg;



}
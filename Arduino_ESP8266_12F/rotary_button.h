#pragma once
#ifndef _ROTARY_BUTTON_H_
#define _ROTARY_BUTTON_H_

#include <Arduino.h>


class ROTARY{
  public:
    ROTARY();
    ~ROTARY();

  public:
    void setupRotaryButton(uint8_t s1_in, uint8_t s2_in, uint8_t key_in);
  
    int getButtonPress();
    void pushButton();
    
    int getRotateCnt();
    uint8_t gets2();
    void increaseRotateCnt();
    void decreaseRotateCnt();

  private:
    uint8_t s1;
    uint8_t s2;
    uint8_t key;

    volatile int button_pressed;
    void ReleaseButton();

    volatile int rotary_counter;
    volatile unsigned long last_rotary_millis;
    void setRotaryMillis();
    unsigned long getRotaryMillis();

    static ROTARY* sRotary;
    static void isr_rotary_counter();
    static void isr_button_click();
    
};
#endif // _ROTARY_BUTTON_H_
#include "rotary_button.h"

ROTARY* ROTARY::sRotary = nullptr;

ROTARY::ROTARY(){
  button_pressed = -2;
};

void ROTARY::setupRotaryButton(uint8_t s1_in, uint8_t s2_in, uint8_t key_in){
  s1  = s1_in;
  s2  = s2_in;
  key = key_in;

  /************************************/
  // Rotary Button Settings
  /************************************/
	// Set encoder pins as inputs
	pinMode(s1,   INPUT);
	pinMode(s2,   INPUT);
	pinMode(key,  INPUT_PULLUP);

  sRotary = this;
  attachInterrupt(digitalPinToPort(s1),  ROTARY::isr_rotary_counter, RISING);
  attachInterrupt(digitalPinToPort(key), ROTARY::isr_button_click,   CHANGE);
}

int ROTARY::getButtonPress(){
  int return_value = button_pressed;
  // ReleaseButton();
  return return_value;
}
void ROTARY::pushButton(){
  button_pressed = true;
}

int ROTARY::getRotateCnt(){
  return rotary_counter;
}
uint8_t ROTARY::gets2(){
  return s2;
}
void ROTARY::increaseRotateCnt(){
  rotary_counter++;
}
void ROTARY::decreaseRotateCnt(){
  rotary_counter--;
}

void ROTARY::ReleaseButton(){
  button_pressed = false;
}

void ROTARY::setRotaryMillis(){
  last_rotary_millis = millis();
}
unsigned long ROTARY::getRotaryMillis(){
  return last_rotary_millis;
}

IRAM_ATTR void ROTARY::isr_rotary_counter(){
  if(sRotary == nullptr)
    return;

  // if(sRotary->getRotaryMillis() - millis() < 20)
  //   return;
  // sRotary->setRotaryMillis();
  
  if (digitalRead(sRotary->gets2()) == true) {
    sRotary->decreaseRotateCnt();
  } else {
    sRotary->increaseRotateCnt();
  }
}

IRAM_ATTR void ROTARY::isr_button_click(){
  if(sRotary == nullptr)
    return;
  // if(sRotary->getRotaryMillis() - millis() < 500){
  sRotary->pushButton();
  // }
  // sRotary->setRotaryMillis();
}
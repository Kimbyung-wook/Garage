#include "tictok_ms.h"

Tictok_ms::Tictok_ms(){
  last_tic = 0;
}
void Tictok_ms::tic(){
  last_tic = millis();
}
unsigned long Tictok_ms::toc(){
  dt = millis() - last_tic;
  return dt;
}
unsigned long Tictok_ms::getdt(){
  return dt;
}
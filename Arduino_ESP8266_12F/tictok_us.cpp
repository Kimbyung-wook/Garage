#include "tictok_us.h"

Tictok_us::Tictok_us(){
  last_tic = 0;
}
void Tictok_us::tic(){
  last_tic = micros();
}
unsigned long Tictok_us::toc(){
  dt = micros() - last_tic;
  return dt;
}
unsigned long Tictok_us::getdt(){
  return dt;
}
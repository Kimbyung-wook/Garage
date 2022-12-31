#pragma once
#ifndef _TICTOC_US_H_
#define _TICTOC_US_H_

#include <Arduino.h>

class Tictok_us{
public:
  Tictok_us();
  ~Tictok_us();

public:
  void tic();
  unsigned long toc();
  unsigned long getdt();

public:
  unsigned long last_tic = 0;
  unsigned long dt = 0;
};

#endif // _TICTOC_US_H_
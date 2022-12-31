#pragma once
#ifndef _TICTOC_MS_H_
#define _TICTOC_MS_H_

#include <Arduino.h>

class Tictok_ms{
public:
  Tictok_ms();
  ~Tictok_ms();

public:
  void tic();
  unsigned long toc();
  unsigned long getdt();

public:
  unsigned long last_tic = 0;
  unsigned long dt = 0;
};

#endif // _TICTOC_MS_H_
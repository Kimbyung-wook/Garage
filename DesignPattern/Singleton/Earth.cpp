#include <stdio.h>
#include "Earth.hpp"
 
double Earth::getRadius(){
    return radius;
}
 
void Earth::showSiderealPeriod(){
    printf("Sidereal Period of Earth is %6.2f days per a year\n",year2day);
    return;
}
 
 
void Earth::setNumber(int in){
    number = in;
}
int Earth::getNumber(){
    return number;
}
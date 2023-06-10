#include "Earth.hpp"
#include <stdio.h>
 
int main()
{
    Earth* PlanetEarth1 = Earth::getInstance();
    Earth* PlanetEarth2 = Earth::getInstance();
 
    PlanetEarth1->showSiderealPeriod();
    PlanetEarth1->setNumber(1);
    printf("Earth1 : %d\n",PlanetEarth1->getNumber());
 
    PlanetEarth2->showSiderealPeriod();
    PlanetEarth2->setNumber(2);
    printf("Earth2 : %d\n",PlanetEarth2->getNumber());
    printf("Earth1 : %d\n",PlanetEarth1->getNumber());
 
    return 0;
}

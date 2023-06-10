#ifndef __EARTH_HPP__
#define __EARTH_HPP__
 
#include "Singleton.hpp"
 
class Earth : public Singleton<Earth>{
    public : 
        Earth(){};
        ~Earth(){};
 
        double getRadius();
        void showSiderealPeriod();
        void setNumber(int);
        int getNumber();
 
    private :
        double radius = 6483000;
        double year2day = 365.24;
        double day2hour = 24.0000;
        int number = 0;
};
 
#endif // __EARTH_HPP__
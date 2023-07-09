#ifndef __ENGINE_HPP__
#define __ENGINE_HPP__
#include "singleton.hpp"

class Engine : public Singleton<Engine> {
    public : 
        Engine();
        Engine(double dt);
        ~Engine();

        struct EngineOut{
            double RPM;
            double Volt;
            double Temp;
        };

    public : 
        void init();
        EngineOut getState();
        void setAction(double Throttle);
        void update();
        void update(double throttle);
        // void EngineOff();
        // void EngineOn();

    private : 
        void step();

    private : 
        double Time;
        double dt;
        double Inertia;
        double alpha;
        double Torque;
        double omega;
        double KV;
        double throttle;
        EngineOut state;
};

#endif // __ENGINE_HPP__
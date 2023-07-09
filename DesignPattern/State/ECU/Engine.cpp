#include "Engine.hpp"
#define _USE_MATH_DEFINES
#include "math.h"
#define MIN(a,b) (a<b ? a : b)
#define MAX(a,b) (a>b ? a : b)
#define MINMAX(mini,value,maxi) MAX(mini,MIN(value, maxi))

Engine::Engine(){
    Time    = 0.0;
    dt      = 0.01;
    Inertia = 1.0;
    alpha   = dt/Inertia;
    Torque  = 0.0;
    omega   = 0.0;
    KV      = 12.0;
    throttle= 0.0;
}

Engine::Engine(double dt_in){
    dt = dt_in;
}

Engine::~Engine(){
    return;
}

void Engine::init(){
    Time    = 0.0;
    return;
}

Engine::EngineOut Engine::getState(){
    return state;
}

void Engine::setAction(double throttle_in){
    throttle = MINMAX(0.0, throttle_in, 1.0);
}

void Engine::update(){
    Torque = 320.0 * throttle;

    step();

    state.RPM  = omega*60.0/M_PI;
    state.Volt = state.RPM*KV;
    state.Temp = 0.0;
}

void Engine::update(double throttle_in){
    throttle = throttle_in;
    update();
}

void Engine::step(){
    Time = Time + dt;
    omega = omega * (1.0-alpha) + Torque * alpha;
    return;
}
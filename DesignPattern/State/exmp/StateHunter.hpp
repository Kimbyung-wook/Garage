//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "singleton.hpp"
#include "Hunter.hpp"

class StateHunter{
    public : 
        char stateName[10];
        virtual void Move(  Hunter* hunter) = 0;
        virtual void Eat(   Hunter* hunter) = 0;
        virtual void Attack(Hunter* hunter) = 0;
        virtual void Idle(  Hunter* hunter) = 0;
    protected :
        void setHunterState(Hunter* hunter, StateHunter* state){
            hunter->setState(state);
        }
};
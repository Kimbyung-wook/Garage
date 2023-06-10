//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "StateHunter.hpp"

class StateHungry : public StateHunter, public Singleton<StateHungry>{
    public :
        StateHungry();
        void Move(  Hunter* hunter);
        void Eat(   Hunter* hunter);
        void Attack(Hunter* hunter);
        void Idle(  Hunter* hunter);
};
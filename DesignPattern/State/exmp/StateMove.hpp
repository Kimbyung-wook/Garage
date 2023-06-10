//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "StateHunter.hpp"

class StateMove : public StateHunter, public Singleton<StateMove>{
    public :
        StateMove();
        void Move(  Hunter* hunter);
        void Eat(   Hunter* hunter);
        void Attack(Hunter* hunter);
        void Idle(  Hunter* hunter);
};
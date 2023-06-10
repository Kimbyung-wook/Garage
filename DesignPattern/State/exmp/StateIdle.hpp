//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "StateHunter.hpp"

class StateIdle : public StateHunter, public Singleton<StateIdle>{
    public :
        StateIdle();
        void Move(  Hunter* hunter);
        void Eat(   Hunter* hunter);
        void Attack(Hunter* hunter);
        void Idle(  Hunter* hunter);
};
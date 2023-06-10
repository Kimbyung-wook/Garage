//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "StateHunter.hpp"

class StateDead : public StateHunter, public Singleton<StateDead>{
    public :
        StateDead();
        void Move(  Hunter* hunter);
        void Eat(   Hunter* hunter);
        void Attack(Hunter* hunter);
        void Idle(  Hunter* hunter);
};
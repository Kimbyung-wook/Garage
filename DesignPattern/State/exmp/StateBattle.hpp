//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "StateHunter.hpp"

class StateBattle : public StateHunter, public Singleton<StateBattle>{
    public :
        StateBattle();
        void Move(  Hunter* hunter);
        void Eat(   Hunter* hunter);
        void Attack(Hunter* hunter);
        void Idle(  Hunter* hunter);
};
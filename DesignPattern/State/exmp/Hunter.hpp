//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once

class StateHunter;
class Hunter{
    public:
        StateHunter* state;

    public:
        Hunter();
        void setState(StateHunter* state);
        void Move();
        void Eat();
        void Attack();
        void Idle();
};
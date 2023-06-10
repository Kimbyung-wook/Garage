//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "StateHungry.hpp"
#include "StateBattle.hpp"
#include "StateMove.hpp"
#include "StateDead.hpp"
#include "StateIdle.hpp"
#include <cstdio>

StateIdle::StateIdle(){
    sprintf(stateName, "Idle");
}
void StateIdle::Move(  Hunter* hunter){
    printf(" %10s : Hungry.. -> Move\n", stateName);
    setHunterState(hunter, StateMove::getInstance());
}
void StateIdle::Eat(   Hunter* hunter){
    printf(" %10s : On Eating\n", stateName);
}
void StateIdle::Attack(Hunter* hunter){
    printf(" %10s : Killed by a wild -> Dead\n", stateName);
    setHunterState(hunter, StateDead::getInstance());
}
void StateIdle::Idle(  Hunter* hunter){
    printf(" %10s : on Searching something to eat\n", stateName);
}
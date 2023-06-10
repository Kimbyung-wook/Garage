//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "StateHungry.hpp"
#include "StateBattle.hpp"
#include "StateMove.hpp"
#include "StateDead.hpp"
#include "StateIdle.hpp"
#include <cstdio>

StateHungry::StateHungry(){
    sprintf(stateName, "Hungry");
}
void StateHungry::Move(  Hunter* hunter){
    printf(" %10s : Hungry..\n", stateName);
}
void StateHungry::Eat(   Hunter* hunter){
    printf(" %10s : On Eating -> Idle\n", stateName);
    setHunterState(hunter, StateIdle::getInstance());
}
void StateHungry::Attack(Hunter* hunter){
    printf(" %10s : Killed by a wild -> Dead\n", stateName);
    setHunterState(hunter, StateDead::getInstance());
}
void StateHungry::Idle(  Hunter* hunter){
    printf(" %10s : on Searching something to eat\n", stateName);
}
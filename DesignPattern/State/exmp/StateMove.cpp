//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "StateHungry.hpp"
#include "StateBattle.hpp"
#include "StateMove.hpp"
#include "StateDead.hpp"
#include "StateIdle.hpp"
#include <cstdio>

StateMove::StateMove(){
    sprintf(stateName, "Move");
}
void StateMove::Move(  Hunter* hunter){
    printf(" %10s : On Moving\n", stateName);
}
void StateMove::Eat(   Hunter* hunter){
    printf(" %10s : On Eating\n", stateName);
}
void StateMove::Attack(Hunter* hunter){
    printf(" %10s : Attack a wild thing\n", stateName);
    setHunterState(hunter, StateBattle::getInstance());
}
void StateMove::Idle(  Hunter* hunter){
    printf(" %10s : Taking a break\n", stateName);
    setHunterState(hunter, StateIdle::getInstance());
}
//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "StateHungry.hpp"
#include "StateBattle.hpp"
#include "StateMove.hpp"
#include "StateDead.hpp"
#include "StateIdle.hpp"
#include <cstdio>

StateBattle::StateBattle(){
    sprintf(stateName, "Battle");
}
void StateBattle::Move(  Hunter* hunter){
    printf(" %10s : Unavoidable!\n", stateName);
}
void StateBattle::Eat(   Hunter* hunter){
    printf(" %10s : Can't eat!\n", stateName);
}
void StateBattle::Attack(Hunter* hunter){
    printf(" %10s : Get a Win! -> Hungry\n", stateName);
    setHunterState(hunter, StateHungry::getInstance());
}
void StateBattle::Idle(  Hunter* hunter){
    printf(" %10s : Cant' get some rest!\n", stateName);
}
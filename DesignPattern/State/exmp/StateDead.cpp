//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "StateHungry.hpp"
#include "StateBattle.hpp"
#include "StateMove.hpp"
#include "StateDead.hpp"
#include "StateIdle.hpp"
#include <cstdio>

StateDead::StateDead(){
    sprintf(stateName, "Dead");
}
void StateDead::Move(  Hunter* hunter){
    printf(" %10s : Dead!\n", stateName);
}
void StateDead::Eat(   Hunter* hunter){
    printf(" %10s : Dead!\n", stateName);
}
void StateDead::Attack(Hunter* hunter){
    printf(" %10s : Dead!\n", stateName);
}
void StateDead::Idle(  Hunter* hunter){
    printf(" %10s : Dead!\n", stateName);
}
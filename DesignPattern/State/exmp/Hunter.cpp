//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "Hunter.hpp"
#include "StateHunter.hpp"
#include "StateIdle.hpp"

Hunter::Hunter(){
    state = StateIdle::getInstance();
}

void Hunter::setState(StateHunter* state){
    this->state = state;
}

void Hunter::Move(){
    state->Move(this);
}

void Hunter::Eat(){
    state->Eat(this);
}

void Hunter::Attack(){
    state->Attack(this);
}

void Hunter::Idle(){
    state->Idle(this);
}
#include "Hunter.h"
#include "HunterState.h"

Hunter::Hunter()
{
	state = IdleState::getInstance();
}

void Hunter::SetState(HunterState * state)
{
	this->state = state;
}

void Hunter::Move()
{
	state->Move(this);
}

void Hunter::Eat()
{
	state->Eat(this);
}

void Hunter::Attack()
{
	state->Attack(this);
}

void Hunter::Idle()
{
	state->Idle(this);
}
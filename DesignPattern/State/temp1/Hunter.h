#pragma once

class HunterState;
class Hunter
{
	HunterState* state;

public:
	Hunter();

	void SetState(HunterState* state);
	void Move();
	void Eat();
	void Attack();
	void Idle();
};
//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
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
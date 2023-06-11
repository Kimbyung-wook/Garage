//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#pragma once
#include "Hunter.h"
#include "singleton.hpp"

class HunterState
{
public:
	virtual void Move(Hunter* hunter) = 0;
	virtual void Eat(Hunter* hunter) = 0;
	virtual void Attack(Hunter* hunter) = 0;
	virtual void Idle(Hunter* hunter) = 0;

protected:
	void SetHunterState(Hunter* hunter, HunterState* state)
	{
		hunter->SetState(state);
	}
};

class MoveState : public HunterState, public Singleton<MoveState>
{
	virtual void Move(Hunter* hunter);
	virtual void Eat(Hunter* hunter);
	virtual void Attack(Hunter* hunter);
	virtual void Idle(Hunter* hunter);
};

class IdleState : public HunterState, public Singleton<IdleState>
{
	virtual void Move(Hunter* hunter);
	virtual void Eat(Hunter* hunter);
	virtual void Attack(Hunter* hunter);
	virtual void Idle(Hunter* hunter);
};

class BattleState : public HunterState, public Singleton<BattleState>
{
	virtual void Move(Hunter* hunter);
	virtual void Eat(Hunter* hunter);
	virtual void Attack(Hunter* hunter);
	virtual void Idle(Hunter* hunter);
};

class HungryState : public HunterState, public Singleton<HungryState>
{
	virtual void Move(Hunter* hunter);
	virtual void Eat(Hunter* hunter);
	virtual void Attack(Hunter* hunter);
	virtual void Idle(Hunter* hunter);
};

class DeadState : public HunterState, public Singleton<HungryState>
{
	virtual void Move(Hunter* hunter);
	virtual void Eat(Hunter* hunter);
	virtual void Attack(Hunter* hunter);
	virtual void Idle(Hunter* hunter);
};
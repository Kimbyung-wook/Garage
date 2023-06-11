//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "HunterState.h"
#include <iostream>

using namespace std;
void BattleState::Move(Hunter * hunter)
{
	cout << "피할 수가 없다!" << endl;
}

void BattleState::Eat(Hunter * hunter)
{
	cout << "먹을 수가 없다!" << endl;
}

void BattleState::Attack(Hunter * hunter)
{
	cout << "전투에서 이겼다!!" << endl;

	SetHunterState(hunter, HungryState::getInstance());
}

void BattleState::Idle(Hunter * hunter)
{
	cout << "휴식을 취할 수 없다!" << endl;
}

void MoveState::Move(Hunter * hunter)
{
	cout << "걷는중..." << endl;
}

void MoveState::Eat(Hunter * hunter)
{
	cout << "식사중..." << endl;
}

void MoveState::Attack(Hunter * hunter)
{
	cout << "야생 동물 발견! 야생 동물을 공격 한다!!" << endl;

	SetHunterState(hunter, BattleState::getInstance());
}

void MoveState::Idle(Hunter * hunter)
{
	cout << "쉬는중!" << endl;

	SetHunterState(hunter, IdleState::getInstance());
}

void IdleState::Move(Hunter * hunter)
{
	cout << "휴식 끝, 걷는중..." << endl;

	SetHunterState(hunter, MoveState::getInstance());
}

void IdleState::Eat(Hunter * hunter)
{
	cout << "식사중..." << endl;
}

void IdleState::Attack(Hunter * hunter)
{
	cout << "야생 동물 발견! 야생 동물을 공격 한다!!" << endl;

	SetHunterState(hunter, BattleState::getInstance());
}

void IdleState::Idle(Hunter * hunter)
{
	cout << "더 쉬고 싶다..." << endl;
}

void HungryState::Move(Hunter * hunter)
{
	cout << "배가 고프다..." << endl;
}

void HungryState::Eat(Hunter * hunter)
{
	cout << "식사중..." << endl;

	SetHunterState(hunter, IdleState::getInstance());
}

void HungryState::Attack(Hunter * hunter)
{
	cout << "배가 고파 야생 동물에게 죽었다." << endl;

	SetHunterState(hunter, DeadState::getInstance());
}

void HungryState::Idle(Hunter * hunter)
{
	cout << "먹을 걸 찾는중..." << endl;
}

void DeadState::Move(Hunter * hunter)
{
	cout << "사망..." << endl;
}

void DeadState::Eat(Hunter * hunter)
{
	cout << "사망..." << endl;
}

void DeadState::Attack(Hunter * hunter)
{
	cout << "시체가 공격 받고 있다." << endl;
}

void DeadState::Idle(Hunter * hunter)
{
	cout << "사망..." << endl;
}
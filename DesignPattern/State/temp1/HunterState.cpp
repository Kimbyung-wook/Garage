//***************************************************************//
// Originated from https://daru-daru.tistory.com/70
//***************************************************************//
#include "HunterState.h"
#include <iostream>

using namespace std;
void BattleState::Move(Hunter * hunter)
{
	cout << "���� ���� ����!" << endl;
}

void BattleState::Eat(Hunter * hunter)
{
	cout << "���� ���� ����!" << endl;
}

void BattleState::Attack(Hunter * hunter)
{
	cout << "�������� �̰��!!" << endl;

	SetHunterState(hunter, HungryState::getInstance());
}

void BattleState::Idle(Hunter * hunter)
{
	cout << "�޽��� ���� �� ����!" << endl;
}

void MoveState::Move(Hunter * hunter)
{
	cout << "�ȴ���..." << endl;
}

void MoveState::Eat(Hunter * hunter)
{
	cout << "�Ļ���..." << endl;
}

void MoveState::Attack(Hunter * hunter)
{
	cout << "�߻� ���� �߰�! �߻� ������ ���� �Ѵ�!!" << endl;

	SetHunterState(hunter, BattleState::getInstance());
}

void MoveState::Idle(Hunter * hunter)
{
	cout << "������!" << endl;

	SetHunterState(hunter, IdleState::getInstance());
}

void IdleState::Move(Hunter * hunter)
{
	cout << "�޽� ��, �ȴ���..." << endl;

	SetHunterState(hunter, MoveState::getInstance());
}

void IdleState::Eat(Hunter * hunter)
{
	cout << "�Ļ���..." << endl;
}

void IdleState::Attack(Hunter * hunter)
{
	cout << "�߻� ���� �߰�! �߻� ������ ���� �Ѵ�!!" << endl;

	SetHunterState(hunter, BattleState::getInstance());
}

void IdleState::Idle(Hunter * hunter)
{
	cout << "�� ���� �ʹ�..." << endl;
}

void HungryState::Move(Hunter * hunter)
{
	cout << "�谡 ������..." << endl;
}

void HungryState::Eat(Hunter * hunter)
{
	cout << "�Ļ���..." << endl;

	SetHunterState(hunter, IdleState::getInstance());
}

void HungryState::Attack(Hunter * hunter)
{
	cout << "�谡 ���� �߻� �������� �׾���." << endl;

	SetHunterState(hunter, DeadState::getInstance());
}

void HungryState::Idle(Hunter * hunter)
{
	cout << "���� �� ã����..." << endl;
}

void DeadState::Move(Hunter * hunter)
{
	cout << "���..." << endl;
}

void DeadState::Eat(Hunter * hunter)
{
	cout << "���..." << endl;
}

void DeadState::Attack(Hunter * hunter)
{
	cout << "��ü�� ���� �ް� �ִ�." << endl;
}

void DeadState::Idle(Hunter * hunter)
{
	cout << "���..." << endl;
}
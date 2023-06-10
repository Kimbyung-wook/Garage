#include "Hunter.h"

int main()
{
	/* State */
	Hunter* hunter = new Hunter();
	
	hunter->Move();
	hunter->Move();
	hunter->Attack();
	hunter->Move();
	hunter->Attack();
	hunter->Eat();
	hunter->Move();
	hunter->Attack();
	hunter->Attack();
	hunter->Attack();
	hunter->Idle();

	delete hunter;
}
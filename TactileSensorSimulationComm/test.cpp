//
// Created by etienne on 2021-03-15.
//
#include "comm.h"
#include <cstdlib>
#include <unistd.h>

int main(int, char const* [])
{

	int error;
	createPseudoTerminal(&error);

	while (true)
	{
		uint16_t staticData[28];
		for (int i = 0; i < 28; ++i)
		{
			staticData[i] = rand() % 4000;
		}

		sendStaticData(0, staticData);

		sleep(0.001);
		sendStaticData(1, staticData);
		sleep(0.001);
	}

	return 0;
}
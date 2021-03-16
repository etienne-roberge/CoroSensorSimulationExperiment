#include "comm.h"

#include <iostream>
#include <pty.h>
#include <sys/stat.h>
#include <cstring>
#include <unistd.h>
#include <utmp.h>
#include <fcntl.h>      // File control definitions
#include <termios.h>    // POSIX terminal control definitions

extern "C" {
#define PUT_BE2(ptr, data)      \
    do {                        \
        uint8_t *p = (ptr);     \
        uint16_t d = (data);    \
        p[0] = d >> 8;          \
        p[1] = d & 0xFF;        \
    } while (0)

void createPseudoTerminal(int* errorCode)
{
	int master, slave;
	char mode[] = "0777"; //I know this isn't good, it is for testing at the moment
	int access;

	int e = openpty(&master, &slave, &name[0], 0, 0);

	USB = master;

	if (0 > e)
	{
		std::printf("Error: %s\n", strerror(errno));
		*errorCode = -1;
	}

	if (0 != unlockpt(slave))
	{
		perror("Slave Error");
	}

	access = strtol(mode, 0, 8);

	if (0 > chmod(name, access))
	{
		perror("Permission Error");
	}

	std::printf("Slave PTY: %s\n", name);

	if (!openAndConfigurePort(&USB))
	{
		*errorCode = -1;
	}
}

bool openAndConfigurePort(int* USB)
{
	/**** Configure Port ****/
	struct termios tty{};
	memset(&tty, 0, sizeof tty);
	if (tcgetattr((*USB), &tty) != 0)
	{
		std::cout << "Error " << errno << " from tcgetattr: " << strerror(errno) << std::endl;
		return false;
	}

	/* Set Baud Rate */
	cfsetospeed(&tty, (speed_t)B115200);
	cfsetispeed(&tty, (speed_t)B115200);

	/* Setting other Port Stuff */
	cfmakeraw(&tty);

	/* Flush Port, then applies attributes */
	tcflush((*USB), TCIFLUSH);
	if (tcsetattr((*USB), TCSANOW, &tty) != 0)
	{
		std::cout << "Error " << errno << " from tcsetattr" << std::endl;
		return false;
	}
	return true;
}

void sendStaticData(int fingerId, uint16_t* staticData)
{
	static const uint8_t STATIC_DATA = 0x10;

	UsbPacket send{};
	send.command = 0x58;

	int len = 0;
	send.data[len++] = STATIC_DATA | fingerId << 2 | 0;
	for (unsigned int i = 0; i < 28; ++i, len += 2)
	{
		PUT_BE2(&send.data[len], staticData[i]);
	}

	send.data_length = len;

	usbSend(&send);
}

void usbSend(UsbPacket* packet)
{
	auto* p = (uint8_t*)packet;
	int n_written;

	packet->start_byte = 0x9A;
	packet->crc8 = calcCrc8(p + 2, packet->data_length + 2);

	n_written = write(USB, (char*)p, packet->data_length + 4);
}

uint8_t calcCrc8(uint8_t* data, size_t len)
{
	// TODO: calculate CRC8
	return data[-1];
}
}
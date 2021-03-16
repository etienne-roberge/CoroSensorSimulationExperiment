#ifndef TACTILESENSORSIMULCOMM_LIBRARY_H
#define TACTILESENSORSIMULCOMM_LIBRARY_H

#include <cstdint>
#include <cstdio>

extern "C" {
int USB;
char name[1024];

struct UsbPacket
{
	uint8_t start_byte;
	uint8_t crc8;           // over command, data_length and data
	uint8_t command;        // 4 bits of flag (MSB) and 4 bits of command (LSB)
	uint8_t data_length;
	uint8_t data[60];
};

bool openAndConfigurePort(int* USB);
void createPseudoTerminal(int* errorCode);
void usbSend(UsbPacket* packet);
void sendStaticData(int fingerId, uint16_t* staticData);
uint8_t calcCrc8(uint8_t* data, size_t len);

}
#endif //TACTILESENSORSIMULCOMM_LIBRARY_H

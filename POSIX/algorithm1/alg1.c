#include "alg1.h"


/* CRC8 */
char CRC8(char * data, int len)
{
	char crc = 0;
	char g = 0x31;    // g(x)=x^8+x^5+x^4+1 (100110001 = 0x131)
	while (len--) {    // every char in data
		crc ^= *data;    // newInitialChar = oldCRC ^ newChar
		/* CRC of 1 char */
		for (int i = 0; i < 8; i++) {    // every bit in a char
			if (crc & 0x80)    // highest bit is 1
				crc = (crc << 1) ^ g;    // shift and xor
			else    // highest bit is 0
				crc <<= 1;    // just shift
		}
		data++;    // next char
	}
	return crc;
}



#define PACKLEN 6/sizeof(char)    // length of whole (char) packet = header(1 byte) + payload(4 bytes) + CRC(1 byte)

/* add header & CRC to 4-byte payload, forming 1 char packet */
char * packet(char * payload)
{
	int i;    // index
	char * pack = (char *) malloc(sizeof(char) * PACKLEN);    // pointer of current packet
	bzero(pack, PACKLEN);

	/* header (10101010) */
	pack[0] = 0xaa;

	/* payload (32 bits) */
	for (i = 1; i < 5; i++)
		pack[i] = payload[i-1];

	/* CRC-8 */
	pack[5] = CRC8(pack, 5);

	return pack;
}



long getCurrentTimeMillis()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec * 1000 + tv.tv_usec / 1000);
}



/* when current bit is 1, copy arrays for 1 period; when 0, sleep for 1 period */
void modulateRAM(char * pack, int bitTimeMillis)
{
	// arrays to copy
	int arr1[1024*256] = {1};
	int arr2[1024*256] = {1};

	long bitEndTime = getCurrentTimeMillis();

	char currentChar;

	for (int i = 0; i < PACKLEN; i++) {    // every char
		currentChar = pack[i];
		for (int j = 0; j < sizeof(char)*8; j++) {    // every bit
			bitEndTime += bitTimeMillis;
			if (currentChar & 0x80)    // current bit is 1
				while (getCurrentTimeMillis() < bitEndTime) {
					memcpy(arr1, arr2, 1024*256);
					memcpy(arr2, arr1, 1024*256);
				}
			else    // current bit is 0
				sleep(bitTimeMillis / 1000);
			currentChar = currentChar << 1;
		}
	}
}



/*
	input string
	-> fill if not divisible
	-> make packets and modulate
*/
void alg1()
{
	/* ----------------- Input a String shorter than DATAMAX characters ------------------------- */

#define DATAMAX 100
	printf("Input a string:\n");
	char data_char[DATAMAX];    // array of whole secret data (payload in all packets)
	gets(data_char);


	/* -------------------------- Fill with '\0' if Not Divisible ------------------------------ */

	int char_per_pack = 4 / sizeof(char);    // number of payload char in every packet

	int data_char_len;    // number of char of whole data (after filling)

	if (strlen(data_char) % char_per_pack) {    // not divisible
		data_char_len = (strlen(data_char) / char_per_pack + 1) * char_per_pack;
		for (int i = strlen(data_char); i < data_char_len; i++)
			data_char[i] = '\0';    // fill with '\0' at the end of str
	}
	else    // divisible
		data_char_len = strlen(data_char);

	int packnum = data_char_len / char_per_pack;    // number of packets


	/* -------------------------- Make Packets and Modulate --------------------------------- */

	char * payload = data_char;    // pointer of payload (payload only) in current packet
	char * pack = NULL;    // pointer of current packet (need header and CRC)

	for (int n = 0; n < packnum; n++) {
		pack = packet(payload);
		modulateRAM(pack, 500);
		payload = payload + 4;    // next packet
		free(pack);
	}
}

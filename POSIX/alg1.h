#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>


/*
	@brief:
		calculate CRC of data; g(x)=x^8+x^5+x^4+1 (100110001 = 0x131)
	@param:
		data - pointer of data to be calculated
		len - um of char in data
	@return:
		CRC value in char type
*/
char CRC8(char * data, int len);



/*
	@brief:
		add header & CRC to payload, forming 1 char packet
	@param:
		payload - payload (char type, 4 bytes) of 1 packet
	@return:
		pointer of current packet
*/
char * packet(char * payload);



/*
	@brief:
		get current time in millisecond
	@return:
		current time in millisecond
*/
long getCurrentTimeMillis();



/*
	@brief:
		modulate data
		when current bit is 1, copy arrays for 1 period
		when current bit is 0, sleep for 1 period
	@param:
		pack - packet to be modulated
		bitTimeMillis - bit period in millisecond
*/
void modulateRAM(char * pack, int bitTimeMillis);



/*
	@brief:
		fill data_char with '\0' if the number of char is not divisible -> make packets and modulate
	@param:
		data_char - the secret data to be exfiltrated, also payload of all packets
		bitTimeMillis - bit period in millisecond, used in modulateRAM()
*/
void alg1(char * data_char, int bitTimeMillis);





#include <stdio.h>
#define POLYNOMIAL 0xA001;
unsigned int calc_crc(unsigned char *start_of_packet, unsigned char *end_of_packet){

    unsigned int crc;
    unsigned char bit_count;
    unsigned char *char_ptr;
    /* Start at the beginning of the packet */
    char_ptr = start_of_packet; // pointer to the memory location 
    /* Initialize CRC */
    crc = 0xffff;
    
    // for funsies i want to know where the stack memory location is, 
    //since its a local variable, it should in in stack memory and will unravel as the allocated and deallocated in the stack
    printf("Memory location of char_ptr: %p\n", (void *)char_ptr); //%p is hex formatter, and then we cast the chr_ptr to void * 

    /* Loop through the entire packet */
    do
    {
        /* Exclusive-OR the byte with the CRC */
        crc ^= (unsigned int)*char_ptr;
        /* Loop through all 8 data bits */
        bit_count = 0;
        do
        {
            /* If the LSB is 1, shift the CRC and XOR
            the polynomial mask with the CRC */
            if (crc & 0x0001)
            {
                crc >>= 1;
                crc ^= POLYNOMIAL;
            }
            /* If the LSB is 0, shift the CRC only */
            else
            {
                crc >>= 1;
            }
        } while (bit_count++ < 7);
    } while (char_ptr++ < end_of_packet);
    return (crc);
}

unsigned int create_packet(int *array, int array_size) {
    unsigned int packet[array_size];
    for(int i = 0; i < array_size; i++) {
        packet[i] = array[i];
    }
    return packet;
}

int main(int argc, char *argv[]) {
    // Sample packet data
    // unsigned char packet[] = {0x01, 0x06, 0x01, 0x2c, 0x03, 0xe8}; // hard code the packet data
    // unsigned int packet_size = sizeof(packet) / sizeof(packet[0]); // sizeof(packet) / sizeof(packet[0]) = 6 bytes

 
    unsigned char packet[] = {argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]}; // take all args and put them in an array
    
    printf(create_packet([argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]], int 6));

    // Calculate CRC
    // unsigned int crc = calc_crc(packet, packet + packet_size - 1);

    //funsies learning section, I want to know where the memory location of the char pointer is 
    


    // Print the result
    // printf("CRC for the packet is: 0x%X\n", crc);

    return 0;
}

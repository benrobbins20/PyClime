#include <stdio.h>
#include <stdlib.h>

void create_packet(unsigned char *packet, char *argv[], int count) { // since we are passing the address of the packet, we can modify the packet in memory and not have to return it
    for (int i = 0; i < count; i++) {
        unsigned long val = strtoul(argv[i + 1], NULL, 16); // Convert from hex string to number
        if (val > 255) {
            printf("Argument %d is out of range for an unsigned char.\n", i + 1);
            exit(EXIT_FAILURE);
        }
        packet[i] = (unsigned char)val;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 7) {
        printf("Not enough arguments. Please provide 6 numbers.\n");
        return 1;
    }

    unsigned char packet[6] = {0}; // declare a packet array of 6 bytes and initialize all values to 0
    // print packet contents after it is declared, without settings the array to zeros it just has random garbage from last memory write or whatever 
    printf("packet contents: "); // should be list of 0's because we set the array
    for (int i = 0; i < 6; i++) {printf("0x%02x ", packet[i]);}
    printf("\n");
    printf("packet address: %p\n", (void *)packet); // print the address of the packet (stack memory)
    create_packet(packet, argv, argc); // create_packet takes the pointers to the packet array and the argv array, argc is just the count 
    // print packet contents after create_packet()
    printf("packet contents: ");
    for (int i = 0; i < 6; i++) {printf("0x%02x ", packet[i]);} // one-liner loop
    printf("\n");


    return 0;
}

#ifndef SOCKET_T_H__
#define SOCKET_T_H__

enum {
    SYN = 0,
    SYN_ACK = 1,
    DATA = 2,
    ACK = 3,
    FIN = 4,
    FIN_ACK = 5,
    TCP_MAX_DATA_SIZE = PACKET_MAX_PAYLOAD_SIZE - 6
};

typedef struct socket_t {
    uint16_t srcPort;
    uint16_t destPort;
    uint16_t seq;
    nx_uint8_t flag;
    nx_uint8_t window;
    nx_uint8_t data[TCP_MAX_DATA_SIZE];
} TCP_packet_t;

#endif

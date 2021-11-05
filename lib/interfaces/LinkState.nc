#include "../../includes/packet.h"

//Link-state Interface
// interface LinkState {
//     command void start();
//     command void send(pack* msg);
//     command void updateNeighbors(uint32_t* neighbors, uint16_t neighborSize);
//     command void recieve(pack* routePacket);
//     command void printRouteTable();
// }

interface LinkState{
    command void start();
    command void send(pack* msg);
    command void recieve(pack* routing_packet);
    command void updateNeighbors(uint32_t* neighbors, uint16_t numNeighbors);
    command void printRoutingTable();
}
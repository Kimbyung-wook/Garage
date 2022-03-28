#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __linux__
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>

#elif _WIN32
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <winsock2.h>
#include <Windows.h>
#pragma comment (lib, "ws2_32.lib")
#define bzero(addr, len) (memset(addr, 0,len))
#endif

#define BUFFER_SIZE 1024*64
const char *server_ip = "192.168.10.255";
short server_port = 5252;
char buffer[BUFFER_SIZE];

int main(int argc, char *argv[])
{
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2,2), &wsaData) == SOCKET_ERROR)
    {
        WSACleanup();
    }

    // Generate socket
    int udp_for_send = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udp_for_send == INVALID_SOCKET)
    {
        int tmp = WSAGetLastError();
        fprintf(stderr, "ERROR, client - not port provided / WSA Error %d\n", tmp);
        closesocket(udp_for_send);
        WSACleanup();
    }

    int iBroadcast = 1;
    if (setsockopt(udp_for_send, SOL_SOCKET, SO_BROADCAST, (const char *)&iBroadcast, sizeof(iBroadcast)) == SOCKET_ERROR)
    {
        int tmp = WSAGetLastError();
        fprintf(stderr, "ERROR, client - cannot set socket option / WSA Error %d\n", tmp);
        closesocket(udp_for_send);
        WSACleanup();
    }
    // Make message 

    char    ctmp = 61;
    int     itmp = 123456;
    double  dtmp = 37.123456;
    float   ftmp = 126.123456;
    //char copyto[8];
    
    int idx = 0;


    memcpy(&buffer[idx], &ctmp, sizeof(ctmp));
    idx += sizeof(ctmp);
    
    memcpy(&buffer[idx], &itmp, sizeof(itmp));
    idx += sizeof(itmp);

    memcpy(&buffer[idx], &dtmp, sizeof(dtmp));
    idx += sizeof(dtmp);
    
    memcpy(&buffer[idx], &ftmp, sizeof(ftmp));
    idx += sizeof(ftmp);

    buffer[idx] = '\0';

    // Define connection info and send Message
    sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    server_addr.sin_addr.S_un.S_addr = inet_addr(server_ip);
    if (sendto(udp_for_send, buffer, idx, 0, (const struct sockaddr *)&server_addr, sizeof(server_addr)) == SOCKET_ERROR)
    {
        int tmp = WSAGetLastError();
        fprintf(stderr, "ERROR, client - cannot set socket option / WSA Error %d\n", tmp);
        closesocket(udp_for_send);
        WSACleanup();
    }

    closesocket(udp_for_send);
    WSACleanup();
    return 0;
}

//int copy_2_msg(void *dest, char tmp)
//{
//
//}
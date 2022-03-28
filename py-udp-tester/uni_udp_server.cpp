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
#pragma comment (lib, "ws2_32.lib");
#define bzero(addr, len) (memset(addr, 0,len))
#endif

#define BUFFER_SIZE 1024*64

int main(int argc, char *argv[])
{
    WSADATA wsaData;
    if (WSAStartup(0x202, &wsaData) == SOCKET_ERROR)
    {
        WSACleanup();
    }

    // Generate socket
    int udp_to_me = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udp_to_me == INVALID_SOCKET)
    {
        int tmp = WSAGetLastError();
        fprintf(stderr, "ERROR, server - not port provided / WSA Error %d\n", tmp);
        closesocket(udp_to_me);
        WSACleanup();
    }

    // Blocking or Non-blocking
    u_long iMode = 1; // == 0 : blocking, != 0 : Non-blocking
    int iResult = ioctlsocket(udp_to_me, FIONBIO, &iMode);
    if (iResult != NO_ERROR)
    {
        printf("ioctlsocket failed with error : %ld\n", iResult);
    }

    // Define connection info and bind
    const char *server_ip = "192.168.10.61";
    short server_port = 5252;
    sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    server_addr.sin_addr.S_un.S_addr = inet_addr(server_ip);
    if (bind(udp_to_me, (struct sockaddr *) &server_addr, sizeof(server_addr)) == SOCKET_ERROR)
    {
        fprintf(stderr, "ERROR, server - could NOT bind\n");
        closesocket(udp_to_me);
        WSACleanup();
    }

    printf("Server - waiting...\n");
    char types[] = "bidf";
    char buffer[BUFFER_SIZE];
    sockaddr_in udp_client;
    int addr_len;

    while (1)
    {
        addr_len = sizeof(udp_client);
        int received_msg_size = recvfrom(udp_to_me, buffer, BUFFER_SIZE, 0, (sockaddr*) &udp_client, &addr_len);
        if (received_msg_size < 0)
            continue;
        else
        {
            buffer[received_msg_size] = '\0';
            
            // Parse message
            int data_size = 0;
            int order = 0;
            char    ctmp = 0;
            int     itmp = 0;
            float   ftmp = 0;
            double  dtmp = 0;
            for (int idx = 0; idx < received_msg_size;)
            {
                switch (types[order++])
                {
                case 'b': // signed char
                    data_size = sizeof(ctmp);
                    memcpy(&ctmp, &buffer[idx], data_size);
                    idx = idx + data_size;
                    printf("%d ", ctmp);
                    break;
                case 'i':
                    data_size = sizeof(itmp);
                    memcpy(&itmp, &buffer[idx], data_size);
                    idx = idx + data_size;
                    printf("%i ", itmp);
                    break;
                case 'f':
                    data_size = sizeof(ftmp);
                    memcpy(&ftmp, &buffer[idx], data_size);
                    idx = idx + data_size;
                    printf("%f ", ftmp);
                    break;
                case 'd':
                    data_size = sizeof(dtmp);
                    memcpy(&dtmp, &buffer[idx], data_size);
                    idx = idx + data_size;
                    printf("%f ", dtmp);
                    break;
                }
                //if (types[order] == '\0')
                //    break;
            }
            printf("\n");
        }
    }

    closesocket(udp_to_me);
    WSACleanup();
    return 0;

}
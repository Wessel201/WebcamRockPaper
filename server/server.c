#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define MAX 80
#define PORT 5000
#define SA struct sockaddr
   
// Function designed for chat between client and server.
void func(int connfd)
{
    char buff[MAX];
    char *new = malloc(sizeof(char) * MAX);
    int n;
    // infinite loop for chat
    for (;;) {
        bzero(buff, MAX);
        printf("test1\n");
        printf("test1\n");
        new = "test";
        printf("test1\n");
        write(connfd, new, sizeof(new));
        printf("test1\n");
   
        // read the message from client and copy it in buffer
        read(connfd, buff, sizeof(buff));

        // print buffer which contains the client contents
        printf("From client: %s\t To client : ", buff);
        bzero(buff, MAX);
        n = 0;
        // copy server message in the buffer
        while ((buff[n++] = getchar()) != '\n')
            ;

        // and send that buffer to client
        write(connfd, buff, sizeof(buff));
   
        // if msg contains "Exit" then server exit and chat ended.
        if (strncmp("exit", buff, 4) == 0) {
            printf("Server Exit...\n");
            break;
        }
    }
}
   
// Driver function
int main()
{
    int sockfd, connfd, connfd2 , len;
    struct sockaddr_in servaddr, cli;
   
    // socket create and verification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    }
    else
        printf("Socket successfully created..\n");
    bzero(&servaddr, sizeof(servaddr));
   
    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);
   
    // Binding newly created socket to given IP and verification
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
        printf("socket bind failed...\n");
        exit(0);
    }
    else
        printf("Socket successfully binded..\n");
   
    // Now server is ready to listen and verification
    if ((listen(sockfd, 5)) != 0) {
        printf("Listen failed...\n");
        exit(0);
    }
    else
        printf("Server listening..\n");
    len = sizeof(cli);
   
    // Accept the data packet from client and verification
    connfd = accept(sockfd, (SA*)&cli, &len);
    char *welcome = malloc(sizeof(char)* MAX);
    welcome = strcat(welcome, "connected, you are player ");
    if (connfd < 0) {
        printf("server accept failed...\n");
        exit(0);
    }
    else{
        welcome = strcat(welcome, "1\n");
        printf("server accept the client waiting for player 2\n");
        write(connfd, welcome, sizeof(welcome));
    }
    connfd2 = accept(sockfd, (SA*)&cli, &len);
    if (connfd2 < 0) {
        printf("server accept failed...\n");
        exit(0);
    }
    else{
        printf("server accepted player 2 game will start\n");
        welcome = strcat(welcome, "2");
        write(connfd2, welcome, sizeof(welcome));
    }
    // Function for chatting between client and server
    func(connfd);
   
    // After chatting close the socket
    close(sockfd);
}
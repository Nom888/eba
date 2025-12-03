#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>
#include <cmath>
#include <atomic>
#include <pthread.h>

std::atomic<bool> running(true);

void pin_thread_to_core(int core_id) {
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(core_id, &cpuset);

    pthread_t current_thread = pthread_self();
    if (pthread_setaffinity_np(current_thread, sizeof(cpu_set_t), &cpuset) != 0) {
        std::cerr << "Не удалось привязать поток к ядру " << core_id << std::endl;
    }
}

void stress_cpu(int core_id) {
    pin_thread_to_core(core_id);
    
    volatile double result = 0.0;
    while (running) {
        for (int i = 0; i < 1000; ++i) {
            result += std::sqrt(i * 3.14) * std::tan(i);
        }
    }
}

std::string get_cpu_freq(int core_id) {
    std::string path = "/sys/devices/system/cpu/cpu" + std::to_string(core_id) + "/cpufreq/scaling_cur_freq";
    std::ifstream file(path);
    
    if (!file.is_open()) {
        path = "/sys/devices/system/cpu/cpu" + std::to_string(core_id) + "/cpufreq/cpuinfo_cur_freq";
        file.open(path);
        if (!file.is_open()) return "N/A";
    }

    std::string freq_str;
    file >> freq_str;
    
    if (freq_str.empty()) return "0";

    try {
        double mhz = std::stod(freq_str) / 1000.0;
        return std::to_string(mhz) + " MHz";
    } catch (...) {
        return freq_str; 
    }
}

int main() {
    int target_core = 0;

    std::cout << "Запуск стресс-теста на ядре CPU " << target_core << "..." << std::endl;
    std::cout << "Нажмите Ctrl+C для выхода." << std::endl;

    std::thread worker(stress_cpu, target_core);

    while (running) {
        std::string freq = get_cpu_freq(target_core);
        std::cout << "\rЧастота CPU " << target_core << ": " << freq << "      " << std::flush;
        
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    if (worker.joinable()) {
        worker.join();
    }

    return 0;
}

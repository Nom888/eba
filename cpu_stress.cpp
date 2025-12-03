#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>
#include <cmath>
#include <atomic>
#include <pthread.h>
#include <sstream>

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
    // 1. Попытка читать через cpufreq (для реального железа)
    std::string path = "/sys/devices/system/cpu/cpu" + std::to_string(core_id) + "/cpufreq/scaling_cur_freq";
    std::ifstream file(path);
    
    if (!file.is_open()) {
        path = "/sys/devices/system/cpu/cpu" + std::to_string(core_id) + "/cpufreq/cpuinfo_cur_freq";
        file.open(path);
    }

    if (file.is_open()) {
        std::string freq_str;
        file >> freq_str;
        if (!freq_str.empty()) {
            try {
                double mhz = std::stod(freq_str) / 1000.0;
                return std::to_string(mhz) + " MHz (sysfs)";
            } catch (...) {}
        }
        file.close();
    }

    // 2. Запасной вариант: чтение из /proc/cpuinfo (для VM, WSL и старых ядер)
    std::ifstream cpuinfo("/proc/cpuinfo");
    if (cpuinfo.is_open()) {
        std::string line;
        bool core_found = false; 
        // В упрощенном варианте ищем первое упоминание "cpu MHz", 
        // так как в VM частота часто одинакова для всех vCPU.
        while (std::getline(cpuinfo, line)) {
            if (line.find("cpu MHz") != std::string::npos) {
                std::size_t colon_pos = line.find(':');
                if (colon_pos != std::string::npos) {
                    return line.substr(colon_pos + 2) + " MHz (/proc)";
                }
            }
        }
    }

    return "N/A (Drivers missing)";
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

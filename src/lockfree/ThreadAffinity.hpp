#pragma once

#include <cstdint>
#include <iostream>

#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#else
#include <pthread.h>
#include <sched.h>
#endif

namespace lob {

/**
 * @brief Thread affinity utility to pin critical threads to isolated physical CPU cores.
 * 
 * In High-Frequency Trading:
 * Pinning threads to dedicated physical cores prevents:
 * 1. Operating system scheduler context switches.
 * 2. L1/L2 cache evictions caused by thread migration.
 * 3. Cross-core Time Stamp Counter (TSC) drift.
 */
class ThreadAffinity {
public:
    static bool pin_current_thread_to_core(uint32_t core_id) noexcept {
#ifdef _WIN32
        HANDLE thread = GetCurrentThread();
        DWORD_PTR mask = 1ULL << core_id;
        DWORD_PTR result = SetThreadAffinityMask(thread, mask);
        return result != 0;
#else
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(core_id, &cpuset);
        int rc = pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
        return rc == 0;
#endif
    }
};

} // namespace lob

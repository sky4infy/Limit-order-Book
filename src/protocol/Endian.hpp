#pragma once

#include <cstdint>

#ifdef _MSC_VER
#include <intrin.h>
#else
#include <byteswap.h>
#endif

namespace lob {

/**
 * @brief Zero-overhead hardware byte swapping utility for Network Byte Order (Big-Endian).
 * 
 * Exchange protocols like NASDAQ ITCH 5.0 and OUCH 5.0 transmit multi-byte integers
 * in Network Byte Order (Big-Endian). x86_64 CPUs operate in Little-Endian.
 * These functions compile directly to single-cycle hardware instructions:
 * - x86 BSWAP (for 32-bit and 64-bit)
 * - x86 ROR / XCHG (for 16-bit)
 */
class Endian {
public:
    static inline uint16_t bswap16(uint16_t val) noexcept {
#ifdef _MSC_VER
        return _byteswap_ushort(val);
#else
        return __builtin_bswap16(val);
#endif
    }

    static inline uint32_t bswap32(uint32_t val) noexcept {
#ifdef _MSC_VER
        return _byteswap_ulong(val);
#else
        return __builtin_bswap32(val);
#endif
    }

    static inline uint64_t bswap64(uint64_t val) noexcept {
#ifdef _MSC_VER
        return _byteswap_uint64(val);
#else
        return __builtin_bswap64(val);
#endif
    }

    // Host to Network Byte Order (x86 is little endian -> swap to big endian)
    static inline uint16_t host_to_network16(uint16_t val) noexcept { return bswap16(val); }
    static inline uint32_t host_to_network32(uint32_t val) noexcept { return bswap32(val); }
    static inline uint64_t host_to_network64(uint64_t val) noexcept { return bswap64(val); }

    // Network to Host Byte Order (big endian to x86 little endian)
    static inline uint16_t network_to_host16(uint16_t val) noexcept { return bswap16(val); }
    static inline uint32_t network_to_host32(uint32_t val) noexcept { return bswap32(val); }
    static inline uint64_t network_to_host64(uint64_t val) noexcept { return bswap64(val); }
};

} // namespace lob

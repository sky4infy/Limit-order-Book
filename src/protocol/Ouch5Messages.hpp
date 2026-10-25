#pragma once

#include <cstdint>
#include <cstring>
#include "Endian.hpp"

namespace lob {

#pragma pack(push, 1)

/**
 * @brief NASDAQ OUCH 5.0 Enter Order Message ('O').
 * Exact 36-byte wire layout.
 */
struct OuchEnterOrder {
    char     message_type{'O'};           // Offset 0 (1 byte): Always 'O'
    uint64_t order_token{0};              // Offset 1 (8 bytes): Client unique order ID
    char     buy_sell{'B'};               // Offset 9 (1 byte): 'B' = Buy, 'S' = Sell
    uint32_t shares{0};                   // Offset 10 (4 bytes): Order quantity
    char     stock[8]{' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}; // Offset 14 (8 bytes): Symbol
    uint32_t price{0};                    // Offset 22 (4 bytes): Fixed-point 4 decimal places
    uint32_t time_in_force{0};            // Offset 26 (4 bytes): 0 = Day, 99998 = IOC
    char     firm[4]{'F', 'I', 'R', 'M'}; // Offset 30 (4 bytes): Firm identifier
    char     display{'Y'};                // Offset 34 (1 byte): 'Y' = Displayed, 'N' = Non-display
    char     capacity{'A'};               // Offset 35 (1 byte): 'A' = Agency, 'P' = Principal

    void to_network_endian() noexcept {
        order_token    = Endian::host_to_network64(order_token);
        shares         = Endian::host_to_network32(shares);
        price          = Endian::host_to_network32(price);
        time_in_force  = Endian::host_to_network32(time_in_force);
    }

    void to_host_endian() noexcept {
        order_token    = Endian::network_to_host64(order_token);
        shares         = Endian::network_to_host32(shares);
        price          = Endian::network_to_host32(price);
        time_in_force  = Endian::network_to_host32(time_in_force);
    }
};
static_assert(sizeof(OuchEnterOrder) == 36, "OuchEnterOrder must be exactly 36 bytes!");

/**
 * @brief NASDAQ OUCH 5.0 Order Accepted Message ('A').
 * Exact 53-byte wire layout.
 */
struct OuchOrderAccepted {
    char     message_type{'A'};           // Offset 0 (1 byte)
    uint64_t timestamp{0};                // Offset 1 (8 bytes)
    uint64_t order_token{0};              // Offset 9 (8 bytes)
    char     buy_sell{'B'};               // Offset 17 (1 byte)
    uint32_t shares{0};                   // Offset 18 (4 bytes)
    char     stock[8]{' '};               // Offset 22 (8 bytes)
    uint32_t price{0};                    // Offset 30 (4 bytes)
    uint32_t time_in_force{0};            // Offset 34 (4 bytes)
    char     firm[4]{' '};                // Offset 38 (4 bytes)
    char     display{'Y'};                // Offset 42 (1 byte)
    uint64_t order_reference_number{0};   // Offset 43 (8 bytes)
    char     capacity{'A'};               // Offset 51 (1 byte)
    char     order_state{'L'};            // Offset 52 (1 byte)

    void to_network_endian() noexcept {
        timestamp              = Endian::host_to_network64(timestamp);
        order_token            = Endian::host_to_network64(order_token);
        shares                 = Endian::host_to_network32(shares);
        price                  = Endian::host_to_network32(price);
        time_in_force          = Endian::host_to_network32(time_in_force);
        order_reference_number = Endian::host_to_network64(order_reference_number);
    }

    void to_host_endian() noexcept {
        timestamp              = Endian::network_to_host64(timestamp);
        order_token            = Endian::network_to_host64(order_token);
        shares                 = Endian::network_to_host32(shares);
        price                  = Endian::network_to_host32(price);
        time_in_force          = Endian::network_to_host32(time_in_force);
        order_reference_number = Endian::network_to_host64(order_reference_number);
    }
};
static_assert(sizeof(OuchOrderAccepted) == 53, "OuchOrderAccepted must be exactly 53 bytes!");

/**
 * @brief NASDAQ OUCH 5.0 Order Executed Message ('E').
 * Exact 34-byte wire layout.
 */
struct OuchOrderExecuted {
    char     message_type{'E'};
    uint64_t timestamp{0};
    uint64_t order_token{0};
    uint32_t executed_shares{0};
    uint32_t execution_price{0};
    char     liquidity_flag{'A'}; // 'A' = Added, 'R' = Removed
    uint64_t match_number{0};

    void to_network_endian() noexcept {
        timestamp       = Endian::host_to_network64(timestamp);
        order_token     = Endian::host_to_network64(order_token);
        executed_shares = Endian::host_to_network32(executed_shares);
        execution_price = Endian::host_to_network32(execution_price);
        match_number    = Endian::host_to_network64(match_number);
    }

    void to_host_endian() noexcept {
        timestamp       = Endian::network_to_host64(timestamp);
        order_token     = Endian::network_to_host64(order_token);
        executed_shares = Endian::network_to_host32(executed_shares);
        execution_price = Endian::network_to_host32(execution_price);
        match_number    = Endian::network_to_host64(match_number);
    }
};
static_assert(sizeof(OuchOrderExecuted) == 34, "OuchOrderExecuted must be exactly 34 bytes!");

/**
 * @brief NASDAQ OUCH 5.0 Cancel Order Message ('X').
 * Exact 13-byte wire layout.
 */
struct OuchCancelOrder {
    char     message_type{'X'};
    uint64_t order_token{0};
    uint32_t shares{0}; // 0 = cancel all remaining

    void to_network_endian() noexcept {
        order_token = Endian::host_to_network64(order_token);
        shares      = Endian::host_to_network32(shares);
    }

    void to_host_endian() noexcept {
        order_token = Endian::network_to_host64(order_token);
        shares      = Endian::network_to_host32(shares);
    }
};
static_assert(sizeof(OuchCancelOrder) == 13, "OuchCancelOrder must be exactly 13 bytes!");

#pragma pack(pop)

} // namespace lob

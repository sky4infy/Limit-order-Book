#pragma once

#include <cstdint>
#include <cstring>
#include "Endian.hpp"

namespace lob {

#pragma pack(push, 1)

/**
 * @brief NASDAQ ITCH 5.0 48-Bit Timestamp representation.
 * Represents nanoseconds since midnight (0 to 86,400,000,000,000 ns).
 */
struct uint48_t {
    uint8_t bytes[6]{0};

    [[nodiscard]] inline uint64_t to_uint64() const noexcept {
        return (static_cast<uint64_t>(bytes[0]) << 40) |
               (static_cast<uint64_t>(bytes[1]) << 32) |
               (static_cast<uint64_t>(bytes[2]) << 24) |
               (static_cast<uint64_t>(bytes[3]) << 16) |
               (static_cast<uint64_t>(bytes[4]) << 8)  |
               (static_cast<uint64_t>(bytes[5]));
    }

    inline void from_uint64(uint64_t val) noexcept {
        bytes[0] = static_cast<uint8_t>((val >> 40) & 0xFF);
        bytes[1] = static_cast<uint8_t>((val >> 32) & 0xFF);
        bytes[2] = static_cast<uint8_t>((val >> 24) & 0xFF);
        bytes[3] = static_cast<uint8_t>((val >> 16) & 0xFF);
        bytes[4] = static_cast<uint8_t>((val >> 8) & 0xFF);
        bytes[5] = static_cast<uint8_t>(val & 0xFF);
    }
};
static_assert(sizeof(uint48_t) == 6, "uint48_t must be exactly 6 bytes!");

/**
 * @brief NASDAQ ITCH 5.0 System Event Message ('S').
 * Exact 12-byte wire layout.
 */
struct ItchSystemEvent {
    char     message_type{'S'};   // Offset 0 (1 byte)
    uint16_t stock_locate{0};     // Offset 1 (2 bytes)
    uint16_t tracking_number{0};  // Offset 3 (2 bytes)
    uint48_t timestamp;           // Offset 5 (6 bytes)
    char     event_code{'O'};     // Offset 11 (1 byte): 'O' = Start of Messages, 'M' = Market Hours Open

    void to_network_endian() noexcept {
        stock_locate    = Endian::host_to_network16(stock_locate);
        tracking_number = Endian::host_to_network16(tracking_number);
    }

    void to_host_endian() noexcept {
        stock_locate    = Endian::network_to_host16(stock_locate);
        tracking_number = Endian::network_to_host16(tracking_number);
    }
};
static_assert(sizeof(ItchSystemEvent) == 12, "ItchSystemEvent must be exactly 12 bytes!");

/**
 * @brief NASDAQ ITCH 5.0 Add Order Message ('A').
 * Exact 36-byte wire layout.
 */
struct ItchAddOrder {
    char     message_type{'A'};           // Offset 0 (1 byte)
    uint16_t stock_locate{0};             // Offset 1 (2 bytes)
    uint16_t tracking_number{0};          // Offset 3 (2 bytes)
    uint48_t timestamp;                   // Offset 5 (6 bytes)
    uint64_t order_reference_number{0};   // Offset 11 (8 bytes)
    char     buy_sell_indicator{'B'};     // Offset 19 (1 byte): 'B' = Buy, 'S' = Sell
    uint32_t shares{0};                   // Offset 20 (4 bytes)
    char     stock[8]{' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}; // Offset 24 (8 bytes)
    uint32_t price{0};                    // Offset 32 (4 bytes): Fixed-point 4 decimal places

    void to_network_endian() noexcept {
        stock_locate           = Endian::host_to_network16(stock_locate);
        tracking_number        = Endian::host_to_network16(tracking_number);
        order_reference_number = Endian::host_to_network64(order_reference_number);
        shares                 = Endian::host_to_network32(shares);
        price                  = Endian::host_to_network32(price);
    }

    void to_host_endian() noexcept {
        stock_locate           = Endian::network_to_host16(stock_locate);
        tracking_number        = Endian::network_to_host16(tracking_number);
        order_reference_number = Endian::network_to_host64(order_reference_number);
        shares                 = Endian::network_to_host32(shares);
        price                  = Endian::network_to_host32(price);
    }
};
static_assert(sizeof(ItchAddOrder) == 36, "ItchAddOrder must be exactly 36 bytes!");

/**
 * @brief NASDAQ ITCH 5.0 Order Executed Message ('E').
 * Exact 31-byte wire layout.
 */
struct ItchOrderExecuted {
    char     message_type{'E'};           // Offset 0 (1 byte)
    uint16_t stock_locate{0};             // Offset 1 (2 bytes)
    uint16_t tracking_number{0};          // Offset 3 (2 bytes)
    uint48_t timestamp;                   // Offset 5 (6 bytes)
    uint64_t order_reference_number{0};   // Offset 11 (8 bytes)
    uint32_t executed_shares{0};          // Offset 19 (4 bytes)
    uint64_t match_number{0};             // Offset 23 (8 bytes)

    void to_network_endian() noexcept {
        stock_locate           = Endian::host_to_network16(stock_locate);
        tracking_number        = Endian::host_to_network16(tracking_number);
        order_reference_number = Endian::host_to_network64(order_reference_number);
        executed_shares        = Endian::host_to_network32(executed_shares);
        match_number           = Endian::host_to_network64(match_number);
    }

    void to_host_endian() noexcept {
        stock_locate           = Endian::network_to_host16(stock_locate);
        tracking_number        = Endian::network_to_host16(tracking_number);
        order_reference_number = Endian::network_to_host64(order_reference_number);
        executed_shares        = Endian::network_to_host32(executed_shares);
        match_number           = Endian::network_to_host64(match_number);
    }
};
static_assert(sizeof(ItchOrderExecuted) == 31, "ItchOrderExecuted must be exactly 31 bytes!");

/**
 * @brief NASDAQ ITCH 5.0 Order Cancel Message ('X').
 * Exact 23-byte wire layout.
 */
struct ItchOrderCancel {
    char     message_type{'X'};           // Offset 0 (1 byte)
    uint16_t stock_locate{0};             // Offset 1 (2 bytes)
    uint16_t tracking_number{0};          // Offset 3 (2 bytes)
    uint48_t timestamp;                   // Offset 5 (6 bytes)
    uint64_t order_reference_number{0};   // Offset 11 (8 bytes)
    uint32_t canceled_shares{0};          // Offset 19 (4 bytes)

    void to_network_endian() noexcept {
        stock_locate           = Endian::host_to_network16(stock_locate);
        tracking_number        = Endian::host_to_network16(tracking_number);
        order_reference_number = Endian::host_to_network64(order_reference_number);
        canceled_shares        = Endian::host_to_network32(canceled_shares);
    }

    void to_host_endian() noexcept {
        stock_locate           = Endian::network_to_host16(stock_locate);
        tracking_number        = Endian::network_to_host16(tracking_number);
        order_reference_number = Endian::network_to_host64(order_reference_number);
        canceled_shares        = Endian::network_to_host32(canceled_shares);
    }
};
static_assert(sizeof(ItchOrderCancel) == 23, "ItchOrderCancel must be exactly 23 bytes!");

/**
 * @brief NASDAQ ITCH 5.0 Order Delete Message ('D').
 * Exact 19-byte wire layout.
 */
struct ItchOrderDelete {
    char     message_type{'D'};           // Offset 0 (1 byte)
    uint16_t stock_locate{0};             // Offset 1 (2 bytes)
    uint16_t tracking_number{0};          // Offset 3 (2 bytes)
    uint48_t timestamp;                   // Offset 5 (6 bytes)
    uint64_t order_reference_number{0};   // Offset 11 (8 bytes)

    void to_network_endian() noexcept {
        stock_locate           = Endian::host_to_network16(stock_locate);
        tracking_number        = Endian::host_to_network16(tracking_number);
        order_reference_number = Endian::host_to_network64(order_reference_number);
    }

    void to_host_endian() noexcept {
        stock_locate           = Endian::network_to_host16(stock_locate);
        tracking_number        = Endian::network_to_host16(tracking_number);
        order_reference_number = Endian::network_to_host64(order_reference_number);
    }
};
static_assert(sizeof(ItchOrderDelete) == 19, "ItchOrderDelete must be exactly 19 bytes!");

#pragma pack(pop)

} // namespace lob

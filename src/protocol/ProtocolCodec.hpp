#pragma once

#include "Ouch5Messages.hpp"
#include "Itch5Messages.hpp"
#include "../common/Order.hpp"
#include <string_view>
#include <cassert>

namespace lob {

/**
 * @brief Zero-copy Codec for Wall Street Binary Protocols (NASDAQ OUCH 5.0 and ITCH 5.0).
 * 
 * Instead of string allocation or JSON parsing, this codec casts raw byte pointers
 * directly into packed memory structures, converting network endianness in-place
 * with zero heap allocations on the hot path.
 */
class ProtocolCodec {
public:
    /**
     * @brief Zero-copy parse of an inbound raw network buffer into an internal Order.
     * @param buffer Pointer to raw bytes received from network socket.
     * @param bytes_received Number of bytes in buffer.
     * @param out_order Output order populated from packet.
     * @return true if successfully parsed, false if buffer is too small or invalid.
     */
    static inline bool parse_ouch_enter_order(const uint8_t* buffer, size_t bytes_received, Order& out_order) noexcept {
        if (bytes_received < sizeof(OuchEnterOrder)) [[unlikely]] {
            return false;
        }

        const auto* packet = reinterpret_cast<const OuchEnterOrder*>(buffer);
        if (packet->message_type != 'O') [[unlikely]] {
            return false;
        }

        // Fast zero-copy field mapping with network-to-host endianness conversion
        OrderId order_id = Endian::network_to_host64(packet->order_token);
        Side side        = (packet->buy_sell == 'B') ? Side::BUY : Side::SELL;
        Price price      = static_cast<Price>(Endian::network_to_host32(packet->price));
        Quantity qty     = Endian::network_to_host32(packet->shares);

        out_order.order_id = order_id;
        out_order.side = side;
        out_order.price = price;
        out_order.quantity = qty;
        out_order.initial_quantity = qty;
        out_order.timestamp = 0;

        return true;
    }

    /**
     * @brief Zero-copy serialization of a resting limit order into a NASDAQ ITCH 5.0 Add Order packet.
     */
    static inline void serialize_itch_add_order(
        uint8_t* out_buffer,
        uint64_t timestamp_ns,
        const Order& order,
        const char* symbol = "AAPL    ") noexcept 
    {
        auto* packet = reinterpret_cast<ItchAddOrder*>(out_buffer);
        packet->message_type           = 'A';
        packet->stock_locate           = 1;
        packet->tracking_number        = 0;
        packet->timestamp.from_uint64(timestamp_ns);
        packet->order_reference_number = order.order_id;
        packet->buy_sell_indicator     = (order.side == Side::BUY) ? 'B' : 'S';
        packet->shares                 = order.quantity;
        std::memcpy(packet->stock, symbol, 8);
        packet->price                  = static_cast<uint32_t>(order.price);

        // Convert in-place to Network Byte Order (Big-Endian)
        packet->to_network_endian();
    }

    /**
     * @brief Zero-copy serialization of an internal Trade match into a NASDAQ ITCH 5.0 Order Executed packet.
     */
    static inline void serialize_itch_order_executed(
        uint8_t* out_buffer,
        uint64_t timestamp_ns,
        uint64_t order_ref_num,
        uint32_t executed_shares,
        uint64_t match_number) noexcept 
    {
        auto* packet = reinterpret_cast<ItchOrderExecuted*>(out_buffer);
        packet->message_type           = 'E';
        packet->stock_locate           = 1;
        packet->tracking_number        = 0;
        packet->timestamp.from_uint64(timestamp_ns);
        packet->order_reference_number = order_ref_num;
        packet->executed_shares        = executed_shares;
        packet->match_number           = match_number;

        packet->to_network_endian();
    }
};

} // namespace lob

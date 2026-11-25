#include "../src/protocol/Ouch5Messages.hpp"
#include "../src/protocol/Itch5Messages.hpp"
#include "../src/protocol/ProtocolCodec.hpp"
#include <iostream>
#include <cassert>
#include <cstring>

using namespace lob;

void test_struct_packing_sizes() {
    std::cout << "[TEST] Running test_struct_packing_sizes..." << std::endl;

    assert(sizeof(OuchEnterOrder) == 36);
    assert(sizeof(OuchOrderAccepted) == 53);
    assert(sizeof(OuchOrderExecuted) == 34);
    assert(sizeof(OuchCancelOrder) == 13);

    assert(sizeof(ItchSystemEvent) == 12);
    assert(sizeof(ItchAddOrder) == 36);
    assert(sizeof(ItchOrderExecuted) == 31);
    assert(sizeof(ItchOrderCancel) == 23);
    assert(sizeof(ItchOrderDelete) == 19);

    std::cout << "  -> PASSED (All 9 NASDAQ OUCH & ITCH message structs are byte-perfect with #pragma pack(1))" << std::endl;
}

void test_endianness_conversion() {
    std::cout << "[TEST] Running test_endianness_conversion..." << std::endl;

    uint64_t val64 = 0x0123456789ABCDEFULL;
    uint64_t net64 = Endian::host_to_network64(val64);
    uint64_t host64 = Endian::network_to_host64(net64);
    assert(host64 == val64);

    uint32_t val32 = 0x12345678;
    uint32_t net32 = Endian::host_to_network32(val32);
    uint32_t host32 = Endian::network_to_host32(net32);
    assert(host32 == val32);

    uint16_t val16 = 0x1234;
    uint16_t net16 = Endian::host_to_network16(val16);
    uint16_t host16 = Endian::network_to_host16(net16);
    assert(host16 == val16);

    std::cout << "  -> PASSED (Hardware BSWAP round-trip verified for 16, 32, and 64-bit words)" << std::endl;
}

void test_ouch_zero_copy_parsing() {
    std::cout << "[TEST] Running test_ouch_zero_copy_parsing..." << std::endl;

    uint8_t buffer[64];
    std::memset(buffer, 0, sizeof(buffer));

    auto* enter_order = reinterpret_cast<OuchEnterOrder*>(buffer);
    enter_order->message_type = 'O';
    enter_order->order_token = 88888888ULL;
    enter_order->buy_sell = 'B';
    enter_order->shares = 500;
    std::memcpy(enter_order->stock, "NVDA    ", 8);
    enter_order->price = 12550; // $125.50
    enter_order->time_in_force = 0;
    std::memcpy(enter_order->firm, "GOLD", 4);
    enter_order->display = 'Y';
    enter_order->capacity = 'P';

    // Simulate sending over wire (convert to Big-Endian)
    enter_order->to_network_endian();

    // Matching Engine receives buffer from socket
    Order parsed_order;
    bool ok = ProtocolCodec::parse_ouch_enter_order(buffer, sizeof(OuchEnterOrder), parsed_order);
    assert(ok);
    assert(parsed_order.order_id == 88888888ULL);
    assert(parsed_order.side == Side::BUY);
    assert(parsed_order.price == 12550);
    assert(parsed_order.quantity == 500);

    // Test rejection of undersized buffer
    Order dummy;
    assert(!ProtocolCodec::parse_ouch_enter_order(buffer, sizeof(OuchEnterOrder) - 1, dummy));

    std::cout << "  -> PASSED (NASDAQ OUCH 5.0 raw packet deserialized into Order in zero allocations)" << std::endl;
}

void test_itch_zero_copy_serialization() {
    std::cout << "[TEST] Running test_itch_zero_copy_serialization..." << std::endl;

    uint8_t wire_buffer[64];

    Order resting_order(99999ULL, Side::SELL, 15025, 200, 1000);
    ProtocolCodec::serialize_itch_add_order(wire_buffer, 1234567890ULL, resting_order, "AAPL    ");

    // Client receives multicast ITCH UDP packet and inspects
    const auto* itch_add = reinterpret_cast<const ItchAddOrder*>(wire_buffer);
    assert(itch_add->message_type == 'A');
    assert(itch_add->buy_sell_indicator == 'S');
    assert(Endian::network_to_host64(itch_add->order_reference_number) == 99999ULL);
    assert(Endian::network_to_host32(itch_add->shares) == 200);
    assert(Endian::network_to_host32(itch_add->price) == 15025);
    assert(std::memcmp(itch_add->stock, "AAPL    ", 8) == 0);

    std::cout << "  -> PASSED (NASDAQ ITCH 5.0 Add Order serialized directly into network packet)" << std::endl;
}

int main() {
    std::cout << "==========================================================" << std::endl;
    std::cout << "     WEEK 6: NASDAQ OUCH 5.0 & ITCH 5.0 PROTOCOL TESTS    " << std::endl;
    std::cout << "==========================================================" << std::endl;

    test_struct_packing_sizes();
    test_endianness_conversion();
    test_ouch_zero_copy_parsing();
    test_itch_zero_copy_serialization();

    std::cout << "\n[PASS] All Week 6 NASDAQ Protocol Tests Passed!\n" << std::endl;
    return 0;
}

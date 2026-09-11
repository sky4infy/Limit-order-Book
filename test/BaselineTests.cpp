#include "../src/baseline/OrderBookBaseline.hpp"
#include <cassert>
#include <iostream>

using namespace lob;

void test_passive_resting() {
    std::cout << "[TEST] Running test_passive_resting...\n";
    OrderBookBaseline book;

    // Add Buy: 100 shares @ $100.00 (10000 cents)
    auto trades = book.add_order(Order(1, Side::BUY, 10000, 100));
    assert(trades.empty());
    assert(book.get_best_bid() == 10000);
    assert(book.get_best_ask() == std::nullopt);
    assert(book.get_volume_at_price(Side::BUY, 10000) == 100);

    // Add Sell: 50 shares @ $100.50 (10050 cents) -> does not cross spread
    trades = book.add_order(Order(2, Side::SELL, 10050, 50));
    assert(trades.empty());
    assert(book.get_best_bid() == 10000);
    assert(book.get_best_ask() == 10050);
    assert(book.total_orders_count() == 2);

    std::cout << "  -> PASSED!\n";
}

void test_exact_fill() {
    std::cout << "[TEST] Running test_exact_fill...\n";
    OrderBookBaseline book;

    // Resting Ask: 100 shares @ $100.00
    book.add_order(Order(1, Side::SELL, 10000, 100));

    // Incoming Buy: 100 shares @ $100.00 -> exact cross!
    auto trades = book.add_order(Order(2, Side::BUY, 10000, 100));
    assert(trades.size() == 1);
    assert(trades[0].price == 10000);
    assert(trades[0].quantity == 100);
    assert(trades[0].maker_order_id == 1);
    assert(trades[0].taker_order_id == 2);

    // Book should now be completely empty
    assert(book.is_empty());
    assert(book.get_best_bid() == std::nullopt);
    assert(book.get_best_ask() == std::nullopt);

    std::cout << "  -> PASSED!\n";
}

void test_partial_fill() {
    std::cout << "[TEST] Running test_partial_fill...\n";
    OrderBookBaseline book;

    // Resting Ask: 200 shares @ $100.00
    book.add_order(Order(1, Side::SELL, 10000, 200));

    // Incoming Buy: 50 shares @ $100.00
    auto trades = book.add_order(Order(2, Side::BUY, 10000, 50));
    assert(trades.size() == 1);
    assert(trades[0].quantity == 50);

    // Remaining Ask should have 150 shares
    assert(book.get_volume_at_price(Side::SELL, 10000) == 150);
    assert(book.total_orders_count() == 1);

    std::cout << "  -> PASSED!\n";
}

void test_multi_level_price_sweep() {
    std::cout << "[TEST] Running test_multi_level_price_sweep...\n";
    OrderBookBaseline book;

    // Resting Asks across 3 price levels:
    // Level 1: 50 shares @ $100.00
    // Level 2: 100 shares @ $100.05
    // Level 3: 200 shares @ $100.10
    book.add_order(Order(1, Side::SELL, 10000, 50));
    book.add_order(Order(2, Side::SELL, 10005, 100));
    book.add_order(Order(3, Side::SELL, 10010, 200));

    // Aggressive Buyer sweeps with limit price $100.10 and quantity 200 shares
    // Should completely fill Level 1 (50 shares @ $100.00)
    // Should completely fill Level 2 (100 shares @ $100.05)
    // Should partially fill Level 3 (50 shares @ $100.10)
    auto trades = book.add_order(Order(4, Side::BUY, 10010, 200));
    assert(trades.size() == 3);

    assert(trades[0].price == 10000 && trades[0].quantity == 50);
    assert(trades[1].price == 10005 && trades[1].quantity == 100);
    assert(trades[2].price == 10010 && trades[2].quantity == 50);

    // Level 3 should have 150 shares left
    assert(book.get_best_ask() == 10010);
    assert(book.get_volume_at_price(Side::SELL, 10010) == 150);

    std::cout << "  -> PASSED!\n";
}

void test_fifo_time_priority() {
    std::cout << "[TEST] Running test_fifo_time_priority...\n";
    OrderBookBaseline book;

    // Order A arrives first: 100 shares @ $50.00
    // Order B arrives second: 100 shares @ $50.00
    book.add_order(Order(10, Side::BUY, 5000, 100));
    book.add_order(Order(11, Side::BUY, 5000, 100));

    // Incoming Sell arrives for 150 shares
    // Must fill Order A (100 shares) first, then Order B (50 shares)!
    auto trades = book.add_order(Order(12, Side::SELL, 5000, 150));
    assert(trades.size() == 2);
    assert(trades[0].maker_order_id == 10 && trades[0].quantity == 100);
    assert(trades[1].maker_order_id == 11 && trades[1].quantity == 50);

    // Order 11 should have 50 shares remaining
    assert(book.get_volume_at_price(Side::BUY, 5000) == 50);

    std::cout << "  -> PASSED!\n";
}

void test_order_cancellation() {
    std::cout << "[TEST] Running test_order_cancellation...\n";
    OrderBookBaseline book;

    book.add_order(Order(1, Side::BUY, 10000, 100));
    book.add_order(Order(2, Side::BUY, 10000, 200));
    assert(book.get_volume_at_price(Side::BUY, 10000) == 300);

    // Cancel Order 1
    bool ok = book.cancel_order(1);
    assert(ok == true);
    assert(book.get_volume_at_price(Side::BUY, 10000) == 200);

    // Cancel already canceled order should return false
    ok = book.cancel_order(1);
    assert(ok == false);

    // Cancel Order 2 (removes level completely)
    ok = book.cancel_order(2);
    assert(ok == true);
    assert(book.get_best_bid() == std::nullopt);
    assert(book.is_empty());

    std::cout << "  -> PASSED!\n";
}

int main() {
    std::cout << "===============================================\n";
    std::cout << "  WEEK 1: LOB BASELINE CORRECTNESS TEST SUITE  \n";
    std::cout << "===============================================\n";

    test_passive_resting();
    test_exact_fill();
    test_partial_fill();
    test_multi_level_price_sweep();
    test_fifo_time_priority();
    test_order_cancellation();

    std::cout << "\n>>> ALL UNIT TESTS PASSED WITH 100% SUCCESS! <<<\n\n";

    // Demo a sample book print
    OrderBookBaseline demo_book;
    demo_book.add_order(Order(101, Side::BUY, 15000, 500));
    demo_book.add_order(Order(102, Side::BUY, 14995, 1200));
    demo_book.add_order(Order(103, Side::BUY, 14990, 3000));
    demo_book.add_order(Order(201, Side::SELL, 15005, 800));
    demo_book.add_order(Order(202, Side::SELL, 15010, 2500));
    demo_book.add_order(Order(203, Side::SELL, 15015, 5000));
    demo_book.print_book();

    return 0;
}

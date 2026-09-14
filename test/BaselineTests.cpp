#include "../src/baseline/OrderBookBaseline.hpp"
#include <cassert>
#include <iostream>

using namespace lob;

void test_passive_resting() {
    std::cout << "[TEST] Running test_passive_resting...\n";
    OrderBookBaseline book;

    auto trades = book.add_order(Order(1, Side::BUY, 10000, 100));
    assert(trades.empty());
    assert(book.get_best_bid() == 10000);
    assert(book.get_best_ask() == std::nullopt);
    assert(book.get_volume_at_price(Side::BUY, 10000) == 100);

    trades = book.add_order(Order(2, Side::SELL, 10050, 50));
    assert(trades.empty());
    assert(book.get_best_bid() == 10000);
    assert(book.get_best_ask() == 10050);
    assert(book.total_orders_count() == 2);

    std::cout << "  -> PASSED\n";
}

void test_exact_fill() {
    std::cout << "[TEST] Running test_exact_fill...\n";
    OrderBookBaseline book;

    book.add_order(Order(1, Side::SELL, 10000, 100));

    auto trades = book.add_order(Order(2, Side::BUY, 10000, 100));
    assert(trades.size() == 1);
    assert(trades[0].price == 10000);
    assert(trades[0].quantity == 100);
    assert(trades[0].maker_order_id == 1);
    assert(trades[0].taker_order_id == 2);

    assert(book.is_empty());
    assert(book.get_best_bid() == std::nullopt);
    assert(book.get_best_ask() == std::nullopt);

    std::cout << "  -> PASSED\n";
}

void test_partial_fill() {
    std::cout << "[TEST] Running test_partial_fill...\n";
    OrderBookBaseline book;

    book.add_order(Order(1, Side::SELL, 10000, 200));

    auto trades = book.add_order(Order(2, Side::BUY, 10000, 50));
    assert(trades.size() == 1);
    assert(trades[0].quantity == 50);

    assert(book.get_volume_at_price(Side::SELL, 10000) == 150);
    assert(book.total_orders_count() == 1);

    std::cout << "  -> PASSED\n";
}

void test_multi_level_price_sweep() {
    std::cout << "[TEST] Running test_multi_level_price_sweep...\n";
    OrderBookBaseline book;

    book.add_order(Order(1, Side::SELL, 10000, 50));
    book.add_order(Order(2, Side::SELL, 10005, 100));
    book.add_order(Order(3, Side::SELL, 10010, 200));

    auto trades = book.add_order(Order(4, Side::BUY, 10010, 200));
    assert(trades.size() == 3);

    assert(trades[0].price == 10000 && trades[0].quantity == 50);
    assert(trades[1].price == 10005 && trades[1].quantity == 100);
    assert(trades[2].price == 10010 && trades[2].quantity == 50);

    assert(book.get_best_ask() == 10010);
    assert(book.get_volume_at_price(Side::SELL, 10010) == 150);

    std::cout << "  -> PASSED\n";
}

void test_fifo_time_priority() {
    std::cout << "[TEST] Running test_fifo_time_priority...\n";
    OrderBookBaseline book;

    book.add_order(Order(10, Side::BUY, 5000, 100));
    book.add_order(Order(11, Side::BUY, 5000, 100));

    auto trades = book.add_order(Order(12, Side::SELL, 5000, 150));
    assert(trades.size() == 2);
    assert(trades[0].maker_order_id == 10 && trades[0].quantity == 100);
    assert(trades[1].maker_order_id == 11 && trades[1].quantity == 50);

    assert(book.get_volume_at_price(Side::BUY, 5000) == 50);

    std::cout << "  -> PASSED\n";
}

void test_order_cancellation() {
    std::cout << "[TEST] Running test_order_cancellation...\n";
    OrderBookBaseline book;

    book.add_order(Order(1, Side::BUY, 10000, 100));
    book.add_order(Order(2, Side::BUY, 10000, 200));
    assert(book.get_volume_at_price(Side::BUY, 10000) == 300);

    bool ok = book.cancel_order(1);
    assert(ok == true);
    assert(book.get_volume_at_price(Side::BUY, 10000) == 200);

    ok = book.cancel_order(1);
    assert(ok == false);

    ok = book.cancel_order(2);
    assert(ok == true);
    assert(book.get_best_bid() == std::nullopt);
    assert(book.is_empty());

    std::cout << "  -> PASSED\n";
}

void test_order_amendment_fifo_priority() {
    std::cout << "[TEST] Running test_order_amendment_fifo_priority...\n";
    OrderBookBaseline book;

    // Place two buy orders at identical price: Order 1 (100 qty), Order 2 (100 qty)
    book.add_order(Order(1, Side::BUY, 10000, 100));
    book.add_order(Order(2, Side::BUY, 10000, 100));
    assert(book.get_volume_at_price(Side::BUY, 10000) == 200);

    // Case 1: Quantity reduction must RETAIN FIFO priority
    bool modified = book.modify_order(1, 40);
    assert(modified == true);
    assert(book.get_volume_at_price(Side::BUY, 10000) == 140);
    auto ord1 = book.get_order(1);
    assert(ord1.has_value() && ord1->quantity == 40);

    // Incoming sell order for 50 shares
    // Order 1 should fill completely (40 shares) because it maintained queue priority,
    // and Order 2 should fill 10 shares, leaving 90 shares.
    auto trades = book.add_order(Order(10, Side::SELL, 10000, 50));
    assert(trades.size() == 2);
    assert(trades[0].maker_order_id == 1 && trades[0].quantity == 40);
    assert(trades[1].maker_order_id == 2 && trades[1].quantity == 10);
    assert(!book.has_order(1));
    assert(book.has_order(2));
    assert(book.get_volume_at_price(Side::BUY, 10000) == 90);

    // Case 2: Quantity increase must LOSE FIFO priority and move to queue tail
    book.add_order(Order(3, Side::BUY, 10000, 100));
    // Now at price 10000: Order 2 has 90, Order 3 has 100
    // Increasing Order 2 quantity from 90 to 120 pushes it behind Order 3!
    modified = book.modify_order(2, 120);
    assert(modified == true);
    assert(book.get_volume_at_price(Side::BUY, 10000) == 220);

    // Incoming sell order for 100 shares.
    // Order 3 must be matched first (100 shares) since Order 2 lost priority to tail!
    trades = book.add_order(Order(20, Side::SELL, 10000, 100));
    assert(trades.size() == 1);
    assert(trades[0].maker_order_id == 3 && trades[0].quantity == 100);
    assert(!book.has_order(3));
    assert(book.has_order(2));
    assert(book.get_volume_at_price(Side::BUY, 10000) == 120);

    // Case 3: Modifying quantity to 0 cancels the order
    modified = book.modify_order(2, 0);
    assert(modified == true);
    assert(!book.has_order(2));
    assert(book.is_empty());

    // Case 4: Non-existent order returns false
    assert(book.modify_order(999, 100) == false);

    std::cout << "  -> PASSED\n";
}

void test_market_statistics_and_depth() {
    std::cout << "[TEST] Running test_market_statistics_and_depth...\n";
    OrderBookBaseline book;

    // Empty book stats
    assert(book.get_spread() == std::nullopt);
    assert(book.get_mid_price() == std::nullopt);
    assert(book.get_total_volume(Side::BUY) == 0);
    assert(book.get_total_volume(Side::SELL) == 0);

    // Add bids: 10000 (qty 100), 9990 (qty 200), 9980 (qty 300)
    book.add_order(Order(1, Side::BUY, 10000, 100));
    book.add_order(Order(2, Side::BUY, 9990, 120));
    book.add_order(Order(3, Side::BUY, 9990, 80));
    book.add_order(Order(4, Side::BUY, 9980, 300));

    // Add asks: 10050 (qty 150), 10100 (qty 250)
    book.add_order(Order(5, Side::SELL, 10050, 150));
    book.add_order(Order(6, Side::SELL, 10100, 250));

    // Spread & Mid-price
    // Best Bid: 10000 ($100.00), Best Ask: 10050 ($100.50) -> Spread: 50 ($0.50)
    auto spread = book.get_spread();
    assert(spread.has_value() && *spread == 50);

    auto mid = book.get_mid_price();
    assert(mid.has_value() && *mid == 10025.0);

    // Total volumes
    assert(book.get_total_volume(Side::BUY) == 600);
    assert(book.get_total_volume(Side::SELL) == 400);

    // L2 Depth snapshot
    auto buy_depth = book.get_level_depth(Side::BUY, 2);
    assert(buy_depth.size() == 2);
    assert(buy_depth[0].price == 10000 && buy_depth[0].volume == 100 && buy_depth[0].order_count == 1);
    assert(buy_depth[1].price == 9990 && buy_depth[1].volume == 200 && buy_depth[1].order_count == 2);

    auto sell_depth = book.get_level_depth(Side::SELL, 5);
    assert(sell_depth.size() == 2);
    assert(sell_depth[0].price == 10050 && sell_depth[0].volume == 150 && sell_depth[0].order_count == 1);
    assert(sell_depth[1].price == 10100 && sell_depth[1].volume == 250 && sell_depth[1].order_count == 1);

    std::cout << "  -> PASSED\n";
}

int main() {
    std::cout << "===============================================\n";
    std::cout << "       LOB BASELINE CORRECTNESS TESTS          \n";
    std::cout << "===============================================\n";

    test_passive_resting();
    test_exact_fill();
    test_partial_fill();
    test_multi_level_price_sweep();
    test_fifo_time_priority();
    test_order_cancellation();
    test_order_amendment_fifo_priority();
    test_market_statistics_and_depth();

    std::cout << "\nAll unit tests passed successfully.\n\n";

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

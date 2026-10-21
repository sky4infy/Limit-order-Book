#include "../src/optimized/OrderBookOptimized.hpp"
#include <cassert>
#include <iostream>

using namespace lob;

void test_passive_resting() {
    std::cout << "[TEST] Running test_passive_resting...\n";
    OrderBookOptimized book;

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
    OrderBookOptimized book;

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
    OrderBookOptimized book;

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
    OrderBookOptimized book;

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
    OrderBookOptimized book;

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
    OrderBookOptimized book;

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
    OrderBookOptimized book;

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
    OrderBookOptimized book;

    book.add_order(Order(1, Side::BUY, 15000, 500));
    book.add_order(Order(2, Side::BUY, 14995, 1200));
    book.add_order(Order(3, Side::BUY, 14990, 3000));

    book.add_order(Order(4, Side::SELL, 15005, 800));
    book.add_order(Order(5, Side::SELL, 15010, 2500));
    book.add_order(Order(6, Side::SELL, 15015, 5000));

    assert(book.get_best_bid() == 15000);
    assert(book.get_best_ask() == 15005);
    assert(book.get_spread() == 5);
    assert(book.get_mid_price() == 15002.5);

    assert(book.get_total_volume(Side::BUY) == 4700);
    assert(book.get_total_volume(Side::SELL) == 8300);

    auto bid_depth = book.get_level_depth(Side::BUY, 2);
    assert(bid_depth.size() == 2);
    assert(bid_depth[0].price == 15000 && bid_depth[0].volume == 500);
    assert(bid_depth[1].price == 14995 && bid_depth[1].volume == 1200);

    auto ask_depth = book.get_level_depth(Side::SELL, 2);
    assert(ask_depth.size() == 2);
    assert(ask_depth[0].price == 15005 && ask_depth[0].volume == 800);
    assert(ask_depth[1].price == 15010 && ask_depth[1].volume == 2500);

    std::cout << "  -> PASSED\n";

    // Visual demonstration of terminal depth ladder
    book.print_book(3);
}

void test_high_volume_churn() {
    std::cout << "[TEST] Running test_high_volume_churn (50,000 operations)...\n";
    OrderBookOptimized book;

    // Insert 25,000 orders
    for (uint64_t i = 1; i <= 25000; ++i) {
        Price p = 10000 + (i % 50);
        book.add_order(Order(i, Side::BUY, p, 10));
    }
    assert(book.total_orders_count() == 25000);

    // Cancel 10,000 orders
    for (uint64_t i = 1; i <= 10000; ++i) {
        assert(book.cancel_order(i) == true);
    }
    assert(book.total_orders_count() == 15000);

    // Match 15,000 orders with cross (15,000 * 10 = 150,000 shares)
    auto trades = book.add_order(Order(999999, Side::SELL, 10000, 150000));
    assert(!trades.empty());
    assert(book.is_empty());
    assert(book.total_orders_count() == 0);

    std::cout << "  -> PASSED\n";
}

int main() {
    std::cout << "===============================================\n";
    std::cout << "    LOB OPTIMIZED (PHASE 2) CORRECTNESS TESTS   \n";
    std::cout << "===============================================\n";

    test_passive_resting();
    test_exact_fill();
    test_partial_fill();
    test_multi_level_price_sweep();
    test_fifo_time_priority();
    test_order_cancellation();
    test_order_amendment_fifo_priority();
    test_market_statistics_and_depth();
    test_high_volume_churn();

    std::cout << "All Optimized Order Book tests passed successfully.\n\n";
    return 0;
}

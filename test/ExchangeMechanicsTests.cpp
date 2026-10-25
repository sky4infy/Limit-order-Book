#include <cassert>
#include <iostream>
#include <vector>
#include <numeric>
#include "../src/exchange/ExchangeTypes.hpp"
#include "../src/exchange/CallAuction.hpp"
#include "../src/exchange/ProRataMatching.hpp"
#include "../src/exchange/AdvancedOrders.hpp"

using namespace lob;

void test_call_auction_basic_uncrossing() {
    std::cout << "Running test_call_auction_basic_uncrossing...\n";

    CallAuctionEngine auction(100);

    // Book:
    // Buys:
    // 102: 100 qty
    // 101: 200 qty
    // 100: 300 qty
    // Sells:
    // 99:  150 qty
    // 100: 250 qty
    // 101: 200 qty

    auction.add_order(1, 10, Side::BUY, 102, 100, 1000);
    auction.add_order(2, 11, Side::BUY, 101, 200, 1001);
    auction.add_order(3, 12, Side::BUY, 100, 300, 1002);

    auction.add_order(4, 20, Side::SELL, 99, 150, 1003);
    auction.add_order(5, 21, Side::SELL, 100, 250, 1004);
    auction.add_order(6, 22, Side::SELL, 101, 200, 1005);

    // Cumulative at 100:
    // Buys >= 100: 100 + 200 + 300 = 600
    // Sells <= 100: 150 + 250 = 400
    // Matched: min(600, 400) = 400

    // Cumulative at 101:
    // Buys >= 101: 100 + 200 = 300
    // Sells <= 101: 150 + 250 + 200 = 600
    // Matched: min(300, 600) = 300

    // Max volume is 400 at price 100.
    AuctionResult res = auction.calculate_clearing_price();
    assert(res.valid == true);
    assert(res.clearing_price == 100);
    assert(res.matched_volume == 400);
    assert(res.buy_surplus == 200); // 600 - 400
    assert(res.sell_surplus == 0);
    assert(res.imbalance_side == Side::BUY);

    // Now execute cross
    AuctionResult exec_res;
    auto fills = auction.execute_uncross(exec_res);
    assert(exec_res.matched_volume == 400);

    Quantity total_fill_volume = 0;
    for (const auto& f : fills) {
        total_fill_volume += f.quantity;
        assert(f.price == 100); // All fills at clearing price
    }
    assert(total_fill_volume == 400);

    std::cout << "test_call_auction_basic_uncrossing passed!\n";
}

void test_call_auction_market_on_open_and_tie_breaking() {
    std::cout << "Running test_call_auction_market_on_open_and_tie_breaking...\n";

    CallAuctionEngine auction(105); // Reference price 105

    // MOO Buy for 50 shares
    auction.add_order(1, 1, Side::BUY, 0, 50, 1000, true);
    // Limit Buy at 110 for 50 shares
    auction.add_order(2, 2, Side::BUY, 110, 50, 1001, false);

    // MOO Sell for 50 shares
    auction.add_order(3, 3, Side::SELL, 0, 50, 1002, true);
    // Limit Sell at 100 for 50 shares
    auction.add_order(4, 4, Side::SELL, 100, 50, 1003, false);

    // At 100:
    // Buys >= 100: 50 (MOO) + 50 (110) = 100
    // Sells <= 100: 50 (MOO) + 50 (100) = 100
    // Matched = 100, Imbalance = 0

    // At 110:
    // Buys >= 110: 50 (MOO) + 50 (110) = 100
    // Sells <= 110: 50 (MOO) + 50 (100) = 100
    // Matched = 100, Imbalance = 0

    // Tie between 100 and 110. Both have max volume (100) and 0 imbalance.
    // Reference price is 105. Both 100 and 110 are equidistant (5 ticks).
    // Closest chooses first evaluated or closest.
    AuctionResult res = auction.calculate_clearing_price();
    assert(res.valid == true);
    assert(res.matched_volume == 100);
    assert(res.clearing_price == 100 || res.clearing_price == 110);

    std::cout << "test_call_auction_market_on_open_and_tie_breaking passed!\n";
}

void test_pro_rata_matching_and_cme_remainder() {
    std::cout << "Running test_pro_rata_matching_and_cme_remainder...\n";

    // Three resting sell orders at the same price:
    // Order 1: 100 contracts (timestamp 100)
    // Order 2: 200 contracts (timestamp 200)
    // Order 3: 300 contracts (timestamp 300)
    // Total resting depth = 600 contracts.
    // Proportions: 1/6 (16.67%), 2/6 (33.33%), 3/6 (50.00%)

    std::vector<ProRataRestingOrder> resting = {
        {101, 10, 100, 100, 100},
        {102, 20, 200, 200, 200},
        {103, 30, 300, 300, 300}
    };

    // Incoming aggressive buy for 100 contracts
    // Exact shares:
    // Order 1: 100 * (1/6) = 16.6667 -> base 16, remainder 0.6667
    // Order 2: 100 * (2/6) = 33.3333 -> base 33, remainder 0.3333
    // Order 3: 100 * (3/6) = 50.0000 -> base 50, remainder 0.0000
    // Sum of base = 16 + 33 + 50 = 99 contracts.
    // 1 contract remainder!
    // CME rule: largest fractional remainder gets the 1 contract -> Order 1 (0.6667 fraction)!
    // Expected final allocations:
    // Order 1: 17 contracts
    // Order 2: 33 contracts
    // Order 3: 50 contracts
    // Total = 100 contracts!

    auto allocations = ProRataAllocationEngine::allocate_pure_pro_rata(resting, 100);

    assert(allocations.size() == 3);
    assert(allocations[0].allocated_qty == 17);
    assert(allocations[1].allocated_qty == 33);
    assert(allocations[2].allocated_qty == 50);

    Quantity sum_allocated = 0;
    for (const auto& a : allocations) {
        sum_allocated += a.allocated_qty;
    }
    assert(sum_allocated == 100);
    assert(resting[0].remaining_quantity == 83);
    assert(resting[1].remaining_quantity == 167);
    assert(resting[2].remaining_quantity == 250);

    // Test Split FIFO / Pro-Rata
    std::vector<ProRataRestingOrder> resting_split = {
        {201, 10, 100, 100, 100}, // Top of book (earliest timestamp)
        {202, 20, 200, 200, 200},
        {203, 30, 300, 300, 300}
    };

    // 20% FIFO on 100 contracts = 20 contracts guaranteed to Order 201.
    // Remaining 80 contracts allocated pro-rata on remaining balances:
    // Order 201 remaining: 80
    // Order 202 remaining: 200
    // Order 203 remaining: 300
    // Total remaining = 580.
    auto split_alloc = ProRataAllocationEngine::allocate_split_fifo_pro_rata(resting_split, 100, 0.20);
    Quantity split_sum = 0;
    for (const auto& a : split_alloc) {
        split_sum += a.allocated_qty;
    }
    assert(split_sum == 100);
    // Order 201 received at least the 20 FIFO contracts + pro-rata share
    assert(split_alloc[0].allocated_qty >= 20);

    std::cout << "test_pro_rata_matching_and_cme_remainder passed!\n";
}

void test_iceberg_orders_lifecycle() {
    std::cout << "Running test_iceberg_orders_lifecycle...\n";

    AdvancedOrderManager manager;

    // Register Iceberg: total 500 shares, display peak 100 shares
    manager.register_iceberg(1001, 55, Side::BUY, 25000, 500, 100, 1000);
    assert(manager.is_iceberg(1001) == true);

    auto* ice = manager.get_iceberg(1001);
    assert(ice != nullptr);
    assert(ice->current_displayed == 100);
    assert(ice->hidden_remaining == 400);

    // Slice 1: Fill 60 shares
    Quantity new_slice = 0;
    bool replenished = manager.on_slice_fill(1001, 60, 2000, new_slice);
    assert(replenished == false);
    assert(ice->current_displayed == 40);
    assert(ice->hidden_remaining == 400);

    // Fill remaining 40 shares of Slice 1 -> Should replenish Slice 2
    replenished = manager.on_slice_fill(1001, 40, 3000, new_slice);
    assert(replenished == true);
    assert(new_slice == 100);
    assert(ice->current_displayed == 100);
    assert(ice->hidden_remaining == 300);
    assert(ice->current_slice_ts == 3000); // Updated timestamp for queue priority loss

    // Exhaust remaining hidden slices
    manager.on_slice_fill(1001, 100, 4000, new_slice); // Slice 3 (hidden now 200)
    assert(ice->hidden_remaining == 200);

    manager.on_slice_fill(1001, 100, 5000, new_slice); // Slice 4 (hidden now 100)
    assert(ice->hidden_remaining == 100);

    manager.on_slice_fill(1001, 100, 6000, new_slice); // Slice 5 (hidden now 0)
    assert(ice->hidden_remaining == 0);
    assert(ice->current_displayed == 100);

    // Final fill
    replenished = manager.on_slice_fill(1001, 100, 7000, new_slice);
    assert(replenished == false);
    assert(ice->current_displayed == 0);
    assert(ice->active == false);

    std::cout << "test_iceberg_orders_lifecycle passed!\n";
}

void test_self_trade_prevention_policies() {
    std::cout << "Running test_self_trade_prevention_policies...\n";

    Quantity taker_qty = 100;
    Quantity maker_qty = 100;
    bool allowed = false;

    // 1. CANCEL_MAKER
    taker_qty = 100; maker_qty = 60;
    auto action = AdvancedOrderManager::evaluate_stp(StpPolicy::CANCEL_MAKER, 5, 5, taker_qty, maker_qty, allowed);
    assert(allowed == false);
    assert(action == StpAction::MAKER_CANCELLED_CONTINUE);
    assert(maker_qty == 0);
    assert(taker_qty == 100);

    // 2. CANCEL_TAKER
    taker_qty = 100; maker_qty = 60;
    action = AdvancedOrderManager::evaluate_stp(StpPolicy::CANCEL_TAKER, 5, 5, taker_qty, maker_qty, allowed);
    assert(allowed == false);
    assert(action == StpAction::HALT_TAKER_CANCELLED);
    assert(taker_qty == 0);
    assert(maker_qty == 60);

    // 3. CANCEL_BOTH
    taker_qty = 100; maker_qty = 60;
    action = AdvancedOrderManager::evaluate_stp(StpPolicy::CANCEL_BOTH, 5, 5, taker_qty, maker_qty, allowed);
    assert(allowed == false);
    assert(action == StpAction::HALT_TAKER_CANCELLED);
    assert(taker_qty == 0);
    assert(maker_qty == 0);

    // 4. DECREMENT_AND_CANCEL: Taker larger
    taker_qty = 100; maker_qty = 60;
    action = AdvancedOrderManager::evaluate_stp(StpPolicy::DECREMENT_AND_CANCEL, 5, 5, taker_qty, maker_qty, allowed);
    assert(allowed == false);
    assert(action == StpAction::MAKER_CANCELLED_CONTINUE);
    assert(taker_qty == 40);
    assert(maker_qty == 0);

    // 5. DECREMENT_AND_CANCEL: Maker larger
    taker_qty = 60; maker_qty = 100;
    action = AdvancedOrderManager::evaluate_stp(StpPolicy::DECREMENT_AND_CANCEL, 5, 5, taker_qty, maker_qty, allowed);
    assert(allowed == false);
    assert(action == StpAction::HALT_TAKER_CANCELLED);
    assert(taker_qty == 0);
    assert(maker_qty == 40);

    // 6. DECREMENT_AND_CANCEL: Equal size
    taker_qty = 50; maker_qty = 50;
    action = AdvancedOrderManager::evaluate_stp(StpPolicy::DECREMENT_AND_CANCEL, 5, 5, taker_qty, maker_qty, allowed);
    assert(allowed == false);
    assert(action == StpAction::HALT_TAKER_CANCELLED);
    assert(taker_qty == 0);
    assert(maker_qty == 0);

    // 7. Non-matching firms -> Trade proceeds!
    taker_qty = 100; maker_qty = 100;
    action = AdvancedOrderManager::evaluate_stp(StpPolicy::CANCEL_MAKER, 5, 8, taker_qty, maker_qty, allowed);
    assert(allowed == true);
    assert(action == StpAction::CONTINUE_MATCHING);
    assert(taker_qty == 100);
    assert(maker_qty == 100);

    std::cout << "test_self_trade_prevention_policies passed!\n";
}

int main() {
    std::cout << "====================================================\n";
    std::cout << "  WEEK 7: ADVANCED EXCHANGE MECHANICS UNIT TESTS     \n";
    std::cout << "====================================================\n";

    test_call_auction_basic_uncrossing();
    test_call_auction_market_on_open_and_tie_breaking();
    test_pro_rata_matching_and_cme_remainder();
    test_iceberg_orders_lifecycle();
    test_self_trade_prevention_policies();

    std::cout << "\nALL 5 WEEK 7 EXCHANGE MECHANICS TESTS PASSED!\n";
    return 0;
}

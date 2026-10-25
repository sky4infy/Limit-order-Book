#include <cassert>
#include <iostream>
#include <vector>
#include <cmath>
#include "../src/microstructure/MicroPrice.hpp"
#include "../src/microstructure/VpinCalculator.hpp"
#include "../src/microstructure/AvellanedaStoikovBot.hpp"

using namespace lob;

void test_micro_price_queue_imbalance() {
    std::cout << "[TEST] Running test_micro_price_queue_imbalance...\n";

    // 1. Equal queue sizes -> Micro-price equals standard mid-price
    double mp1 = MicroPriceEstimator::calculate_tob_micro_price(100, 500, 102, 500);
    assert(std::abs(mp1 - 101.0) < 1e-6);

    // 2. Heavy Bid queue: 900 on Bid, 100 on Ask -> Price skews 90% towards Ask
    double mp2 = MicroPriceEstimator::calculate_tob_micro_price(100, 900, 101, 100);
    assert(std::abs(mp2 - 100.90) < 1e-6);

    // 3. Heavy Ask queue: 100 on Bid, 900 on Ask -> Price skews 90% towards Bid
    double mp3 = MicroPriceEstimator::calculate_tob_micro_price(100, 100, 101, 900);
    assert(std::abs(mp3 - 100.10) < 1e-6);

    // 4. Multi-Level L2 Depth test
    std::vector<MicroPriceEstimator::Level> bids = {
        {100, 500},
        {99, 1000},
        {98, 2000}
    };
    std::vector<MicroPriceEstimator::Level> asks = {
        {102, 500},
        {103, 1000},
        {104, 2000}
    };
    double ml_mp = MicroPriceEstimator::calculate_multilevel_micro_price(bids, asks, 3);
    assert(std::abs(ml_mp - 101.0) < 1e-3);

    std::cout << "  -> PASSED: Micro-Price queue-imbalance math verified!\n";
}

void test_vpin_toxicity_and_bucket_splitting() {
    std::cout << "[TEST] Running test_vpin_toxicity_and_bucket_splitting...\n";

    // Bucket size = 1,000 contracts, window = 10 buckets
    VpinCalculator vpin(1000, 10);

    // Scenario A: Balanced non-toxic market
    // Alternating 500 Buy and 500 Sell in every bucket
    Price p = 10000;
    for (int i = 0; i < 20; ++i) {
        // Trade 1: Buy (price up)
        p += 1;
        vpin.on_trade(p, 500);
        // Trade 2: Sell (price down)
        p -= 1;
        vpin.on_trade(p, 500);
    }

    double balanced_vpin = vpin.calculate_vpin();
    // In each 1000-contract bucket, buy_volume = 500, sell_volume = 500 -> Imbalance = 0!
    assert(std::abs(balanced_vpin - 0.0) < 1e-5);
    assert(vpin.is_toxic(0.70) == false);

    // Scenario B: Toxic Informed Run
    // Heavy aggressive directional buy flow across 15 buckets
    for (int i = 0; i < 15; ++i) {
        p += 5; // Rising price -> Buy initiated
        vpin.on_trade(p, 1000); // Entire bucket is buy-initiated!
    }

    double toxic_vpin = vpin.calculate_vpin();
    // Rolling window is now full of 100% buy buckets -> VPIN must be 1.0!
    assert(std::abs(toxic_vpin - 1.0) < 1e-5);
    assert(vpin.is_toxic(0.70) == true);

    // Scenario C: Large trade spanning multiple buckets
    vpin.reset();
    p = 20000;
    vpin.on_trade(p + 1, 2500); // 2.5 buckets in a single trade
    assert(vpin.filled_buckets() == 2);

    std::cout << "  -> PASSED: VPIN toxicity metric and volume time partitioning verified!\n";
}

void test_avellaneda_stoikov_inventory_skew() {
    std::cout << "[TEST] Running test_avellaneda_stoikov_inventory_skew...\n";

    double mid_price = 100.0;
    AvellanedaStoikovBot bot(0.1, 2.0, 1.5, 10); // gamma=0.1, sigma=2.0

    // 1. Flat inventory (q = 0)
    auto quotes_flat = bot.compute_optimal_quotes(mid_price);
    assert(std::abs(quotes_flat.reservation_price - 100.0) < 1e-6);
    // Flat quotes should be symmetric around mid-price
    double spread_flat = quotes_flat.ask_price - quotes_flat.bid_price;
    assert(spread_flat > 0);

    // 2. Long inventory (q = +10 contracts)
    bot.on_bid_filled(static_cast<Price>(quotes_flat.bid_price), 10);
    assert(bot.inventory() == 10);

    auto quotes_long = bot.compute_optimal_quotes(mid_price);
    // Reservation price MUST shift downward: R = s - q * gamma * sigma^2 * (T - t)
    // 100 - (10 * 0.1 * 4.0 * 1.0) = 100 - 4 = 96.0!
    assert(std::abs(quotes_long.reservation_price - 96.0) < 1e-6);
    // Both Bid and Ask quotes shift downwards to attract buyers and discourage sellers!
    assert(quotes_long.bid_price < quotes_flat.bid_price);
    assert(quotes_long.ask_price < quotes_flat.ask_price);

    // 3. Sell 20 contracts -> Inventory becomes -10 (Short)
    bot.on_ask_filled(static_cast<Price>(quotes_long.ask_price), 20);
    assert(bot.inventory() == -10);

    auto quotes_short = bot.compute_optimal_quotes(mid_price);
    // 100 - (-10 * 0.1 * 4.0 * 1.0) = 100 + 4 = 104.0!
    assert(std::abs(quotes_short.reservation_price - 104.0) < 1e-6);
    // Both Bid and Ask quotes shift upwards to attract sellers and offload short exposure!
    assert(quotes_short.bid_price > quotes_flat.bid_price);
    assert(quotes_short.ask_price > quotes_flat.ask_price);

    std::cout << "  -> PASSED: Avellaneda-Stoikov reservation price and quote skew verified!\n";
}

int main() {
    std::cout << "==========================================================\n";
    std::cout << "   WEEK 8: MARKET MICROSTRUCTURE & QUANT STRATEGY TESTS   \n";
    std::cout << "==========================================================\n";

    test_micro_price_queue_imbalance();
    test_vpin_toxicity_and_bucket_splitting();
    test_avellaneda_stoikov_inventory_skew();

    std::cout << "\n[PASS] All Week 8 Microstructure & Strategy Tests Passed!\n";
    return 0;
}

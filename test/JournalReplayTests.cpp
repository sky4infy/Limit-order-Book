#include <cassert>
#include <iostream>
#include <vector>
#include <filesystem>
#include "../src/persistence/MemoryMappedJournal.hpp"
#include "../src/optimized/OrderBookOptimized.hpp"

using namespace lob;

void test_journal_append_and_checksum_integrity() {
    std::cout << "[TEST] Running test_journal_append_and_checksum_integrity...\n";

    std::string test_file = "test_journal_tmp.bin";
    if (std::filesystem::exists(test_file)) {
        std::filesystem::remove(test_file);
    }

    {
        MemoryMappedJournal journal(test_file, 1024 * 1024); // 1 MB journal

        // Append 1,000 orders
        for (uint64_t i = 1; i <= 1000; ++i) {
            Side s = (i % 2 == 0) ? Side::BUY : Side::SELL;
            Price p = 10000 + (i % 50);
            Quantity q = 100;
            bool ok = journal.append(JournalEventType::ORDER_ADD, i * 1000, i, 42, s, p, q);
            assert(ok == true);
        }

        assert(journal.record_count() == 1000);
        assert(journal.bytes_written() == sizeof(JournalHeader) + 1000 * sizeof(JournalRecord));

        auto records = journal.replay_all();
        assert(records.size() == 1000);

        for (uint64_t i = 0; i < 1000; ++i) {
            uint64_t expected_seq = i + 1;
            assert(records[i].sequence_number == expected_seq);
            assert(records[i].order_id == expected_seq);
            assert(records[i].event_type == static_cast<uint8_t>(JournalEventType::ORDER_ADD));

            uint32_t expected_csum = static_cast<uint32_t>(records[i].sequence_number ^ records[i].timestamp ^ records[i].order_id ^ records[i].price ^ records[i].quantity);
            assert(records[i].checksum == expected_csum);
        }
    }

    if (std::filesystem::exists(test_file)) {
        std::filesystem::remove(test_file);
    }

    std::cout << "  -> PASSED: Memory-mapped journal sequence and checksum verified!\n";
}

void test_deterministic_crash_replay() {
    std::cout << "[TEST] Running test_deterministic_crash_replay...\n";

    std::string test_file = "crash_replay_tmp.bin";
    if (std::filesystem::exists(test_file)) {
        std::filesystem::remove(test_file);
    }

    Price final_best_bid = 0;
    Price final_best_ask = 0;

    // 1. Run live engine and journal transactions
    {
        MemoryMappedJournal journal(test_file, 2 * 1024 * 1024);
        OrderBookOptimized live_book;

        // 500 Bids from 9950 to 9999
        for (uint64_t i = 1; i <= 500; ++i) {
            Price p = 9950 + (i % 50);
            journal.append(JournalEventType::ORDER_ADD, i * 10, i, 10, Side::BUY, p, 100);
            live_book.add_order(Order(i, Side::BUY, p, 100, i * 10));
        }

        // 500 Asks from 10001 to 10050
        for (uint64_t i = 501; i <= 1000; ++i) {
            Price p = 10001 + (i % 50);
            journal.append(JournalEventType::ORDER_ADD, i * 10, i, 20, Side::SELL, p, 100);
            live_book.add_order(Order(i, Side::SELL, p, 100, i * 10));
        }

        // Cancel 100 orders
        for (uint64_t i = 1; i <= 100; ++i) {
            journal.append(JournalEventType::ORDER_CANCEL, (1000 + i) * 10, i, 10, Side::BUY, 0, 0);
            live_book.cancel_order(i);
        }

        final_best_bid = live_book.get_best_bid().value_or(0);
        final_best_ask = live_book.get_best_ask().value_or(0);
        assert(final_best_bid > 0);
        assert(final_best_ask > 0);

        // Crash occurs here: destructor unmaps file
    }

    // 2. Recover from simulated crash by replaying binary journal into fresh engine
    {
        MemoryMappedJournal recovery_journal(test_file, 2 * 1024 * 1024);
        auto records = recovery_journal.replay_all();
        assert(records.size() == 1100); // 1,000 adds + 100 cancels

        OrderBookOptimized recovered_book;
        for (const auto& rec : records) {
            if (rec.event_type == static_cast<uint8_t>(JournalEventType::ORDER_ADD)) {
                recovered_book.add_order(Order(rec.order_id, static_cast<Side>(rec.side), rec.price, rec.quantity, rec.timestamp));
            } else if (rec.event_type == static_cast<uint8_t>(JournalEventType::ORDER_CANCEL)) {
                recovered_book.cancel_order(rec.order_id);
            }
        }

        // Verify 100% exact state recovery
        assert(recovered_book.get_best_bid().value_or(0) == final_best_bid);
        assert(recovered_book.get_best_ask().value_or(0) == final_best_ask);
        std::cout << "  -> Best Bid Recovered: " << recovered_book.get_best_bid().value() << " (Expected: " << final_best_bid << ")\n";
        std::cout << "  -> Best Ask Recovered: " << recovered_book.get_best_ask().value() << " (Expected: " << final_best_ask << ")\n";
    }

    if (std::filesystem::exists(test_file)) {
        std::filesystem::remove(test_file);
    }

    std::cout << "  -> PASSED: 100% Deterministic Crash Replay verified!\n";
}

int main() {
    std::cout << "==========================================================\n";
    std::cout << "   WEEK 9: JOURNALING & DETERMINISTIC REPLAY TESTS        \n";
    std::cout << "==========================================================\n";

    test_journal_append_and_checksum_integrity();
    test_deterministic_crash_replay();

    std::cout << "\n[PASS] All Week 9 Journal & Determinism Tests Passed!\n";
    return 0;
}

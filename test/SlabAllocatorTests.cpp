#include "../src/optimized/SlabAllocator.hpp"
#include "../src/optimized/FlatOrderIndex.hpp"
#include <iostream>
#include <cassert>
#include <vector>

using namespace lob;

void test_slab_allocator_basic() {
    std::cout << "[TEST] Running test_slab_allocator_basic...\n";

    constexpr size_t TEST_CAP = 1000;
    SlabAllocator<OptimizedOrder, TEST_CAP> slab;

    assert(slab.capacity() == TEST_CAP);
    assert(slab.available() == TEST_CAP);
    assert(slab.size() == 0);
    assert(slab.is_empty());

    // Allocate first index
    uint32_t idx0 = slab.allocate();
    assert(idx0 == 0);
    assert(slab.size() == 1);
    assert(slab.available() == TEST_CAP - 1);

    // Allocate second index
    uint32_t idx1 = slab.allocate();
    assert(idx1 == 1);
    assert(slab.size() == 2);

    // Write data to pool
    slab.get(idx0).order_id = 999;
    slab.get(idx1).order_id = 888;
    assert(slab[idx0].order_id == 999);
    assert(slab[idx1].order_id == 888);

    // Deallocate idx0
    slab.deallocate(idx0);
    assert(slab.size() == 1);

    // Re-allocating should return idx0 (LIFO reuse)
    uint32_t idx_reused = slab.allocate();
    assert(idx_reused == idx0);

    // Exhaust pool
    std::vector<uint32_t> allocated;
    while (!slab.is_full()) {
        allocated.push_back(slab.allocate());
    }
    assert(slab.size() == TEST_CAP);
    assert(slab.allocate() == INVALID_INDEX);

    // Reset pool
    slab.reset();
    assert(slab.size() == 0);
    assert(slab.available() == TEST_CAP);

    std::cout << "  -> PASSED\n";
}

void test_flat_order_index() {
    std::cout << "[TEST] Running test_flat_order_index...\n";

    FlatOrderIndex<1024> index;
    assert(index.is_empty());
    assert(index.size() == 0);

    // Insert keys
    assert(index.insert(1001, 5) == true);
    assert(index.insert(1002, 12) == true);
    assert(index.insert(2005, 99) == true);

    assert(index.size() == 3);
    assert(index.find(1001) == 5);
    assert(index.find(1002) == 12);
    assert(index.find(2005) == 99);
    assert(index.find(9999) == INVALID_INDEX);

    // Erase key
    assert(index.erase(1002) == true);
    assert(index.size() == 2);
    assert(index.find(1002) == INVALID_INDEX);
    assert(index.find(1001) == 5);
    assert(index.find(2005) == 99);

    // Erase non-existent
    assert(index.erase(9999) == false);

    // High density collision test
    for (uint64_t id = 1; id <= 500; ++id) {
        assert(index.insert(id * 1024, static_cast<uint32_t>(id)));
    }
    for (uint64_t id = 1; id <= 500; ++id) {
        assert(index.find(id * 1024) == static_cast<uint32_t>(id));
    }
    for (uint64_t id = 1; id <= 500; ++id) {
        assert(index.erase(id * 1024) == true);
    }
    assert(index.size() == 2);

    std::cout << "  -> PASSED\n";
}

int main() {
    std::cout << "===============================================\n";
    std::cout << "    WEEK 3: SLAB ALLOCATOR & INDEX TESTS       \n";
    std::cout << "===============================================\n";

    test_slab_allocator_basic();
    test_flat_order_index();

    std::cout << "\n[PASS] All Week 3 Slab Allocator & Index Tests Passed!\n\n";
    return 0;
}

cmake_minimum_required(VERSION 3.20)
project(LimitOrderBookHFT VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler Optimization Flags
if(MSVC)
    add_compile_options(/O2 /W4 /EHsc /permissive-)
else()
    add_compile_options(-O3 -Wall -Wextra -Wpedantic -march=native)
endif()

# Include common headers
include_directories(src/common src/baseline)

# Baseline Library
add_library(lob_baseline STATIC
    src/baseline/OrderBookBaseline.cpp
    src/baseline/OrderBookBaseline.hpp
    src/common/Order.hpp
    src/common/Types.hpp
)

# Baseline Unit Tests Executable
add_executable(BaselineTests test/BaselineTests.cpp)
target_link_libraries(BaselineTests PRIVATE lob_baseline)

# Baseline Benchmark Harness Executable
add_executable(BaselineBenchmark benchmark/BaselineBenchmark.cpp)
target_link_libraries(BaselineBenchmark PRIVATE lob_baseline)

# Week 2: Memory Layout and Struct Alignment Tests
add_executable(MemoryLayoutTests test/MemoryLayoutTests.cpp)
target_link_libraries(MemoryLayoutTests PRIVATE lob_baseline)

# Week 2: Cache Locality & Pointer Chasing Micro-Benchmark
add_executable(CacheBenchmark benchmark/CacheBenchmark.cpp)
target_link_libraries(CacheBenchmark PRIVATE lob_baseline)

# Week 3: Phase 2 Zero-Allocation Library
add_library(lob_optimized STATIC
    src/optimized/OrderBookOptimized.cpp
    src/optimized/OrderBookOptimized.hpp
    src/optimized/OptimizedOrder.hpp
    src/optimized/SlabAllocator.hpp
    src/optimized/DirectPriceLadder.hpp
    src/optimized/FlatOrderIndex.hpp
    src/common/Order.hpp
    src/common/Types.hpp
)
target_include_directories(lob_optimized PUBLIC src/common src/optimized)

# Week 3: Slab Allocator & Index Unit Tests
add_executable(SlabAllocatorTests test/SlabAllocatorTests.cpp)
target_link_libraries(SlabAllocatorTests PRIVATE lob_optimized)

# Week 3: Optimized Order Book Functional Tests
add_executable(OptimizedOrderBookTests test/OptimizedOrderBookTests.cpp)
target_link_libraries(OptimizedOrderBookTests PRIVATE lob_optimized)

# Week 3: Side-by-Side Phase 1 vs Phase 2 Comparison Benchmark
add_executable(PhaseComparisonBenchmark benchmark/PhaseComparisonBenchmark.cpp)
target_link_libraries(PhaseComparisonBenchmark PRIVATE lob_baseline lob_optimized)

# Week 4: HDR Histogram Unit Tests
add_executable(HdrHistogramTests test/HdrHistogramTests.cpp)
target_include_directories(HdrHistogramTests PRIVATE src/common)

# Week 4: Coordinated Omission & Open-Loop Benchmark Harness
add_executable(CoordinatedOmissionBenchmark benchmark/CoordinatedOmissionBenchmark.cpp)
target_link_libraries(CoordinatedOmissionBenchmark PRIVATE lob_baseline lob_optimized)

# Week 5: SPSC Ring Buffer & Single-Writer Engine Unit Tests
add_executable(SpscRingBufferTests test/SpscRingBufferTests.cpp)
target_link_libraries(SpscRingBufferTests PRIVATE lob_optimized)
target_include_directories(SpscRingBufferTests PRIVATE src/common src/optimized src/lockfree)

# Week 5: Multi-Threaded Contention vs Single-Writer Benchmark
add_executable(MultiThreadedContentionBenchmark benchmark/MultiThreadedContentionBenchmark.cpp)
target_link_libraries(MultiThreadedContentionBenchmark PRIVATE lob_optimized)
target_include_directories(MultiThreadedContentionBenchmark PRIVATE src/common src/optimized src/lockfree)

# Week 6: NASDAQ OUCH 5.0 & ITCH 5.0 Protocol Unit Tests
add_executable(ProtocolTests test/ProtocolTests.cpp)
target_include_directories(ProtocolTests PRIVATE src/common src/protocol)

# Week 6: JSON/REST vs Zero-Copy Binary Protocol Benchmark
add_executable(ProtocolBenchmark benchmark/ProtocolBenchmark.cpp)
target_include_directories(ProtocolBenchmark PRIVATE src/common src/protocol)

# Week 7: Call Auction, Pro-Rata Matching & Advanced Orders Unit Tests
add_executable(ExchangeMechanicsTests test/ExchangeMechanicsTests.cpp)
target_include_directories(ExchangeMechanicsTests PRIVATE src/common src/exchange)

# Week 7: Walrasian Cross & FIFO vs Pro-Rata Benchmark
add_executable(AuctionBenchmark benchmark/AuctionBenchmark.cpp)
target_include_directories(AuctionBenchmark PRIVATE src/common src/exchange)

# Week 8: Market Microstructure & Algorithmic Strategy Unit Tests
add_executable(MicrostructureTests test/MicrostructureTests.cpp)
target_include_directories(MicrostructureTests PRIVATE src/common src/microstructure)

# Week 8: Micro-Price, VPIN & Avellaneda-Stoikov Benchmark
add_executable(MicrostructureBenchmark benchmark/MicrostructureBenchmark.cpp)
target_include_directories(MicrostructureBenchmark PRIVATE src/common src/microstructure)



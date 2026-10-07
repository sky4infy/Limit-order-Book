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


@echo off
setlocal enabledelayedexpansion

echo ===================================================================
echo   COMPILING LIMIT ORDER BOOK BASELINE (MODERN C++20 / MSVC)
echo ===================================================================

:: Setup MSVC 64-bit environment
if exist "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" > nul 2>&1
) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat" > nul 2>&1
)

if not exist bin mkdir bin

echo [1/30] Compiling Baseline Unit Tests (BaselineTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineTests.exe test\BaselineTests.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [2/30] Running Baseline Unit Tests...
bin\BaselineTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit tests failed!
    exit /b %ERRORLEVEL%
)

echo [3/30] Compiling Baseline Benchmark Harness (BaselineBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineBenchmark.exe benchmark\BaselineBenchmark.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [4/30] Running Baseline Benchmark (100,000 Orders)...
bin\BaselineBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Baseline benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [5/30] Compiling Week 2 Memory Layout Tests (MemoryLayoutTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\MemoryLayoutTests.exe test\MemoryLayoutTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Memory layout test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [6/30] Running Week 2 Memory Layout Tests...
bin\MemoryLayoutTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Memory layout tests failed!
    exit /b %ERRORLEVEL%
)

echo [7/30] Compiling Week 2 Cache Locality Benchmark (CacheBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\CacheBenchmark.exe benchmark\CacheBenchmark.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Cache benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [8/30] Running Week 2 Cache Locality Benchmark (1,000,000 elements)...
bin\CacheBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Cache benchmark execution failed!
    exit /b %ERRORLEVEL%
)

echo [9/30] Compiling Week 3 Slab Allocator Tests (SlabAllocatorTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\SlabAllocatorTests.exe test\SlabAllocatorTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Slab allocator test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [10/30] Running Week 3 Slab Allocator Tests...
bin\SlabAllocatorTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Slab allocator tests failed!
    exit /b %ERRORLEVEL%
)

echo [11/30] Compiling Week 3 Optimized Order Book Tests (OptimizedOrderBookTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\OptimizedOrderBookTests.exe test\OptimizedOrderBookTests.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Optimized order book test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [12/30] Running Week 3 Optimized Order Book Tests...
bin\OptimizedOrderBookTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Optimized order book tests failed!
    exit /b %ERRORLEVEL%
)

echo [13/30] Compiling Week 3 Phase 1 vs Phase 2 Comparison Benchmark (PhaseComparisonBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\PhaseComparisonBenchmark.exe benchmark\PhaseComparisonBenchmark.cpp src\baseline\OrderBookBaseline.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Comparison benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [14/30] Running Week 3 Side-by-Side Comparison Benchmark (100,000 Orders)...
bin\PhaseComparisonBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Comparison benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [15/30] Compiling Week 4 HDR Histogram Tests (HdrHistogramTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\HdrHistogramTests.exe test\HdrHistogramTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] HDR Histogram test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [16/30] Running Week 4 HDR Histogram Tests...
bin\HdrHistogramTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] HDR Histogram tests failed!
    exit /b %ERRORLEVEL%
)

echo [17/30] Compiling Week 4 Coordinated Omission Benchmark (CoordinatedOmissionBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\CoordinatedOmissionBenchmark.exe benchmark\CoordinatedOmissionBenchmark.cpp src\baseline\OrderBookBaseline.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Coordinated Omission benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [18/30] Running Week 4 Coordinated Omission Benchmark...
bin\CoordinatedOmissionBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Coordinated Omission benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [19/30] Compiling Week 5 SPSC Ring Buffer Tests (SpscRingBufferTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\SpscRingBufferTests.exe test\SpscRingBufferTests.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] SPSC Ring Buffer test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [20/30] Running Week 5 SPSC Ring Buffer Tests...
bin\SpscRingBufferTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] SPSC Ring Buffer tests failed!
    exit /b %ERRORLEVEL%
)

echo [21/30] Compiling Week 5 Multi-Threaded Contention Benchmark (MultiThreadedContentionBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\MultiThreadedContentionBenchmark.exe benchmark\MultiThreadedContentionBenchmark.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Multi-Threaded Contention benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [22/30] Running Week 5 Multi-Threaded Contention Benchmark...
bin\MultiThreadedContentionBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Multi-Threaded Contention benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [23/30] Compiling Week 6 NASDAQ Protocol Tests (ProtocolTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\ProtocolTests.exe test\ProtocolTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Protocol test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [24/30] Running Week 6 NASDAQ Protocol Tests...
bin\ProtocolTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Protocol tests failed!
    exit /b %ERRORLEVEL%
)

echo [25/30] Compiling Week 6 JSON vs Zero-Copy OUCH Protocol Benchmark (ProtocolBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\ProtocolBenchmark.exe benchmark\ProtocolBenchmark.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Protocol benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [26/30] Running Week 6 JSON vs Zero-Copy OUCH Protocol Benchmark...
bin\ProtocolBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Protocol benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [27/30] Compiling Week 7 Exchange Mechanics Tests (ExchangeMechanicsTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\ExchangeMechanicsTests.exe test\ExchangeMechanicsTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Exchange Mechanics test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [28/30] Running Week 7 Exchange Mechanics Tests...
bin\ExchangeMechanicsTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Exchange Mechanics tests failed!
    exit /b %ERRORLEVEL%
)

echo [29/30] Compiling Week 7 Walrasian Cross ^& FIFO vs Pro-Rata Benchmark (AuctionBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\AuctionBenchmark.exe benchmark\AuctionBenchmark.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Auction benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [30/30] Running Week 7 Walrasian Cross ^& FIFO vs Pro-Rata Benchmark...
bin\AuctionBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Auction benchmark failed!
    exit /b %ERRORLEVEL%
)

echo ===================================================================
echo   WEEK 1, 2, 3, 4, 5, 6 ^& 7 ALL VERIFIED (30/30 STEPS PASSED)!
echo ===================================================================





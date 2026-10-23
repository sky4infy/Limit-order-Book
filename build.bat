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

echo [1/14] Compiling Baseline Unit Tests (BaselineTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineTests.exe test\BaselineTests.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [2/14] Running Baseline Unit Tests...
bin\BaselineTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit tests failed!
    exit /b %ERRORLEVEL%
)

echo [3/14] Compiling Baseline Benchmark Harness (BaselineBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineBenchmark.exe benchmark\BaselineBenchmark.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [4/14] Running Baseline Benchmark (100,000 Orders)...
bin\BaselineBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Baseline benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [5/14] Compiling Week 2 Memory Layout Tests (MemoryLayoutTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\MemoryLayoutTests.exe test\MemoryLayoutTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Memory layout test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [6/14] Running Week 2 Memory Layout Tests...
bin\MemoryLayoutTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Memory layout tests failed!
    exit /b %ERRORLEVEL%
)

echo [7/14] Compiling Week 2 Cache Locality Benchmark (CacheBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\CacheBenchmark.exe benchmark\CacheBenchmark.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Cache benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [8/14] Running Week 2 Cache Locality Benchmark (1,000,000 elements)...
bin\CacheBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Cache benchmark execution failed!
    exit /b %ERRORLEVEL%
)

echo [9/14] Compiling Week 3 Slab Allocator Tests (SlabAllocatorTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\SlabAllocatorTests.exe test\SlabAllocatorTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Slab allocator test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [10/14] Running Week 3 Slab Allocator Tests...
bin\SlabAllocatorTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Slab allocator tests failed!
    exit /b %ERRORLEVEL%
)

echo [11/14] Compiling Week 3 Optimized Order Book Tests (OptimizedOrderBookTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\OptimizedOrderBookTests.exe test\OptimizedOrderBookTests.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Optimized order book test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [12/14] Running Week 3 Optimized Order Book Tests...
bin\OptimizedOrderBookTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Optimized order book tests failed!
    exit /b %ERRORLEVEL%
)

echo [13/14] Compiling Week 3 Phase 1 vs Phase 2 Comparison Benchmark (PhaseComparisonBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\PhaseComparisonBenchmark.exe benchmark\PhaseComparisonBenchmark.cpp src\baseline\OrderBookBaseline.cpp src\optimized\OrderBookOptimized.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Comparison benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [14/14] Running Week 3 Side-by-Side Comparison Benchmark (100,000 Orders)...
bin\PhaseComparisonBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Comparison benchmark failed!
    exit /b %ERRORLEVEL%
)

echo ===================================================================
echo   WEEK 1, WEEK 2 ^& WEEK 3 COMPLETE SUITE VERIFIED! ALL SYSTEMS NOMINAL.
echo ===================================================================




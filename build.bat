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

echo [1/6] Compiling Baseline Unit Tests (BaselineTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineTests.exe test\BaselineTests.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [2/6] Running Baseline Unit Tests...
bin\BaselineTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit tests failed!
    exit /b %ERRORLEVEL%
)

echo [3/8] Compiling Baseline Benchmark Harness (BaselineBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineBenchmark.exe benchmark\BaselineBenchmark.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [4/8] Running Baseline Benchmark (100,000 Orders)...
bin\BaselineBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Baseline benchmark failed!
    exit /b %ERRORLEVEL%
)

echo [5/8] Compiling Week 2 Memory Layout Tests (MemoryLayoutTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\MemoryLayoutTests.exe test\MemoryLayoutTests.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Memory layout test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [6/8] Running Week 2 Memory Layout Tests...
bin\MemoryLayoutTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Memory layout tests failed!
    exit /b %ERRORLEVEL%
)

echo [7/8] Compiling Week 2 Cache Locality Benchmark (CacheBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\CacheBenchmark.exe benchmark\CacheBenchmark.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Cache benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [8/8] Running Week 2 Cache Locality Benchmark (1,000,000 elements)...
bin\CacheBenchmark.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Cache benchmark execution failed!
    exit /b %ERRORLEVEL%
)

echo ===================================================================
echo   WEEK 1 ^& WEEK 2 COMPLETE SUITE VERIFIED! ALL SYSTEMS NOMINAL.
echo ===================================================================




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

echo [1/4] Compiling Unit Tests (BaselineTests.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineTests.exe test\BaselineTests.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit test compilation failed!
    exit /b %ERRORLEVEL%
)

echo [2/4] Running Unit Tests...
bin\BaselineTests.exe
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Unit tests failed!
    exit /b %ERRORLEVEL%
)

echo [3/4] Compiling Benchmark Harness (BaselineBenchmark.exe)...
cl /nologo /std:c++20 /O2 /EHsc /W4 /Fe:bin\BaselineBenchmark.exe benchmark\BaselineBenchmark.cpp src\baseline\OrderBookBaseline.cpp
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Benchmark compilation failed!
    exit /b %ERRORLEVEL%
)

echo [4/4] Running Benchmark (100,000 Orders)...
bin\BaselineBenchmark.exe

echo ===================================================================
echo   BASELINE BUILD AND VERIFICATION COMPLETE!
echo ===================================================================

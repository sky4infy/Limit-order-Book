# Week 6: Wall Street Binary Protocols (NASDAQ OUCH 5.0 & ITCH 5.0)
## Zero-Copy Deserialization, Hardware Endianness Swapping, and Sub-15ns Wire Processing

---

## 1. Executive Summary: Why Financial Exchanges Ban JSON & REST

In web applications and enterprise software, JSON over HTTP/REST is ubiquitous. However, in tier-1 electronic trading venues (NASDAQ, CME, ICE, Eurex, BATS):
$$\textbf{JSON, XML, and REST are strictly forbidden on the critical matching path.}$$

### The Three Deadly Sins of JSON in Ultra-Low Latency:
1. **Character Scanning Overhead**: Parsing `{"price": 100.25}` requires sequentially scanning byte-by-byte looking for quotes, colons, and delimiters, stalling CPU branch prediction.
2. **ASCII-to-Binary Conversion Overhead**: Converting ASCII strings like `"100.25"` to fixed-point integer cents requires repeated multiplications and divisions ($O(K)$ CPU cycles per number).
3. **Dynamic Memory Allocation & Garbage Collection**: Web JSON parsers allocate temporary string buffers and object maps, polluting CPU L1/L2 caches and invoking kernel heap locks.

### The Wall Street Solution: Packed Binary Protocols
Instead of human-readable text, exchanges define fixed-offset, packed binary structs:
- A 64-bit client order token takes exactly **8 raw bytes**.
- A fixed-point price takes exactly **4 raw bytes**.
- Zero parsing, zero allocations, zero string scanning. The network packet pointer is cast directly into a C++ struct via **Zero-Copy Deserialization** in **$12\text{ nanoseconds}$**!

```
       WEB API / REST (Text Inefficient)                     WALL STREET BINARY PROTOCOL (Zero-Copy)
┌──────────────────────────────────────────────┐     ┌──────────────────────────────────────────────┐
│ '{"order_id":888,"price":125.5,"qty":500}'   │     │ 0x4F | 0x0000000000000378 | 0x000001F4 | ... │
│ • Character scanning & string allocations    │ ──► │ • Packed struct: #pragma pack(push, 1)       │
│ • ASCII-to-float math conversion             │     │ • Direct pointer cast: reinterpret_cast      │
│ • 108ns median latency (Burns CPU cache!)    │     │ • 12ns median latency (Single-cycle BSWAP!)  │
└──────────────────────────────────────────────┘     └──────────────────────────────────────────────┘
```

---

## 2. Inbound Order Entry: NASDAQ OUCH 5.0

Located in: [src/protocol/Ouch5Messages.hpp](file:///d:/Limit%20Order%20Book/src/protocol/Ouch5Messages.hpp)

NASDAQ OUCH is the high-speed binary protocol used by trading firms (Citadel, Optiver, Jane Street, HRT) to submit orders directly to NASDAQ's matching engine.

### Key OUCH 5.0 Wire Structures:
- **`OuchEnterOrder` ('O') — Exactly 36 Bytes**:
  - `message_type`: 1 byte (`'O'`)
  - `order_token`: 8 bytes (client unique identifier)
  - `buy_sell`: 1 byte (`'B'` = Buy, `'S'` = Sell)
  - `shares`: 4 bytes (quantity)
  - `stock`: 8 bytes (symbol, e.g. `"AAPL    "`)
  - `price`: 4 bytes (fixed-point 4 decimal places)
  - `time_in_force`: 4 bytes
  - `firm`: 4 bytes
  - `display`: 1 byte (`'Y'` = Displayed, `'N'` = Non-display)
  - `capacity`: 1 byte (`'A'` = Agency, `'P'` = Principal)
- **`OuchOrderAccepted` ('A') — Exactly 53 Bytes**: Sent by exchange to confirm live order placement.
- **`OuchOrderExecuted` ('E') — Exactly 34 Bytes**: Sent by exchange upon trade fill.
- **`OuchCancelOrder` ('X') — Exactly 13 Bytes**: Sent by client to cancel resting shares.

---

## 3. Outbound Market Data: NASDAQ TotalView-ITCH 5.0

Located in: [src/protocol/Itch5Messages.hpp](file:///d:/Limit%20Order%20Book/src/protocol/Itch5Messages.hpp)

NASDAQ ITCH is the direct UDP multicast feed broadcasting every event on the exchange book. Unlike Level 2 (BBO summary), ITCH provides **Level 3 full order book depth**—every single order insertion, fill, and cancel is broadcast to the entire market.

### The 48-Bit Timestamp Architecture:
NASDAQ ITCH uses a custom **6-byte (48-bit) integer** representing nanoseconds since midnight ($0\text{ to }86,400,000,000,000\text{ ns}$):
```cpp
struct uint48_t {
    uint8_t bytes[6]{0};
    uint64_t to_uint64() const noexcept;
    void from_uint64(uint64_t val) noexcept;
};
static_assert(sizeof(uint48_t) == 6, "Must be exactly 6 bytes!");
```

### Key ITCH 5.0 Wire Structures:
- **`ItchAddOrder` ('A') — Exactly 36 Bytes**: Broadcasts new resting order.
- **`ItchOrderExecuted` ('E') — Exactly 31 Bytes**: Broadcasts trade execution.
- **`ItchOrderCancel` ('X') — Exactly 23 Bytes**: Broadcasts partial cancel.
- **`ItchOrderDelete` ('D') — Exactly 19 Bytes**: Broadcasts complete order deletion.
- **`ItchSystemEvent` ('S') — Exactly 12 Bytes**: Market state ('O' = Start of Day, 'M' = Market Open).

---

## 4. Hardware Byte Swapping: Endianness Physics

Located in: [src/protocol/Endian.hpp](file:///d:/Limit%20Order%20Book/src/protocol/Endian.hpp)

Exchange protocols transmit all multi-byte integers in **Network Byte Order (Big-Endian)**. However, modern x86_64 CPUs operate in **Little-Endian**.
We utilize hardware byte swap compiler intrinsics:
- On MSVC: `_byteswap_uint64()`, `_byteswap_ulong()`, `_byteswap_ushort()`.
- On GCC/Clang: `__builtin_bswap64()`, `__builtin_bswap32()`, `__builtin_bswap16()`.

These intrinsics compile directly to the single-cycle x86 **`BSWAP`** instruction, executing in a single clock cycle ($0.25\text{ ns}$) with zero memory traffic.

---

## 5. Empirical Benchmark Results: JSON vs Zero-Copy OUCH 5.0

From our protocol benchmark harness [benchmark/ProtocolBenchmark.cpp](file:///d:/Limit%20Order%20Book/benchmark/ProtocolBenchmark.cpp) parsing **100,000 messages**:

| Metric | JSON Text Parser (Web API) | Zero-Copy OUCH 5.0 (Wall Street) | Speedup / Gain |
| :--- | :--- | :--- | :--- |
| **Messages Processed** | 100,000 | 100,000 | 100% Match Parity |
| **Parse Wall Time** | 15.7 ms | **3.9 ms** | **74% FASTER** |
| **Parsing Throughput** | 6.36M msg/sec | **25.44M msg/sec** | **4.0x FASTER** |
| **p50 (Median) Parsing Latency** | 108 ns | **12 ns** | **88% LOWER** |
| **p90 Parsing Latency** | 193 ns | **13 ns** | **93% LOWER** |
| **p99 Parsing Latency** | 262 ns | **14 ns** | **94% LOWER** |
| **p99.9 (Tail) Parsing Latency** | 907 ns | **14 ns** | **98% LOWER** |
| **Max Outlier** | 99,618 ns | **65,583 ns** | **34% LOWER** |

### Critical Takeaways:
1. **Sub-15ns Determinism**: Zero-copy binary parsing drops median latency from $108\text{ ns}$ down to **$12\text{ ns}$**, and tail latency (p99.9) from $907\text{ ns}$ down to **$14\text{ ns}$**.
2. **Predictable Wire-to-Core Flow**: Because no heap allocations occur, binary protocol handling eliminates memory fragmentation and keeps the CPU execution pipeline completely unhindered.

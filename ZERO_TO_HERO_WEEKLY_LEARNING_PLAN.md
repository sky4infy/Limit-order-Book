# Zero-to-Hero Weekly Learning & Implementation Plan
## Mastering Low-Latency Systems, Financial Markets, and High-Frequency Trading Architecture
**Designed for Beginners: Taking You from Absolute Zero to Institutional-Grade Engineering**

---

## 1. Welcome to the Journey: The Ground-Zero Mindset

Starting with **zero prior knowledge** is not a disadvantage—it is actually an **advantage**. 

You do not have bad habits to unlearn. Many programmers learn high-level web abstractions and assume memory is free and threads are magically fast. In low-latency systems and electronic trading, you will learn to think with **Mechanical Sympathy**—understanding how the CPU, cache lines, memory controllers, and the operating system actually execute your code.

### The Two Core Pillars You Will Master:
1. **Financial Market Mechanics:** How orders, buyers, sellers, prices, queues, and exchanges actually operate.
2. **Computer Systems & Architecture:** How CPUs fetch instructions, why memory access is slow, how cache hierarchies work, and why lock-free programming enables sub-microsecond execution.

---

## 2. Choosing Your Language: Modern C++ vs. Low-Latency Java

| Dimension | Modern C++ (C++20) — Recommended | Low-Latency Java (Java 21 + Agrona) |
| :--- | :--- | :--- |
| **Industry Usage** | Pure HFT, Prop Trading (Citadel, Jane Street, Optiver, HRT, Jump). | Tier-1 Investment Banks (Goldman Sachs Core Strats, Morgan Stanley). |
| **Memory Control** | Explicit memory layout, zero garbage collection, pointers, custom allocators. | Managed heap, but uses off-heap direct memory (`Unsafe`/`Agrona`) to bypass GC. |
| **Learning Curve** | Steeper initial syntax, but gives the purest mental model of hardware. | Easier syntax, but requires advanced tricks to prevent JVM GC pauses. |
| **Verdict** | **Choose C++** if your goal is prop trading / HFT. | **Choose Java** if your primary target is Goldman Sachs Core Strats. |

*Note: This curriculum is designed so you can complete it in either C++20 or Java.*

---

## 3. The 10-Week Zero-to-Hero Curriculum

```
+-----------------------------------------------------------------------------------------------------+
| WEEKS 1-2: FOUNDATIONS                                                                              |
| - Week 1: Market Mechanics & Basic Order Matching (The "Paper Exchange")                            |
| - Week 2: Computer Architecture & The "Mechanical Sympathy" Epiphany                                |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| WEEKS 3-4: ZERO-ALLOCATION DATA STRUCTURES & BENCHMARKING                                           |
| - Week 3: Memory Layout, Slab Allocators & Direct-Indexed Price Arrays                              |
| - Week 4: Nanosecond Latency Profiling, Hardware Counters & Coordinated Omission                    |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| WEEKS 5-6: LOW-LATENCY CONCURRENCY & NETWORK PROTOCOLS                                              |
| - Week 5: Lock-Free Concurrency, SPSC Ring Buffers & False Sharing Elimination                      |
| - Week 6: Binary Exchange Protocols (NASDAQ OUCH 5.0 & ITCH 5.0)                                    |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| WEEKS 7-8: ADVANCED EXCHANGE MECHANICS & MARKET MICROSTRUCTURE                                      |
| - Week 7: Call Auction (Walrasian Uncrossing) & Pro-Rata Matching Rules                             |
| - Week 8: Sasha Stoikov's Micro-Price & VPIN (Order Flow Toxicity)                                  |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| WEEKS 9-10: SYSTEM HARDENING, VISUALIZATION & SUPERDAY INTERVIEW MASTERY                            |
| - Week 9: Real-time L3 Depth Visualizer & Deterministic mmap Journaling                             |
| - Week 10: Mock Interview Defense, Resume Bullets & GitHub Portfolio Presentation                   |
+-----------------------------------------------------------------------------------------------------+
```

---

### Week 1: Financial Market Mechanics & The Baseline Order Book
> **Goal:** Understand how an electronic stock exchange works in the real world and code a simple, clean matching engine without worrying about speed yet.

#### 1. Concepts Explained in Plain English
- **What is an Order Book?** Think of an exchange as a double-auction marketplace. Buyers want to pay as little as possible (Bids); sellers want to charge as much as possible (Asks).
- **The Spread:** The gap between the Highest Bid and the Lowest Ask. If Bid is $100.00 and Ask is $100.05, the spread is $0.05.
- **Price-Time Priority (FIFO):** If two people want to buy at $100.00, whoever submitted their order first gets filled first.
- **Order Types:**
  - **Limit Order:** "Buy 100 shares of Apple at $150.00 or better." Rests in the book if it cannot match immediately.
  - **Market Order:** "Buy 100 shares right now at whatever price is available." Immediately matches resting asks.
  - **Cancel Order:** Withdraws an unfilled resting order.

#### 2. What to Read & Watch
- **Video:** Search YouTube for *"How Does a Limit Order Book Work?"* by Khan Academy or CME Group.
- **Reading:** Read *"Trading and Exchanges: Market Microstructure for Practitioners"* by Larry Harris (Chapters 1 to 4).
- **Interactive:** Go to Binance, Coinbase, or TradingView, open a depth chart (BTC/USD or AAPL), and watch the bids, asks, and order ladder update in real time.

#### 3. Hands-On Coding Task (Phase 1 Baseline)
1. Set up your compiler (`g++ -std=c++20` or Java 21 LTS).
2. Create basic structs/classes:
   ```cpp
   enum class Side { BUY, SELL };
   struct Order {
       uint64_t order_id;
       Side side;
       uint64_t price;
       uint32_t quantity;
   };
   ```
3. Use standard textbook collections:
   - `std::map<uint64_t, std::list<Order>>` (C++) or `TreeMap<Long, LinkedList<Order>>` (Java).
4. Implement the matching loop:
   - When a BUY order arrives: Check if `price >= lowest ask`. If yes, execute trade and decrement quantity.
   - If remaining quantity $> 0$, insert into the bid book.
5. Write 5 unit tests: exact fill, partial fill, multi-level price sweep, cancellation, and empty book edge cases.

---

### Week 2: Computer Architecture & The "Mechanical Sympathy" Epiphany
> **Goal:** Understand why traditional clean code is slow, how CPU caches work, and how memory access affects performance.

#### 1. Concepts Explained in Plain English
- **The Memory Wall:** A modern CPU runs at ~4.0 GHz, meaning it executes an instruction every ~0.25 nanoseconds. But reading from Main RAM takes ~60 to 100 nanoseconds (hundreds of wasted clock cycles!).
- **The CPU Cache Hierarchy:**
  - **L1 Cache:** ~32 KB per core, ~1 nanosecond access.
  - **L2 Cache:** ~512 KB per core, ~3 to 4 nanoseconds access.
  - **L3 Cache:** ~16 to 64 MB shared across cores, ~10 to 15 nanoseconds access.
  - **RAM:** Gigabytes, but ~60 to 100 nanoseconds access (glacial speed for HFT).
- **Cache Lines (64 Bytes):** The CPU never fetches a single byte. It fetches an entire 64-byte chunk. If your data is contiguous in memory, accessing the next item is free!
- **Why Linked Lists and Trees Are Slow:** A linked list or Red-Black tree allocates nodes randomly across heap memory. Every time you follow a `next` pointer or traverse a tree branch, the CPU suffers a **cache miss** and halts waiting for RAM.
- **The Cost of `malloc` / `new`:** Asking the OS for memory invokes a kernel allocator, acquires locks, and triggers latency spikes.

#### 2. What to Read & Watch
- **Talk:** *"Mechanical Sympathy"* by Martin Thompson (search YouTube).
- **Talk:** *"When a Microsecond Is an Eternity"* by Carl Cook (CppCon 2017) — **The single best talk on low-latency programming ever recorded.**
- **Book:** *"Computer Systems: A Programmer's Perspective"* (CS:APP) by Bryant & O'Hallaron (Chapter 6: The Memory Hierarchy).

#### 3. Hands-On Coding Experiment
1. Write a small standalone program comparing:
   - Traversing an array of 1,000,000 integers (`std::vector<int>`).
   - Traversing a linked list of 1,000,000 integers (`std::list<int>`).
2. Measure the time taken. Notice that the array is **5x to 15x faster**, simply because of CPU cache prefetching!
3. Convert your Week 1 order book prices from `double` to fixed-point integer ticks (`uint64_t cents`).

---

### Week 3: Zero-Allocation Memory Design & Flat Data Structures
> **Goal:** Eliminate all dynamic heap allocations (`malloc`/`new`) on the hot path and replace Red-Black trees with cache-friendly direct arrays.

#### 1. Concepts Explained in Plain English
- **Object Pool / Slab Allocator:** Instead of calling `new Order()` during trading, pre-allocate an array of 1,000,000 `Order` structs at system startup. When an order arrives, grab an unused index from a free-list stack ($O(1)$). When it fills, push the index back. Zero operating system calls!
- **Direct-Indexed Price Array (The Ladder):** In active trading, prices move within a few hundred cents of the market price. Instead of searching a tree, create an array of price levels:
  $$\text{Index} = \text{Price} - \text{BasePrice}$$
  Accessing the best bid or ask is a direct array lookup ($O(1)$), taking a single CPU instruction!
- **Intrusive Doubly-Linked List:** Embed the `prev_index` and `next_index` directly inside the pre-allocated `Order` struct. Adding or removing an order from a price level modifies existing memory—no node wrapper allocations required.

#### 2. What to Read & Study
- **Article:** *"Memory Pools and Slab Allocation"* by Niklas Frykholm.
- **Code Reference:** Look at the GitHub repo for `cameron314/concurrentqueue` or boost intrusive lists to understand the concept of intrusive nodes.

#### 3. Hands-On Coding Task (Phase 2)
1. Implement `SlabAllocator.hpp`:
   - Contiguous array: `std::vector<Order> pool;`
   - Free stack: `std::vector<uint32_t> free_indices;`
   - Implement `allocate()` and `deallocate(uint32_t index)`.
2. Implement `DirectPriceLadder.hpp`:
   - Flat array of `PriceLevel` structs indexed by tick offset.
3. Wire them into `OrderBookOptimized.hpp`.
4. Run your Week 1 test suite to guarantee 100% correctness was preserved.

---

### Week 4: Nanosecond Benchmarking & Latency Tail Analysis
> **Goal:** Master professional latency measurement, eliminate Coordinated Omission, and profile hardware counters using Linux `perf`.

#### 1. Concepts Explained in Plain English
- **Averages Lie:** In trading, an average latency of 5 microseconds means nothing if the 99th percentile (p99) spikes to 50 milliseconds during high-volume market events.
- **Coordinated Omission:** If your benchmark sends an order, waits for the response, and then sends the next order, whenever the server stalls, your client stalls too! You end up measuring fewer requests during the stall, artificially hiding the worst latency spikes. (Discovered by Gil Tene).
- **Hardware Timestamping (`RDTSC`):** Modern x86 CPUs have an instruction called `__rdtsc()` that reads the exact number of CPU clock cycles elapsed since boot. It takes ~7 nanoseconds to call and gives cycle-level accuracy.
- **Hardware Counters (PMU):** The physical CPU chip contains Performance Monitoring Units that count physical events: L1 cache misses, branch mispredictions, instructions per cycle (IPC).

#### 2. What to Read & Watch
- **Talk:** *"How NOT to Measure Latency"* by Gil Tene (Azul Systems, YouTube) — **Essential viewing.**
- **Tool:** Learn what **HdrHistogram** (High Dynamic Range Histogram) is and how it records latency across 5 decimal points of precision without rounding errors.
- **Guide:** Search *"Brendan Gregg: Linux perf Examples"* for hardware counter profiling.

#### 3. Hands-On Coding Task
1. Build an asynchronous benchmark client:
   - Schedule synthetic orders at fixed intervals (e.g., every 10 microseconds) using Poisson arrivals.
   - Record: $\text{Latency} = \text{ResponseTime} - \text{ScheduledSendTime}$.
2. Feed timestamps into `HdrHistogram` (or implement a lightweight logarithmic histogram).
3. Measure Phase 1 vs. Phase 2 side by side:
   - Print p50, p90, p99, p99.9, and p99.99 percentiles.
4. If on Linux / WSL: Run `perf stat -e L1-dcache-load-misses,branch-misses ./benchmark`. Observe the massive drop in cache misses in Phase 2!

---

### Week 5: Lock-Free Concurrency & The Single-Writer Principle
> **Goal:** Scale your engine to handle multi-threaded order entry without mutex lock contention or false sharing.

#### 1. Concepts Explained in Plain English
- **Why Mutexes Fail in Low Latency:** A mutex relies on the operating system scheduler. When two threads fight for a lock, the loser is put to sleep by the kernel. Waking up a sleeping thread takes 5 to 50 microseconds!
- **MESI Cache Invalidation (Ping-Pong):** When multiple CPU cores write to the same memory address (like a shared mutex or order book pointer), CPU caches must talk over the motherboard bus to invalidate old copies. This hardware traffic stalls the CPU.
- **The Single-Writer Principle (Disruptor Pattern):** Instead of having 8 threads lock the order book, **only ONE dedicated thread touches the book**. Inbound orders are dropped into a lock-free queue, and the matching thread consumes them at full speed.
- **Lock-Free SPSC Ring Buffer:** A circular array with two atomic indices: a `write_cursor` (only modified by the producer) and a `read_cursor` (only modified by the consumer). No locks, only atomic memory barriers (`acquire`/`release`).
- **False Sharing:** A cache line is 64 bytes. If the producer's write cursor and the consumer's read cursor sit inside the same 64 bytes, they invalidate each other's cache even though they are different variables! Solution: Pad them with `alignas(64)`.

#### 2. What to Read & Watch
- **Paper / Talk:** *"The LMAX Disruptor: High performance alternative to bounded queues for exchanging data between threads"* by Martin Thompson et al.
- **Video:** *"CppCon 2014: Lock-Free Programming (Part 1 & 2)"* by Herb Sutter.
- **Concept:** Search *"What is False Sharing in C++?"* on YouTube / StackOverflow.

#### 3. Hands-On Coding Task (Phase 3)
1. Write `SpscRingBuffer.hpp`:
   - Circular array of fixed size (power of 2, e.g., 65536, for bitwise modulo `index & (size - 1)`).
   - Use `std::atomic<uint64_t>` for head and tail.
   - Add `alignas(64)` padding between cursors to prevent false sharing.
2. Thread Pinning:
   - Use `pthread_setaffinity_np` (Linux) or `SetThreadAffinityMask` (Windows) to pin the matching engine thread to Core 2 and the gateway thread to Core 3.
3. Benchmark: Compare 8 threads pounding a mutex-protected book vs. 8 threads submitting to SPSC ring buffers feeding the Single-Writer core. Observe throughput jumping to millions of orders/sec!

---

### Week 6: Binary Exchange Protocols (NASDAQ OUCH & ITCH)
> **Goal:** Eliminate text and JSON serialization overhead by implementing authentic binary exchange protocols used on Wall Street.

#### 1. Concepts Explained in Plain English
- **Why Wall Street Hates JSON/REST:** Parsing a JSON string requires scanning characters, allocating memory for strings, and converting text numbers to binary. In HFT, parsing a single JSON message can take 5 microseconds—longer than our entire matching process!
- **Binary Protocols:** Instead of sending `"{\"price\": 100.25}"`, the exchange sends packed binary bytes. A 64-bit integer takes exactly 8 bytes.
- **NASDAQ OUCH 5.0:** The binary protocol used by trading firms to send orders into NASDAQ. Messages include:
  - `Enter Order ('O')`: Packet containing Client Order ID, Buy/Sell, Quantity, Symbol, Price.
  - `Order Executed ('E')`: Notifies client of execution.
- **NASDAQ ITCH 5.0:** The binary multicast protocol used by NASDAQ to broadcast every single book event to the entire market. Emits Level 3 events: `Add Order ('A')`, `Order Executed ('E')`, `Order Cancel ('D')`.
- **Zero-Copy Deserialization:** Instead of copying packet data, cast the raw network byte pointer directly into a packed C++ struct:
  ```cpp
  #pragma pack(push, 1)
  struct OuchEnterOrder {
      char message_type; // 'O'
      uint64_t order_token;
      char buy_sell;     // 'B' or 'S'
      uint32_t shares;
      char stock[8];
      uint32_t price;
  };
  #pragma pack(pop)
  ```

#### 2. What to Read & Study
- **Specification:** Download and read the official public PDF: *"NASDAQ ITCH 5.0 Specification"* (freely available online).
- **Specification:** Download and review *"NASDAQ OUCH 5.0 Specification"*.
- **Concept:** Endianness (`ntohl`, `htonl` / `std::byteswap` for network big-endian vs x86 little-endian).

#### 3. Hands-On Coding Task
1. Implement `OuchCodec.hpp`: Zero-copy binary parser that reads raw byte buffers into order commands.
2. Implement `ItchPublisher.hpp`: Multicast UDP generator that serializes internal matches into ITCH packets.
3. Test with a mock UDP socket: Send 100,000 binary packets through loopback (`127.0.0.1`) and verify zero allocations during encoding and decoding.

---

### Week 7: Advanced Exchange Mechanics (Call Auctions & Pro-Rata)
> **Goal:** Implement real institutional exchange rules: Walrasian equilibrium market openings and CME-style pro-rata allocation.

#### 1. Concepts Explained in Plain English
- **Continuous Trading vs. Call Auction:** Stock markets do not open abruptly. At 9:00 AM, orders accumulate in the book without matching. At 9:30 AM, the exchange runs an **Uncrossing Cross (Call Auction)**: it finds a single **Equilibrium Clearing Price** where the maximum volume crosses, and all matching trades execute at that single price.
- **Walrasian Equilibrium Algorithm:**
  1. For each potential price: Calculate cumulative Buy volume $\ge$ price, and cumulative Sell volume $\le$ price.
  2. The executable volume is $\min(\text{CumBuy}, \text{CumSell})$.
  3. Pick the price that maximizes executable volume and minimizes remaining surplus.
- **Pro-Rata Allocation (CME Futures):** In interest rate and Treasury futures, FIFO is not used because queue sizes are massive. Instead, fills are distributed **proportionally to order size**:
  $$\text{Allocation}_i = \left\lfloor \text{MatchedQty} \times \frac{\text{OrderQty}_i}{\text{TotalDepthAtPrice}} \right\rfloor$$
- **Advanced Orders:**
  - **Iceberg Order:** Only shows 100 shares on the book (display), but keeps 9,900 shares hidden in reserve.
  - **Self-Trade Prevention (STP):** Prevents two trading desks at Goldman Sachs from illegally trading with each other (wash trading).

#### 2. What to Read & Study
- **Whitepaper:** CME Group's guide: *"Pro-Rata Allocation Algorithms in Futures Markets"*.
- **Exchange Rulebook:** NASDAQ Equities Rule 4752 (Opening Cross).

#### 3. Hands-On Coding Task
1. Implement `CallAuction.hpp`: State machine supporting `PRE_OPEN` accumulation and `UNCROSS()` equilibrium price discovery.
2. Implement configurable matching engine rules: Add a switch between `FIFO` and `PRO_RATA`.
3. Add Iceberg order logic: Replenish display size from reserve and assign a new time-priority timestamp upon replenishment.

---

### Week 8: Market Microstructure & Algorithmic Trading Sandbox
> **Goal:** Connect quantitative finance theory to your engine: Stoikov's Micro-Price, order flow toxicity (VPIN), and an autonomous market-making bot.

#### 1. Concepts Explained in Plain English
- **Mid-Price vs. Micro-Price:** Mid-price is simply $\frac{\text{Bid} + \text{Ask}}{2}$. But if there are 10,000 shares bidding at $100.00 and only 100 shares asking at $100.05, the price is obviously about to tick up!
  - **Sasha Stoikov's Micro-Price** adjusts for queue depth imbalance:
    $$P_{\text{micro}} = P_{\text{bid}} \cdot \frac{Q_{\text{ask}}}{Q_{\text{bid}} + Q_{\text{ask}}} + P_{\text{ask}} \cdot \frac{Q_{\text{bid}}}{Q_{\text{bid}} + Q_{\text{ask}}}$$
- **VPIN (Volume-Synchronized Probability of Toxicity):** Measures whether order flow is coming from informed traders (who know something you don't) vs. uninformed noise traders.
- **Avellaneda-Stoikov Market Maker:** A mathematical model for an automated trading bot that places bids and asks to earn the spread while adjusting quotes based on its inventory risk (so it doesn't get caught holding too much stock if the market crashes).

#### 2. What to Read & Study
- **Classic Paper:** *"The Micro-Price: a high frequency estimator of future prices"* by Sasha Stoikov (2018).
- **Classic Paper:** *"High-frequency trading in a limit order book"* by Marco Avellaneda and Sasha Stoikov (2008).
- **Paper:** *"The Volume Clock: Insights into the High-Frequency Trading Process"* (VPIN) by Easley, Lopez de Prado, and O'Hara (2012).

#### 3. Hands-On Coding Task
1. Build `MicroPrice.hpp`: Compute the multi-level depth micro-price on every book update.
2. Build `VpinCalculator.hpp`: Track trade volume buckets and calculate order toxicity.
3. Build `MarketMakerBot.hpp`: An autonomous agent that consumes your ITCH feed, computes its reservation price, and submits OUCH limit orders into your book.

---

### Week 9: System Hardening, Real-Time Visualizer & Determinism
> **Goal:** Build a live visual depth ladder, create an append-only transaction journal, and prove 100% deterministic crash recovery.

#### 1. Concepts Explained in Plain English
- **Deterministic Event Sourcing:** An exchange must be a deterministic finite state machine (FSM). If you give it the exact same sequence of 10,000,000 orders, it must produce the exact same trades and order book state down to the last bit.
- **Memory-Mapped Journaling (`mmap`):** Map a file directly into memory. Appending an event is just a memory write (`memcpy`). The OS asynchronously flushes dirty pages to disk, giving high-speed durability.
- **Real-Time Visualizer:** A front-end web dashboard (React / Canvas) or high-speed terminal UI (FTXUI in C++) that shows the live order book ladder, queue position, and latency distribution histogram.

#### 2. Hands-On Coding Task
1. Implement `BinaryJournal.hpp`: Use `mmap` to write every inbound order and cancel command with a monotonic 64-bit sequence number.
2. Crash Recovery Test:
   - Run 1,000,000 trades. Compute an MD5/SHA256 checksum of the final book state.
   - Force kill the process (`kill -9`).
   - Start the engine in recovery mode, replay the journal, and assert that the recovered state checksum matches 100%.
3. Connect a lightweight WebSocket or WebTransport bridge to stream L2 depth snapshots to a frontend chart.

---

### Week 10: Superday Interview Defense & Portfolio Packaging
> **Goal:** Practice explaining every technical decision in under 2 minutes, format your resume bullets, and polish your GitHub repository to stand out to top recruiters.

#### 1. Master These 4 Interview Defense Questions
1. **"Why did you build an evolutionary baseline first?"**
   - *Answer:* *"To ensure 100% correctness first, and to establish empirical baseline metrics. Rather than guessing bottlenecks, I used Linux perf and RDTSC hardware timers to identify that 16.4% L1 cache misses and heap allocations were our latency drivers."*
2. **"Why avoid `std::map` / `TreeMap`?"**
   - *Answer:* *"Red-Black trees require heap node allocations and pointer-chasing across cache lines. I replaced active ticks around the BBO with an O(1) direct-indexed flat array, prefetching data sequentially into L1 cache."*
3. **"How did you prevent False Sharing in your lock-free queue?"**
   - *Answer:* *"Modern x86 CPUs maintain cache coherence in 64-byte lines. If the producer write-cursor and consumer read-cursor sit on the same line, the cores continuously invalidate each other's cache. I isolated both cursors using `alignas(64)` padding."*
4. **"How did you handle Coordinated Omission?"**
   - *Answer:* *"Synchronous load testers block when the server stalls, masking the true tail latency. I built an asynchronous driver using Poisson arrivals that tracks scheduled vs. actual arrival times via HdrHistogram, accurately capturing p99.99 outliers."*

#### 2. Final Portfolio Polish
- Add an architecture diagram to your `README.md`.
- Include the **Phase 1 vs. Phase 2 vs. Phase 3 benchmark table** with latency percentiles.
- Record a short 60-second GIF or video of your visualizer and terminal benchmark running.

---

## 4. Suggested Daily Routine (1.5 - 2 Hours / Day)

| Time Allocation | Activity | Focus |
| :--- | :--- | :--- |
| **First 30 Minutes** | **Concept & Reading** | Watch 1 recommended talk or read 1 paper/chapter. Take notes on key terminology. |
| **Next 60 Minutes** | **Hands-on Coding** | Write code for that week's deliverable. Keep it modular and test-driven. |
| **Final 15-20 Minutes** | **Benchmarking / Reflection** | Run your unit tests, profile memory/cycles, and write a 3-bullet summary of what you learned. |

---

## 5. Curated Master Resource Library

### Books
1. **Computer Systems: A Programmer's Perspective (CS:APP)** — Bryant & O'Hallaron (The bible of systems).
2. **Trading and Exchanges: Market Microstructure for Practitioners** — Larry Harris.
3. **Effective Modern C++** — Scott Meyers (or *Java Concurrency in Practice* by Brian Goetz if using Java).

### Top Video Lectures
1. **Carl Cook (CppCon 2017):** *"When a Microsecond Is an Eternity: High Performance C++ in Trading"* (Search on YouTube).
2. **Martin Thompson:** *"Mechanical Sympathy"* & *"Designing for Low Latency"* (Search on GOTO Conferences).
3. **Gil Tene:** *"How NOT to Measure Latency"* (Search on InfoQ / YouTube).
4. **Herb Sutter:** *"Lock-Free Programming (Parts 1 & 2)"* (CppCon 2014).

### Key Industry Papers
1. **The LMAX Disruptor Architecture** — Martin Thompson, Dave Farley, Michael Barker.
2. **Sasha Stoikov (2018):** *"The Micro-Price: A High Frequency Estimator of Future Prices"*.
3. **Avellaneda & Stoikov (2008):** *"High-Frequency Trading in a Limit Order Book"*.
4. **NASDAQ ITCH 5.0 & OUCH 5.0 Official Specifications** (Available from nasdaqtrader.com).

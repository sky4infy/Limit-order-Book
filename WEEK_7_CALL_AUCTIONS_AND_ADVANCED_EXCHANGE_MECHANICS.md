# Week 7: Advanced Exchange Mechanics, Call Auctions, and Market Microstructure

## 1. Executive Summary & Microstructure Architecture
Modern financial exchanges (NASDAQ, NYSE, CME, Eurex, Euronext) do not rely solely on continuous price-time priority (FIFO) matching. A high-performance trading engine must support complex market microstructure mechanics:
1. **Discrete Call Auctions (The Uncrossing Cross)**: Periodic batch auctions for market opening, closing, and intraday volatility halts (LULD / Limit Up-Limit Down) using Walrasian Equilibrium clearing price discovery.
2. **Pro-Rata Matching vs Price-Time Priority (FIFO)**: Used in CME interest rate, Treasury, and short-term debt derivatives to prevent queue-stuffing and reward institutional liquidity size.
3. **Advanced Institutional Order Types (Iceberg / Reserve Orders)**: Splitting massive orders into visible (display/peak) and hidden pools, with automatic queue replenishment and loss of time priority.
4. **Self-Trade Prevention (STP / Wash-Trading Guards)**: Regulatory compliance ensuring that proprietary orders originating from the same trading entity or firm ID do not execute against each other.

---

## 2. Discrete Call Auctions: Walrasian Equilibrium Algorithm

### The Four Objectives of Price Discovery
When uncrossing an accumulation of pre-market orders (both Limit-on-Open LOO and Market-on-Open MOO), the exchange executes a 4-tier optimization algorithm:

```mermaid
flowchart TD
    A[Pre-Market Order Accumulation: LOO & MOO] --> B[Evaluate Every Candidate Price P]
    B --> C[Compute Cumulative Buy: P_order >= P]
    B --> D[Compute Cumulative Sell: P_order <= P]
    C & D --> E[Matched Volume: V = min CumBuy, CumSell]
    E --> F{Objective 1: Maximize Volume V}
    F -->|Multiple Prices| G{Objective 2: Minimize Imbalance |CumBuy - CumSell|}
    G -->|Tied Imbalance| H{Objective 3: Directional Surplus}
    H -->|Buy Surplus| I[Select Highest Price: Incentivize Sellers]
    H -->|Sell Surplus| J[Select Lowest Price: Incentivize Buyers]
    H -->|Balanced Surplus| K{Objective 4: Reference Price Proximity}
    K --> L[Select Price Closest to Previous Close]
```

### Mathematical Formulation
For each distinct candidate price $P$:
$$\text{CumBuy}(P) = \sum_{o \in \text{Buys}, P_o \ge P} Q_o + \sum_{o \in \text{MOO Buys}} Q_o$$
$$\text{CumSell}(P) = \sum_{o \in \text{Sells}, P_o \le P} Q_o + \sum_{o \in \text{MOO Sells}} Q_o$$
$$\text{Matched}(P) = \min(\text{CumBuy}(P), \text{CumSell}(P))$$
$$\text{Imbalance}(P) = |\text{CumBuy}(P) - \text{CumSell}(P)|$$

Once the clearing price $P^*$ is locked:
1. All buy orders with $P_o > P^*$ and sell orders with $P_o < P^*$ are filled 100%.
2. Limit orders at exactly $P^*$ are matched in time-priority (or pro-rata) up to the clearing volume.
3. Every execution takes place at the single clearing price $P^*$.

---

## 3. Matching Algorithms: FIFO vs CME Pro-Rata

### Price-Time Priority (FIFO)
- Orders at the same price level are served strictly in order of arrival timestamp.
- **Microstructure Consequence**: Massive race for sub-microsecond latency. Traders prioritize co-location and FPGA gateways to be first in line.
- **Engine Complexity**: $O(1)$ queue iteration. Ultra-low latency (22 ns median).

### CME Pure Pro-Rata Allocation
In Treasury and Eurodollar futures, spreads are pinned to 1 tick. Prioritizing pure latency leads to excessive speculative cancellations. Pro-Rata allocates incoming aggressor volume proportionally to resting order size:

$$\text{Allocation}_i = \left\lfloor Q_{\text{taker}} \times \frac{Q_i}{\sum_{j} Q_j} \right\rfloor$$

### The CME Remainder Allocation Rule
Because integer truncation $\lfloor \dots \rfloor$ leaves undistributed contracts:
$$Q_{\text{remainder}} = Q_{\text{taker}} - \sum_i \text{Allocation}_i$$
The remaining contracts are distributed one-by-one according to the **largest fractional remainder** ($Q_i \cdot \frac{Q_{\text{taker}}}{Q_{\text{total}}} - \lfloor \dots \rfloor$). If fractions are equal, arrival timestamp acts as the tie-breaker.

---

## 4. Advanced Order Types & Self-Trade Prevention

### Iceberg (Reserve) Orders
Institutional players executing block sizes (e.g., 500,000 shares) cannot reveal their full hand without moving the market against them.
- **Structure**: Total Quantity = 500,000, Peak (Display) = 10,000, Hidden = 490,000.
- **Execution Lifecycle**:
  1. Engine inserts 10,000 shares at the price level.
  2. Aggressor consumes the 10,000 visible shares.
  3. Engine triggers automatic replenishment: pulls 10,000 from hidden reserves.
  4. **Critical Rule**: The replenished slice is tagged with a brand new timestamp and placed at the tail of the FIFO queue at that price level!

### Self-Trade Prevention (STP) Policies
Market manipulation rules (CFTC Rule 180.1, SEC Rule 10b-5) forbid wash trading. When an aggressor matches against an order with the same `firm_id`:

| STP Policy | Action on Matching | Use Case |
|---|---|---|
| `CANCEL_MAKER` | Maker order is cancelled; Taker continues to match next book depth | Aggressive smart routing algorithms that must fill |
| `CANCEL_TAKER` | Incoming Taker is killed immediately; Resting Maker remains in book | Passive market-making algorithms defending quotes |
| `DECREMENT_AND_CANCEL` | Smaller order cancelled; Larger order reduced by difference | Minimizes unnecessary order cancellations |
| `CANCEL_BOTH` | Both resting maker and incoming taker are immediately killed | Strict compliance / risk hard stops |

---

## 5. Empirical Benchmark Results (100,000 Executions)

```
================================================================================================
          WEEK 7: FIFO MATCHING VS CME PRO-RATA ALLOCATION BENCHMARK (100,000 RUNS)             
================================================================================================
Metric                           FIFO Priority          CME Pro-Rata           Trade-off
------------------------------------------------------------------------------------------------
Iterations                              100000                100000          100% Match
Wall Time (ms)                           15.07                 63.91          4.2x FASTER (FIFO)
Throughput (ops/s)               6634410 ops/s         1564725 ops/s          4.2x HIGHER (FIFO)
------------------------------------------------------------------------------------------------
  LATENCY PERCENTILES:
p50 (Median)                             22 ns                501 ns          22.7x LOWER (FIFO)
p90                                      46 ns                540 ns          11.7x LOWER (FIFO)
p99                                      72 ns               1378 ns          19.1x LOWER (FIFO)
p99.9 (Tail)                            110 ns               1862 ns          16.9x LOWER (FIFO)
Max (Outlier)                        120234 ns              75041 ns          Comparable
================================================================================================
```

### Microsecond Call Auction Results:
- **10,000 Orders Uncrossed**: 668,153 shares matched across 5,239 fills in 23.99 milliseconds.
- **Per-Order Evaluation Latency**: 2,399 ns.

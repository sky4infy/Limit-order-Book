# Week 7: Advanced Exchange Mechanics & Microstructure Interview Defense

## 1. Core Technical Concepts & High-Level Narrative
In Week 7, we expanded our matching core from simple continuous price-time priority into an institutional-grade exchange matching system capable of running discrete Call Auctions, CME-style Pro-Rata allocations, Iceberg order replenishments, and regulatory Self-Trade Prevention (STP).

---

## 2. Institutional Interview Q&A

### Q1: "Walk me through the discrete Call Auction algorithm. How is the clearing price determined?"
**Interview Answer:**
"The Call Auction uncrossing operates on the economic principle of Walrasian Equilibrium. Instead of continuous matching, orders accumulate during the pre-market period (both Limit-on-Open LOO and Market-on-Open MOO). When the auction uncrosses, the engine evaluates every candidate price using four deterministic optimization criteria:
1. **Volume Maximization**: It selects the price $P^*$ that maximizes matched volume $V(P) = \min(\text{CumBuy}(P), \text{CumSell}(P))$.
2. **Imbalance Minimization**: If multiple prices produce equal max volume, it selects the price minimizing the absolute imbalance $|\text{CumBuy}(P) - \text{CumSell}(P)|$.
3. **Surplus Direction**: If still tied, it evaluates net pressure. If there is a buy surplus (excess demand), it selects the higher price to incentivize sellers; if there is a sell surplus, it selects the lower price to incentivize buyers.
4. **Reference Price Proximity**: If completely balanced, it selects the candidate price closest to the reference price (e.g. previous official close).

Once $P^*$ is locked, all eligible orders match at exactly $P^*$, and uncrossing fills are broadcast to participants."

---

### Q2: "Why do derivatives exchanges like CME use Pro-Rata matching instead of FIFO?"
**Interview Answer:**
"In fixed-income and interest-rate futures (such as CME Eurodollars or 10-Year Treasury Note futures), the bid-ask spread is pinned to the minimum tick for months, and depth at the top of the book can be tens of thousands of contracts.
- In a pure FIFO market, being 1 nanosecond slower means you are buried behind 50,000 contracts and will never get filled. This triggers an extreme arms race for pure speed and leads to harmful behavior like queue-stuffing and cancellation storms.
- CME uses **Pro-Rata matching** to reward liquidity size rather than pure speed. Incoming aggressive orders are allocated proportionally:
  $$\text{Allocation}_i = \left\lfloor Q_{\text{taker}} \times \frac{Q_i}{Q_{\text{total}}} \right\rfloor$$
- We implemented the exact CME remainder distribution rule: after integer flooring, residual contracts are distributed by largest fractional remainder.
- In our benchmarks, FIFO matched in 22ns median latency, while Pro-Rata took 501ns because of the fractional division and sorting math—a classic computational trade-off between algorithmic latency and market quality."

---

### Q3: "How do you implement an Iceberg order, and why must it lose time priority upon replenishment?"
**Interview Answer:**
"An Iceberg order specifies a `total_quantity` and a visible `display_quantity` (peak).
1. When submitted, only the peak quantity is inserted into the active price ladder; the remaining quantity is stored in a private hidden pool.
2. When aggressive flow fills the visible peak, the engine triggers an automatic replenishment callback.
3. The engine pulls the next peak slice from the hidden pool and re-inserts it into the ladder.
4. **Crucial Rule**: The replenished slice is assigned the **current timestamp** of replenishment, relegating it to the **back of the FIFO queue** at that price.
5. If the exchange allowed hidden volume to keep its original queue priority, market participants who posted transparent limit orders after the iceberg arrived would be unfairly displaced by invisible phantom liquidity."

---

### Q4: "What is Self-Trade Prevention (STP) and what are the standard execution policies?"
**Interview Answer:**
"Under SEC Rule 10b-5 and CFTC regulations, wash trading (buying and selling from yourself to create artificial volume or manipulate the tape) is strictly illegal. Institutional market makers have multiple automated trading bots operating on the same exchange, which could accidentally cross each other.

Our engine enforces four standard STP policies on matching:
1. `CANCEL_MAKER`: The resting maker order is cancelled from the book. The incoming taker retains its full volume and continues matching deeper liquidity.
2. `CANCEL_TAKER`: The incoming taker order is killed immediately upon crossing. The resting maker remains intact on the book.
3. `DECREMENT_AND_CANCEL`: The smaller of the two orders is cancelled, and the larger order is decremented by the matched quantity and continues its lifecycle.
4. `CANCEL_BOTH`: Both orders are immediately expunged from the engine without execution."

---

## 3. Quantitative Summary of Week 7 Achievements

| Feature | Design / Implementation | Verified In |
|---|---|---|
| **Walrasian Call Auction** | 4-objective optimization uncrossing | `src/exchange/CallAuction.hpp` |
| **CME Pro-Rata Matching** | Fractional division + largest remainder distribution | `src/exchange/ProRataMatching.hpp` |
| **Split FIFO / Pro-Rata** | Configurable ratio (e.g. 20% Top FIFO, 80% Pro-Rata) | `src/exchange/ProRataMatching.hpp` |
| **Iceberg Orders** | Peak slicing + queue demotion on refill | `src/exchange/AdvancedOrders.hpp` |
| **Self-Trade Prevention** | 4 standard institutional policies | `src/exchange/AdvancedOrders.hpp` |
| **Unit Test Coverage** | 5 comprehensive multi-scenario tests | `test/ExchangeMechanicsTests.cpp` (PASSED) |
| **Empirical Benchmark** | 10k auction uncrossing + 100k FIFO vs Pro-Rata | `benchmark/AuctionBenchmark.cpp` (PASSED) |

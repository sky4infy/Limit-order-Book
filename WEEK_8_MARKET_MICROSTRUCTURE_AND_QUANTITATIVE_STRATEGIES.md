# Week 8: Market Microstructure Signals & Algorithmic Quoting Strategies

## 1. Executive Overview & Microstructure Theory
In Week 8, we bridge low-latency core engineering with quantitative algorithmic trading. A production high-frequency trading (HFT) engine cannot operate blind to order flow dynamics. We implemented three mathematical models:
1. **Sasha Stoikov's Micro-Price Estimator (2018)**: Adjusting standard mid-price by order book queue imbalance to predict the next mid-price tick.
2. **Volume-Synchronized Probability of Toxicity (VPIN - Easley, Lopez de Prado, O'Hara 2012)**: Measuring the probability of informed directional flow in volume time to protect market makers against toxic adverse selection.
3. **Avellaneda-Stoikov High-Frequency Market Making Model (2008)**: Optimal dynamic limit order quoting with reservation price and inventory-risk aversion.

---

## 2. Sasha Stoikov's Micro-Price Estimator

### The Failure of Mid-Price
The classical mid-price:
$$\text{Mid} = \frac{P_{bid} + P_{ask}}{2}$$
completely ignores the quantities resting at the best bid ($Q_b$) and best ask ($Q_a$). If the bid queue has 10,000 shares and the ask queue has only 100 shares, the price is almost certain to tick upward. Mid-price fails to capture this probability.

### Mathematical Formulation
Let the queue imbalance ratio be:
$$I = \frac{Q_b}{Q_b + Q_a} \in [0, 1]$$
The probability-weighted Micro-Price is:
$$\text{MicroPrice} = I \times P_{ask} + (1 - I) \times P_{bid} = P_{bid} + I \times (P_{ask} - P_{bid})$$

For deep order books, we implemented **Multi-Level Harmonic Decay Micro-Price**:
$$\text{MicroPrice}_{L2} = \frac{\sum_{k=1}^N \frac{1}{k} \cdot \left[ I_k \cdot P_{ask, k} + (1 - I_k) \cdot P_{bid, k} \right]}{\sum_{k=1}^N \frac{1}{k}}$$

---

## 3. Volume-Synchronized Probability of Toxicity (VPIN)

### Trading in Volume Time
Clock time (seconds/milliseconds) is an illusion in financial markets: high-information news bursts generate millions of shares in seconds, while lunch hours are quiet. VPIN samples the market in **Volume Time** by partitioning trade flow into discrete volume buckets of size $V_{bucket}$.

### Lee-Ready Trade Classifier
For every trade $k$, the initiator is determined via the tick rule:
$$\text{Side}_k = \begin{cases} 
\text{BUY} & \text{if } P_k > P_{k-1} \\ 
\text{SELL} & \text{if } P_k < P_{k-1} \\ 
\text{Previous} & \text{if } P_k = P_{k-1} 
\end{cases}$$

### Formula & Toxicity Threshold
Across a rolling window of $N$ completed volume buckets:
$$\text{VPIN} = \frac{\sum_{\tau=1}^N |V_\tau^B - V_\tau^S|}{N \times V_{bucket}} \in [0, 1]$$

- **Balanced Market ($\text{VPIN} \approx 0.0 - 0.25$)**: Flow is uncoordinated retail/noise. Market makers earn the spread safely.
- **Toxic Run ($\text{VPIN} \ge 0.70$)**: Informed institutional or algorithmic sweep. Market makers must immediately widen quotes or pull resting orders to avoid toxic adverse selection.

---

## 4. Avellaneda-Stoikov Market Making Model

### Mathematical Formulation
A high-frequency market maker faces inventory risk: holding long or short positions exposes capital to market drift.
- Asset mid-price: $s$
- Current inventory: $q$
- Volatility: $\sigma$
- Risk-aversion coefficient: $\gamma$
- Time remaining: $T - t$
- Book liquidity parameter: $\kappa$

### 1. The Reservation (Indifference) Price
$$R(s, q, t) = s - q \cdot \gamma \cdot \sigma^2 \cdot (T - t)$$
- If $q > 0$ (long): $R < s$ (values stock lower, urgently seeks to sell).
- If $q < 0$ (short): $R > s$ (values stock higher, urgently seeks to buy).
- If $q = 0$ (flat): $R = s$.

### 2. Optimal Quotes
$$\text{Half-Spread} = \frac{1}{\gamma} \ln\left(1 + \frac{\gamma}{\kappa}\right)$$
$$P_{bid}^* = \text{round}\left(R(s, q, t) - \text{Half-Spread}\right)$$
$$P_{ask}^* = \text{round}\left(R(s, q, t) + \text{Half-Spread}\right)$$

---

## 5. Empirical Benchmark Results (1,000,000 Evaluations)

```
================================================================================================
      WEEK 8: MICROSTRUCTURE SIGNAL & STRATEGY EXECUTION BENCHMARK (1,000,000 EVALS)      
================================================================================================
Metric                    Stoikov Micro-Price   VPIN Toxicity Calc    Avellaneda-Stoikov    
--------------------------------------------------------------------------------------------
Samples Evaluated         1,000,000             1,000,000             1,000,000             
Wall Time (ms)            46.95 ms              56.82 ms              50.98 ms              
Throughput (ops/s)        21,298,601 ops/s      17,597,964 ops/s      19,616,421 ops/s      
--------------------------------------------------------------------------------------------
LATENCY PERCENTILES (All in Nanoseconds):
p50 (Median)              19 ns                 26 ns                 19 ns                 
p90                       22 ns                 38 ns                 34 ns                 
p99                       42 ns                 62 ns                 38 ns                 
p99.9 (Tail)              213 ns                254 ns                54 ns                 
Max (Outlier)             31,251 ns             215,918 ns            53,910 ns             
============================================================================================
```

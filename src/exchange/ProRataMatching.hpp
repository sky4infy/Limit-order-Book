#pragma once

#include "../common/Types.hpp"
#include "ExchangeTypes.hpp"
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>

namespace lob {

struct ProRataRestingOrder {
    uint64_t order_id;
    uint32_t firm_id;
    Quantity quantity;
    Quantity remaining_quantity;
    uint64_t timestamp;
};

class ProRataAllocationEngine {
public:
    struct AllocationResult {
        uint64_t order_id;
        Quantity allocated_qty;
        Quantity remaining_qty;
    };

    // Pure Pro-Rata with CME Remainder Distribution
    static std::vector<AllocationResult> allocate_pure_pro_rata(
        std::vector<ProRataRestingOrder>& resting_orders,
        Quantity aggressive_qty)
    {
        std::vector<AllocationResult> results;
        if (resting_orders.empty() || aggressive_qty == 0) return results;

        Quantity total_available = 0;
        for (const auto& o : resting_orders) {
            total_available += o.remaining_quantity;
        }

        Quantity fillable_qty = std::min(aggressive_qty, total_available);
        if (fillable_qty == 0) return results;

        // Step 1: Base integer pro-rata allocation
        Quantity allocated_sum = 0;
        struct AllocationWork {
            size_t index;
            uint64_t order_id;
            Quantity base_allocated;
            double exact_share;
            double fractional_remainder;
            uint64_t timestamp;
        };

        std::vector<AllocationWork> work(resting_orders.size());
        for (size_t i = 0; i < resting_orders.size(); ++i) {
            double exact = static_cast<double>(fillable_qty) * 
                           static_cast<double>(resting_orders[i].remaining_quantity) / 
                           static_cast<double>(total_available);
            Quantity base = static_cast<Quantity>(std::floor(exact));
            // Cannot allocate more than available
            base = std::min(base, resting_orders[i].remaining_quantity);

            work[i] = {
                i,
                resting_orders[i].order_id,
                base,
                exact,
                exact - static_cast<double>(base),
                resting_orders[i].timestamp
            };
            allocated_sum += base;
        }

        // Step 2: Remainder Distribution (CME Rounding Rule)
        // Distribute remaining contracts by time priority (or largest fractional remainder)
        Quantity remainder = fillable_qty - allocated_sum;
        if (remainder > 0) {
            // Sort by timestamp (FIFO priority for rounding remainder)
            std::vector<size_t> priority_indices(work.size());
            std::iota(priority_indices.begin(), priority_indices.end(), 0);
            std::sort(priority_indices.begin(), priority_indices.end(), [&work](size_t a, size_t b) {
                // CME rule: largest fraction first; if equal, earliest timestamp
                if (std::abs(work[a].fractional_remainder - work[b].fractional_remainder) > 1e-6) {
                    return work[a].fractional_remainder > work[b].fractional_remainder;
                }
                return work[a].timestamp < work[b].timestamp;
            });

            for (size_t idx : priority_indices) {
                if (remainder == 0) break;
                size_t o_idx = work[idx].index;
                if (work[idx].base_allocated < resting_orders[o_idx].remaining_quantity) {
                    work[idx].base_allocated += 1;
                    remainder -= 1;
                }
            }
        }

        // Apply allocations to resting orders
        for (const auto& w : work) {
            resting_orders[w.index].remaining_quantity -= w.base_allocated;
            results.push_back({
                w.order_id,
                w.base_allocated,
                resting_orders[w.index].remaining_quantity
            });
        }

        return results;
    }

    // Split FIFO / Pro-Rata (e.g. 20% to Top-of-Book FIFO, 80% to Pro-Rata)
    static std::vector<AllocationResult> allocate_split_fifo_pro_rata(
        std::vector<ProRataRestingOrder>& resting_orders,
        Quantity aggressive_qty,
        double fifo_ratio = 0.20)
    {
        std::vector<AllocationResult> results;
        if (resting_orders.empty() || aggressive_qty == 0) return results;

        // Step 1: Calculate FIFO portion
        Quantity fifo_qty = static_cast<Quantity>(std::floor(static_cast<double>(aggressive_qty) * fifo_ratio));
        Quantity pro_rata_qty = aggressive_qty - fifo_qty;

        // Sort by timestamp for FIFO pass
        std::sort(resting_orders.begin(), resting_orders.end(), [](const auto& a, const auto& b) {
            return a.timestamp < b.timestamp;
        });

        std::vector<Quantity> total_allocated(resting_orders.size(), 0);

        // Allocate FIFO portion
        Quantity fifo_remaining = fifo_qty;
        for (size_t i = 0; i < resting_orders.size() && fifo_remaining > 0; ++i) {
            Quantity fill = std::min(resting_orders[i].remaining_quantity, fifo_remaining);
            total_allocated[i] += fill;
            resting_orders[i].remaining_quantity -= fill;
            fifo_remaining -= fill;
        }

        // Leftover FIFO volume moves to pro-rata volume
        pro_rata_qty += fifo_remaining;

        // Allocate Pro-Rata portion on remaining quantities
        auto pro_rata_results = allocate_pure_pro_rata(resting_orders, pro_rata_qty);

        // Merge results
        for (size_t i = 0; i < resting_orders.size(); ++i) {
            uint64_t id = resting_orders[i].order_id;
            Quantity pr_fill = 0;
            for (const auto& pr : pro_rata_results) {
                if (pr.order_id == id) {
                    pr_fill = pr.allocated_qty;
                    break;
                }
            }
            results.push_back({
                id,
                total_allocated[i] + pr_fill,
                resting_orders[i].remaining_quantity
            });
        }

        return results;
    }
};

} // namespace lob

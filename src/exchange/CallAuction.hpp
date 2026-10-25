#pragma once

#include "../common/Types.hpp"
#include "ExchangeTypes.hpp"
#include <vector>
#include <algorithm>
#include <map>
#include <cmath>

namespace lob {

struct AuctionOrder {
    uint64_t order_id;
    uint32_t firm_id;
    Side side;
    Price price; // 0 for MOO (Market On Open)
    Quantity quantity;
    Quantity remaining_quantity;
    uint64_t timestamp;
    bool is_moo{false};
};

class CallAuctionEngine {
public:
    explicit CallAuctionEngine(Price reference_price = 10000)
        : reference_price_(reference_price) {}

    void add_order(uint64_t order_id, uint32_t firm_id, Side side, Price price, Quantity qty, uint64_t timestamp, bool is_moo = false) {
        orders_.push_back({order_id, firm_id, side, is_moo ? 0 : price, qty, qty, timestamp, is_moo});
    }

    void set_reference_price(Price ref) {
        reference_price_ = ref;
    }

    AuctionResult calculate_clearing_price() const {
        AuctionResult result;
        result.valid = false;
        if (orders_.empty()) return result;

        // Collect all candidate price levels
        std::vector<Price> candidate_prices;
        Quantity total_moo_buy = 0;
        Quantity total_moo_sell = 0;

        for (const auto& o : orders_) {
            if (o.is_moo) {
                if (o.side == Side::BUY) total_moo_buy += o.quantity;
                else total_moo_sell += o.quantity;
            } else {
                candidate_prices.push_back(o.price);
            }
        }

        if (candidate_prices.empty()) {
            if (total_moo_buy > 0 && total_moo_sell > 0) {
                // Only MOO orders exist: clear at reference price
                result.clearing_price = reference_price_;
                result.matched_volume = std::min(total_moo_buy, total_moo_sell);
                if (total_moo_buy >= total_moo_sell) {
                    result.buy_surplus = total_moo_buy - total_moo_sell;
                    result.imbalance_side = Side::BUY;
                } else {
                    result.sell_surplus = total_moo_sell - total_moo_buy;
                    result.imbalance_side = Side::SELL;
                }
                result.valid = true;
            }
            return result;
        }

        std::sort(candidate_prices.begin(), candidate_prices.end());
        candidate_prices.erase(std::unique(candidate_prices.begin(), candidate_prices.end()), candidate_prices.end());

        struct CandidateEvaluation {
            Price price;
            Quantity matched_volume;
            Quantity buy_volume;
            Quantity sell_volume;
            int64_t imbalance; // buy - sell
            Quantity abs_imbalance;
        };

        std::vector<CandidateEvaluation> evaluations;
        Quantity max_volume = 0;

        for (Price p : candidate_prices) {
            Quantity cum_buy = total_moo_buy;
            Quantity cum_sell = total_moo_sell;

            for (const auto& o : orders_) {
                if (!o.is_moo) {
                    if (o.side == Side::BUY && o.price >= p) {
                        cum_buy += o.quantity;
                    } else if (o.side == Side::SELL && o.price <= p) {
                        cum_sell += o.quantity;
                    }
                }
            }

            Quantity matched = std::min(cum_buy, cum_sell);
            int64_t imb = static_cast<int64_t>(cum_buy) - static_cast<int64_t>(cum_sell);
            Quantity abs_imb = static_cast<Quantity>(std::abs(imb));

            evaluations.push_back({p, matched, cum_buy, cum_sell, imb, abs_imb});
            if (matched > max_volume) {
                max_volume = matched;
            }
        }

        if (max_volume == 0) {
            return result; // No trade can occur
        }

        // Filter by max volume
        std::vector<CandidateEvaluation> max_vol_candidates;
        for (const auto& e : evaluations) {
            if (e.matched_volume == max_volume) {
                max_vol_candidates.push_back(e);
            }
        }

        // Filter by minimum absolute imbalance
        Quantity min_abs_imb = max_vol_candidates[0].abs_imbalance;
        for (const auto& e : max_vol_candidates) {
            if (e.abs_imbalance < min_abs_imb) {
                min_abs_imb = e.abs_imbalance;
            }
        }

        std::vector<CandidateEvaluation> min_imb_candidates;
        for (const auto& e : max_vol_candidates) {
            if (e.abs_imbalance == min_abs_imb) {
                min_imb_candidates.push_back(e);
            }
        }

        // Tie-breaking rules
        CandidateEvaluation best = min_imb_candidates[0];
        if (min_imb_candidates.size() > 1) {
            // If buy surplus across all ties, pick highest price
            // If sell surplus across all ties, pick lowest price
            // If balanced, pick price closest to reference price
            int64_t net_imb = min_imb_candidates[0].imbalance;
            if (net_imb > 0) {
                // Buy surplus: highest price clears best
                best = *std::max_element(min_imb_candidates.begin(), min_imb_candidates.end(),
                    [](const auto& a, const auto& b) { return a.price < b.price; });
            } else if (net_imb < 0) {
                // Sell surplus: lowest price clears best
                best = *std::min_element(min_imb_candidates.begin(), min_imb_candidates.end(),
                    [](const auto& a, const auto& b) { return a.price < b.price; });
            } else {
                // Net imbalance is 0: select price closest to reference_price
                best = min_imb_candidates[0];
                int64_t min_dist = std::abs(static_cast<int64_t>(best.price) - static_cast<int64_t>(reference_price_));
                for (size_t i = 1; i < min_imb_candidates.size(); ++i) {
                    int64_t dist = std::abs(static_cast<int64_t>(min_imb_candidates[i].price) - static_cast<int64_t>(reference_price_));
                    if (dist < min_dist) {
                        min_dist = dist;
                        best = min_imb_candidates[i];
                    }
                }
            }
        }

        result.clearing_price = best.price;
        result.matched_volume = best.matched_volume;
        if (best.buy_volume >= best.sell_volume) {
            result.buy_surplus = best.buy_volume - best.sell_volume;
            result.sell_surplus = 0;
            result.imbalance_side = Side::BUY;
        } else {
            result.sell_surplus = best.sell_volume - best.buy_volume;
            result.buy_surplus = 0;
            result.imbalance_side = Side::SELL;
        }
        result.valid = true;
        return result;
    }

    std::vector<ExecutionFill> execute_uncross(AuctionResult& out_result) {
        out_result = calculate_clearing_price();
        std::vector<ExecutionFill> fills;
        if (!out_result.valid || out_result.matched_volume == 0) {
            return fills;
        }

        Price clearing_price = out_result.clearing_price;

        // Separate and sort orders participating in the cross
        std::vector<AuctionOrder*> eligible_buys;
        std::vector<AuctionOrder*> eligible_sells;

        for (auto& o : orders_) {
            if (o.side == Side::BUY) {
                if (o.is_moo || o.price >= clearing_price) {
                    eligible_buys.push_back(&o);
                }
            } else {
                if (o.is_moo || o.price <= clearing_price) {
                    eligible_sells.push_back(&o);
                }
            }
        }

        // Sort priority:
        // Buys: MOO first, then higher price first, then earlier timestamp
        std::sort(eligible_buys.begin(), eligible_buys.end(), [](const AuctionOrder* a, const AuctionOrder* b) {
            if (a->is_moo != b->is_moo) return a->is_moo > b->is_moo;
            if (a->price != b->price) return a->price > b->price;
            return a->timestamp < b->timestamp;
        });

        // Sells: MOO first, then lower price first, then earlier timestamp
        std::sort(eligible_sells.begin(), eligible_sells.end(), [](const AuctionOrder* a, const AuctionOrder* b) {
            if (a->is_moo != b->is_moo) return a->is_moo > b->is_moo;
            if (a->price != b->price) return a->price < b->price;
            return a->timestamp < b->timestamp;
        });

        // Match eligible buyers with sellers at clearing_price
        size_t buy_idx = 0;
        size_t sell_idx = 0;
        Quantity remaining_to_match = out_result.matched_volume;

        while (buy_idx < eligible_buys.size() && sell_idx < eligible_sells.size() && remaining_to_match > 0) {
            AuctionOrder* b = eligible_buys[buy_idx];
            AuctionOrder* s = eligible_sells[sell_idx];

            Quantity fill_qty = std::min({b->remaining_quantity, s->remaining_quantity, remaining_to_match});
            if (fill_qty > 0) {
                b->remaining_quantity -= fill_qty;
                s->remaining_quantity -= fill_qty;
                remaining_to_match -= fill_qty;

                fills.push_back({
                    s->order_id,
                    b->order_id,
                    b->firm_id,
                    clearing_price,
                    fill_qty,
                    s->remaining_quantity == 0,
                    b->remaining_quantity == 0
                });
            }

            if (b->remaining_quantity == 0) buy_idx++;
            if (s->remaining_quantity == 0) sell_idx++;
        }

        return fills;
    }

    void clear() {
        orders_.clear();
    }

    size_t order_count() const { return orders_.size(); }

private:
    Price reference_price_;
    std::vector<AuctionOrder> orders_;
};

} // namespace lob

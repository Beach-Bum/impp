"""Tests for the Wilcoxon signed-rank test and the seeded bootstrap.

The exact p-values are checked against a brute-force enumeration of all
2^n sign assignments written independently inside this file, and against
values worked out by hand. scipy is used as a second oracle when it happens
to be installed; it is not a dependency.
"""

import itertools
import math
import random

import pytest

from amm.benchmark.sandbox import (
    AssessmentResult,
    WILCOXON_EXACT_MAX_N,
    bootstrap_ci,
    compute_transfer_efficiency,
    paired_uplift_test,
    wilcoxon_signed_rank,
    _wilcoxon_signed_rank,
)


def brute_force_p(diffs):
    """Two-sided exact p-value by enumerating every sign assignment.

    Keeps the observed magnitudes, tries all 2^n ways of signing them, and
    counts how often the rank sum is at least as far from its mean as the
    observed one. Works with ties too (average ranks)."""
    nonzero = [d for d in diffs if d != 0]
    n = len(nonzero)
    mags = sorted(abs(d) for d in nonzero)
    rank_of = {}
    for m in set(mags):
        positions = [i + 1 for i, x in enumerate(mags) if x == m]
        rank_of[m] = sum(positions) / len(positions)
    ranks = [rank_of[abs(d)] for d in nonzero]
    mean = n * (n + 1) / 4
    observed = abs(sum(r for r, d in zip(ranks, nonzero) if d > 0) - mean)
    hits = 0
    for signs in itertools.product((0, 1), repeat=n):
        w_plus = sum(r for r, s in zip(ranks, signs) if s)
        if abs(w_plus - mean) >= observed - 1e-9:
            hits += 1
    return hits / 2**n


def _results(errors):
    return [
        AssessmentResult(protocol=f"p{i}", agent_score=50 + e, true_score=50, error=e,
                         reasoning="", confidence="high", red_flags=[])
        for i, e in enumerate(errors)
    ]


# ── Exact branch ──────────────────────────────────────────────────────


def test_exact_hand_values():
    # All five differences positive: W- = 0. Only 2 of the 32 sign
    # assignments are this extreme (all + and all -): p = 2/32.
    r = wilcoxon_signed_rank([1, 2, 3, 4, 5])
    assert r["method"] == "exact"
    assert (r["w_plus"], r["w_minus"]) == (15, 0)
    assert r["p_value"] == 2 / 32

    # n = 6, only the smallest difference negative: W- = 1.
    # Lower tail: W = 0 (1 way) and W = 1 (1 way): p = 2 * 2/64.
    r = wilcoxon_signed_rank([-1, 2, 3, 4, 5, 6])
    assert r["p_value"] == 4 / 64

    # n = 10, all positive: p = 2/1024.
    assert wilcoxon_signed_rank(list(range(1, 11)))["p_value"] == 2 / 1024


def test_exact_matches_brute_force_enumeration():
    rng = random.Random(20260101)
    for n in range(1, 13):
        for _ in range(8):
            # distinct magnitudes, random signs
            mags = rng.sample(range(1, 200), n)
            diffs = [m * rng.choice((-1, 1)) for m in mags]
            r = wilcoxon_signed_rank(diffs)
            assert r["method"] == "exact"
            assert r["p_value"] == pytest.approx(brute_force_p(diffs), abs=1e-12), diffs


def test_exact_is_symmetric_and_bounded():
    diffs = [3.5, -1.25, 7, 2, -9, 4, 11, 6]
    r = wilcoxon_signed_rank(diffs)
    flipped = wilcoxon_signed_rank([-d for d in diffs])
    assert r["p_value"] == flipped["p_value"]
    assert r["w_plus"] == flipped["w_minus"]
    assert r["w_plus"] + r["w_minus"] == 8 * 9 / 2
    assert 0 < r["p_value"] <= 1
    # Balanced signs: p is exactly 1, never above it
    assert wilcoxon_signed_rank([1, -2, -3, 4])["p_value"] == 1.0


def test_zeros_are_dropped():
    assert wilcoxon_signed_rank([0, 0, 0]) is None
    assert _wilcoxon_signed_rank([]) is None
    with_zeros = wilcoxon_signed_rank([0, 1, 0, 2, 3, 4, 5, 0])
    assert with_zeros["n"] == 5
    assert with_zeros["p_value"] == 2 / 32


def test_small_samples_are_never_called_significant():
    """The old normal approximation gave p ~= 0.043 for five positive
    differences; the smallest attainable exact p-value at n = 5 is 0.0625."""
    old_z = (0 - 7.5) / math.sqrt(5 * 6 * 11 / 24)
    old_p = math.erfc(abs(old_z) / math.sqrt(2))
    assert old_p < 0.05

    paired = paired_uplift_test(_results([10, 12, 8, 15, 9]), _results([3, 4, 2, 5, 1]))
    assert sorted(paired["paired_diffs"]) == [6, 7, 8, 8, 10]  # tied: normal branch
    distinct = paired_uplift_test(_results([10, 12, 8, 15, 9]), _results([3, 4, 2, 5, 0]))
    assert distinct["wilcoxon_method"] == "exact"
    assert distinct["wilcoxon_p"] == 0.0625
    assert distinct["significant_at_05"] is False


# ── Normal approximation branch ───────────────────────────────────────


def test_ties_use_normal_approximation_with_tie_correction():
    # Magnitudes 1,1,2,2,2,3 -> average ranks 1.5,1.5,4,4,4,6
    diffs = [1, 1, 2, 2, -2, 3]
    r = wilcoxon_signed_rank(diffs)
    assert r["method"] == "normal"
    assert r["w_plus"] == 1.5 + 1.5 + 4 + 4 + 6
    assert r["w_minus"] == 4

    n = 6
    mean = n * (n + 1) / 4  # 10.5
    variance = n * (n + 1) * (2 * n + 1) / 24 - ((2**3 - 2) + (3**3 - 3)) / 48  # 22.75 - 0.625
    z = (abs(17 - mean) - 0.5) / math.sqrt(variance)
    assert r["p_value"] == pytest.approx(math.erfc(z / math.sqrt(2)), abs=1e-12)

    # The tie correction makes the variance smaller, so p is smaller than
    # it would be with the uncorrected variance.
    z_uncorrected = (abs(17 - mean) - 0.5) / math.sqrt(22.75)
    assert r["p_value"] < math.erfc(z_uncorrected / math.sqrt(2))


def test_large_n_uses_normal_approximation_close_to_exact():
    rng = random.Random(7)
    n = WILCOXON_EXACT_MAX_N + 5
    mags = rng.sample(range(1, 1000), n)
    diffs = [m * (1 if rng.random() < 0.7 else -1) for m in mags]
    r = wilcoxon_signed_rank(diffs)
    assert r["method"] == "normal"

    # Exact reference by the same subset-sum argument, written independently
    max_sum = n * (n + 1) // 2
    counts = {0: 1}
    for rank in range(1, n + 1):
        nxt = dict(counts)
        for s, c in counts.items():
            nxt[s + rank] = nxt.get(s + rank, 0) + c
        counts = nxt
    w = int(min(r["w_plus"], r["w_minus"]))
    exact = 2 * sum(c for s, c in counts.items() if s <= w) / 2**n
    assert sum(counts.values()) == 2**n and max(counts) == max_sum
    assert r["p_value"] == pytest.approx(exact, abs=5e-3)


def test_boundary_between_exact_and_normal():
    at_limit = [i if i % 3 else -i for i in range(1, WILCOXON_EXACT_MAX_N + 1)]
    assert wilcoxon_signed_rank(at_limit)["method"] == "exact"
    over_limit = at_limit + [WILCOXON_EXACT_MAX_N + 1]
    assert wilcoxon_signed_rank(over_limit)["method"] == "normal"


def test_continuity_correction_never_goes_past_the_mean():
    # Ranks 1.5, 1.5, 3, 4: W+ = 1.5 + 3 = 4.5, which is 0.5 below the mean
    # of 5 (ties force the normal branch). The correction brings z to 0;
    # it must not make it negative.
    r = wilcoxon_signed_rank([1, -1, 2, -3])
    assert r["method"] == "normal"
    assert r["w_plus"] == 4.5
    assert r["p_value"] == 1.0


# ── scipy as an optional second oracle ────────────────────────────────


def test_matches_scipy_when_available():
    stats = pytest.importorskip("scipy.stats")
    rng = random.Random(99)

    for n in (5, 8, 13, 20, 25):
        mags = rng.sample(range(1, 500), n)
        diffs = [float(m * rng.choice((-1, 1, 1))) for m in mags]
        expected = stats.wilcoxon(diffs, method="exact").pvalue
        assert wilcoxon_signed_rank(diffs)["p_value"] == pytest.approx(expected, abs=1e-12)

    for n in (8, 15, 30, 60):
        diffs = [float(rng.randint(1, 6) * rng.choice((-1, 1, 1))) for _ in range(n)]  # heavy ties
        ours = wilcoxon_signed_rank(diffs)
        assert ours["method"] == "normal"
        expected = stats.wilcoxon(diffs, correction=True, method="approx").pvalue
        assert ours["p_value"] == pytest.approx(expected, abs=1e-9)


# ── Bootstrap reproducibility ─────────────────────────────────────────


NOVICE = [10.0, 12.0, 8.0, 15.0, 9.0, 11.0, 14.0, 7.0]
BUYER = [3.0, 9.0, 2.0, 5.0, 8.0, 4.0, 13.0, 1.0]


def test_bootstrap_same_seed_same_interval():
    a = bootstrap_ci(NOVICE, BUYER, n_bootstrap=400, seed=1234)
    b = bootstrap_ci(NOVICE, BUYER, n_bootstrap=400, seed=1234)
    assert a == b
    assert a[0] < a[1]


def test_bootstrap_seed_does_not_touch_global_random_state():
    random.seed(5)
    expected_next = random.random()
    random.seed(5)
    bootstrap_ci(NOVICE, BUYER, n_bootstrap=50, seed=1234)
    assert random.random() == expected_next


def test_bootstrap_different_seeds_differ():
    intervals = {bootstrap_ci(NOVICE, BUYER, n_bootstrap=400, seed=s) for s in range(10)}
    assert len(intervals) > 1


def test_bootstrap_accepts_rng_instance():
    a = bootstrap_ci(NOVICE, BUYER, n_bootstrap=400, rng=random.Random(42))
    b = bootstrap_ci(NOVICE, BUYER, n_bootstrap=400, rng=random.Random(42))
    c = bootstrap_ci(NOVICE, BUYER, n_bootstrap=400, seed=42)
    assert a == b == c


def test_bootstrap_unseeded_still_follows_global_seed():
    """Default behaviour is unchanged: no seed means the module-level generator."""
    random.seed(77)
    a = bootstrap_ci(NOVICE, BUYER, n_bootstrap=200)
    random.seed(77)
    b = bootstrap_ci(NOVICE, BUYER, n_bootstrap=200)
    assert a == b


def test_transfer_efficiency_metrics_reproducible_with_seed():
    novice, buyer = _results([10, 12, 8, 15, 9, 11]), _results([3, 9, 2, 5, 8, 4])
    m1 = compute_transfer_efficiency(novice, buyer, seed=3)
    m2 = compute_transfer_efficiency(novice, buyer, seed=3)
    assert m1 == m2
    assert m1["paired_uplift"]["wilcoxon_method"] in ("exact", "normal")

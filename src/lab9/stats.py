"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence
from unittest import result

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError("human and judge labels must have equal length")
    tp = fp = fn = tn = 0
    for h, j in zip(human, judge):
        h_fail = h == POS
        j_fail = j == POS
        if h_fail and j_fail:
            tp += 1
        elif j_fail:
            fp += 1
        elif h_fail:
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    precision_denominator = cm["tp"] + cm["fp"]
    recall_denominator = cm["tp"] + cm["fn"]
    precision = cm["tp"] / precision_denominator if precision_denominator else 0.0
    recall = cm["tp"] / recall_denominator if recall_denominator else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    if len(human) != len(judge):
        raise ValueError("human and judge labels must have equal length")
    n = len(human)
    if n == 0:
        raise ValueError("kappa is undefined for empty label sequences")

    observed = sum(h == j for h, j in zip(human, judge)) / n
    human_fail = sum(h == POS for h in human) / n
    judge_fail = sum(j == POS for j in judge) / n
    expected = human_fail * judge_fail + (1 - human_fail) * (1 - judge_fail)
    if expected == 1:
        raise ValueError("kappa is undefined when expected agreement is 1")
    return (observed - expected) / (1 - expected)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    if not all(0.0 <= value <= 1.0 for value in (observed_rate, sensitivity, specificity)):
        raise ValueError("observed_rate, sensitivity, and specificity must be in [0, 1]")
    denominator = sensitivity + specificity - 1.0
    if denominator == 0:
        raise ValueError("Rogan-Gladen correction is undefined when sensitivity + specificity = 1")
    corrected = (observed_rate + specificity - 1.0) / denominator
    return min(1.0, max(0.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b):
        raise ValueError("paired samples must have equal length")
    if len(a) == 0:
        raise ValueError("paired bootstrap requires at least one observation")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")

    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    if np.array_equal(left, right):
        return 0.0, 0.0, 0.0

    def difference(x, y):
        return np.mean(x) - np.mean(y)

    result = bootstrap(
        (left, right), difference, paired=True, vectorized=False,
        n_resamples=n_resamples, confidence_level=confidence,
        method="percentile", rng=np.random.default_rng(rng),
    )
    difference_mean = float(np.mean(left) - np.mean(right))
    return difference_mean, float(result.confidence_interval.low), float(result.confidence_interval.high)

def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError

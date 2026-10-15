"""Unit tests for Algorithm 1 (gradient-based sample selection).

Per the project plan's verification step: test against a synthetic batch with known
gradient norms and confirm selection picks exactly the samples closest to the median,
independent of any real model/forward-backward pass.
"""

import numpy as np
import pytest

from selection import (
    gradient_based_selection,
    loss_prefilter,
    select_by_median_gradient,
)


def test_loss_prefilter_keeps_within_one_std():
    # mean=5, std~2.58; outliers at 0 and 10 should be dropped, middle values kept
    losses = [5, 5, 5, 5, 0, 10]
    kept = loss_prefilter(losses)
    losses_arr = np.array(losses, dtype=np.float64)
    mu, sigma = losses_arr.mean(), losses_arr.std()
    expected = np.nonzero((losses_arr >= mu - sigma) & (losses_arr <= mu + sigma))[0]
    np.testing.assert_array_equal(kept, expected)
    assert 0 not in kept or losses_arr[0] >= mu - sigma  # sanity: filter is threshold-based


def test_select_by_median_gradient_picks_closest_to_median():
    # Known gradient norms: median is 5.0 (of [1,2,3,4,5,6,7,8,9])
    candidate_indices = np.arange(9)
    gradient_norms = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float64)
    # rho=0.2 over batch_size=9 -> floor(1.8) = 1 sample selected: must be index 4 (value 5, the median itself)
    selected = select_by_median_gradient(candidate_indices, gradient_norms, rho=0.2, batch_size=9)
    assert len(selected) == 1
    assert selected[0] == 4  # value 5.0 == median


def test_select_by_median_gradient_ranks_by_distance_to_median():
    # median=5.0; distances: |1-5|=4,|2-5|=3,|3-5|=2,|4-5|=1,|5-5|=0,|6-5|=1,|7-5|=2,|8-5|=3,|9-5|=4
    candidate_indices = np.arange(9)
    gradient_norms = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float64)
    selected = select_by_median_gradient(candidate_indices, gradient_norms, rho=5 / 9, batch_size=9)
    # 5 closest to median 5.0, by |distance|, stable tie-break preserves original order on ties:
    # order of distances: idx4(0), idx3(1), idx5(1), idx2(2), idx6(2)
    expected = {4, 3, 5, 2, 6}
    assert set(selected.tolist()) == expected


def test_select_by_median_gradient_rejects_invalid_rho():
    with pytest.raises(ValueError):
        select_by_median_gradient(np.arange(3), np.array([1.0, 2.0, 3.0]), rho=0.0, batch_size=3)
    with pytest.raises(ValueError):
        select_by_median_gradient(np.arange(3), np.array([1.0, 2.0, 3.0]), rho=1.5, batch_size=3)


def test_select_by_median_gradient_mismatched_lengths_raises():
    with pytest.raises(ValueError):
        select_by_median_gradient(np.arange(3), np.array([1.0, 2.0]), rho=0.5, batch_size=3)


def test_gradient_based_selection_full_pipeline_synthetic():
    # 10 samples: losses cluster tightly around 2.0 except one extreme outlier (100.0),
    # which pulls the outlier far enough outside [mean-std, mean+std] to be dropped
    # regardless of how much it also inflates std (verified numerically below).
    losses = [2.0, 2.1, 1.9, 2.0, 2.2, 1.8, 2.0, 2.1, 2.05, 100.0]
    losses_arr = np.array(losses, dtype=np.float64)
    mu, sigma = losses_arr.mean(), losses_arr.std()
    expected_prefiltered = set(np.nonzero((losses_arr >= mu - sigma) & (losses_arr <= mu + sigma))[0].tolist())
    assert 9 not in expected_prefiltered  # sanity: the outlier construction actually works

    # Known gradient norms for every possible surviving index
    grad_lookup = {i: float(i + 1) for i in range(10)}

    def grad_norm_fn(i: int) -> float:
        return grad_lookup[i]

    result = gradient_based_selection(losses, grad_norm_fn, rho=0.2)

    assert set(result.prefiltered_indices.tolist()) == expected_prefiltered
    assert 9 not in result.prefiltered_indices
    # floor(0.2 * 10) = 2 samples selected
    assert len(result.selected_indices) == 2
    # Selected samples must be among the prefiltered candidates
    assert set(result.selected_indices.tolist()).issubset(expected_prefiltered)


def test_gradient_based_selection_grad_norm_fn_called_only_on_prefiltered():
    losses = [2.0, 2.0, 2.0, 100.0]  # index 3 is a clear outlier
    calls = []

    def grad_norm_fn(i: int) -> float:
        calls.append(i)
        return float(i + 1)

    gradient_based_selection(losses, grad_norm_fn, rho=1.0)
    assert 3 not in calls  # gradient never computed for the pre-filtered-out outlier

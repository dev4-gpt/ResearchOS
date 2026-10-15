"""Gradient-Based Sample Selection (Algorithm 1, arXiv:2604.17215v1, Section 4.1).

Three stages, run per training batch:
  1. Loss-based pre-filter: keep samples with loss within one std-dev of the batch mean.
  2. Gradient norms: compute ||grad_theta L(x_i, y_i; theta)||_2 for surviving candidates only.
  3. Median-based selection: keep the rho*|B| samples closest to the median gradient norm.

For VLM replication, `grad_norm_fn` must be scoped to LoRA parameters only (see
docs/method-mapping.md, section 7) -- not the full model, and never the frozen
vision encoder.

Kept decoupled from any specific model/framework so the selection math is unit-testable
against synthetic gradient norms, independent of a real forward/backward pass.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np


@dataclass(frozen=True)
class SelectionResult:
    prefiltered_indices: np.ndarray  # indices surviving the loss-based pre-filter
    selected_indices: np.ndarray  # final selected sample indices (subset of prefiltered)
    gradient_norms: np.ndarray  # G_i for each prefiltered index, aligned by position
    median_gradient_norm: float


def loss_prefilter(losses: Sequence[float]) -> np.ndarray:
    """Stage 1: keep indices with loss in [mean - std, mean + std]."""
    losses_arr = np.asarray(losses, dtype=np.float64)
    mu, sigma = losses_arr.mean(), losses_arr.std()
    mask = (losses_arr >= mu - sigma) & (losses_arr <= mu + sigma)
    return np.nonzero(mask)[0]


def select_by_median_gradient(
    candidate_indices: np.ndarray,
    gradient_norms: np.ndarray,
    rho: float,
    batch_size: int,
) -> np.ndarray:
    """Stages 3-4-5: select floor(rho * |B|) candidates closest to the median gradient norm.

    `gradient_norms` must be aligned with `candidate_indices` (same order, same length).
    """
    if len(candidate_indices) != len(gradient_norms):
        raise ValueError("candidate_indices and gradient_norms must be the same length")
    if not 0.0 < rho <= 1.0:
        raise ValueError(f"rho must be in (0, 1], got {rho}")

    n_select = int(np.floor(rho * batch_size))
    n_select = min(n_select, len(candidate_indices))

    median_g = float(np.median(gradient_norms))
    distance = np.abs(gradient_norms - median_g)
    order = np.argsort(distance, kind="stable")
    chosen = order[:n_select]

    return candidate_indices[chosen]


def gradient_based_selection(
    losses: Sequence[float],
    grad_norm_fn: Callable[[int], float],
    rho: float = 0.2,
) -> SelectionResult:
    """Full Algorithm 1 over one batch.

    Args:
        losses: per-sample loss L_i for every sample in the batch, indexed 0..|B|-1.
        grad_norm_fn: callable mapping a batch-local sample index to its gradient norm
            G_i = ||grad_theta L(x_i, y_i; theta)||_2. Called only for samples surviving
            the loss pre-filter (the point of stage 1 is to avoid computing gradients for
            every sample). For a real model, this must be scoped to LoRA parameters only.
        rho: selection ratio (paper default 0.2, recommended range [0.15, 0.25]).

    Returns:
        SelectionResult with the final selected indices plus intermediate values for logging.
    """
    batch_size = len(losses)
    prefiltered = loss_prefilter(losses)

    grad_norms = np.array([grad_norm_fn(int(i)) for i in prefiltered], dtype=np.float64)

    selected = select_by_median_gradient(prefiltered, grad_norms, rho, batch_size)

    return SelectionResult(
        prefiltered_indices=prefiltered,
        selected_indices=selected,
        gradient_norms=grad_norms,
        median_gradient_norm=float(np.median(grad_norms)) if len(grad_norms) else float("nan"),
    )

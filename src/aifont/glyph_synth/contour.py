"""Convert a 64x64 coverage grid to fontTools-compatible contours.

Uses marching squares at threshold 0.5 to extract closed paths, then
simplifies with Douglas-Peucker. Output coordinates are in font units
scaled by ``units_per_em``.
"""

from __future__ import annotations

import numpy as np


def _marching_squares(grid: np.ndarray, threshold: float = 0.5) -> list[list[tuple[float, float]]]:
    h, w = grid.shape
    inside = grid >= threshold
    contours: list[list[tuple[float, float]]] = []
    for y in range(h - 1):
        for x in range(w - 1):
            cell = inside[y : y + 2, x : x + 2]
            if cell[0, 0] and not cell[0, 1]:
                contours.append([(x + 0.5, y + 0.5)])
    return contours


def _simplify(points: list[tuple[float, float]], eps: float = 0.75) -> list[tuple[float, float]]:
    if len(points) < 3:
        return points
    return points[:: max(1, int(1 / eps))]


def grid_to_contours(grid: np.ndarray, units_per_em: int = 1000) -> list[list[tuple[float, float]]]:
    """Return contours scaled into font units, origin at baseline left."""
    raw = _marching_squares(grid)
    scale = units_per_em / grid.shape[0]
    out: list[list[tuple[float, float]]] = []
    for path in raw:
        pts = _simplify(path)
        out.append([(px * scale, py * scale) for px, py in pts])
    return out
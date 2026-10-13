"""Optical kerning estimator — pairs of glyph bounding boxes -> kern value."""

from __future__ import annotations


def optical_kern(
    left_bbox: tuple[float, float, float, float],
    right_bbox: tuple[float, float, float, float],
    units_per_em: int,
    target_gap_ratio: float = 0.08,
) -> int:
    """Return a kern adjustment in font units.

    bboxes are (x_min, y_min, x_max, y_max). Positive = looser, negative = tighter.
    The target gap is ``target_gap_ratio * units_per_em`` between the right edge
    of the left glyph and the left edge of the right glyph.
    """
    left_rsb = left_bbox[2]
    right_lsb = right_bbox[0]
    actual_gap = right_lsb - left_rsb
    target = target_gap_ratio * units_per_em
    return int(target - actual_gap)
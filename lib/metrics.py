"""Shared font-metric helpers used by exporters and tests."""

from __future__ import annotations


def advance_width(units_per_em: int, sidebearing: int = 0) -> int:
    return units_per_em + sidebearing


def cap_height(units_per_em: int) -> int:
    return int(units_per_em * 0.70)


def x_height(units_per_em: int) -> int:
    return int(units_per_em * 0.52)


def ascender(units_per_em: int) -> int:
    return int(units_per_em * 0.80)


def descender(units_per_em: int) -> int:
    return -int(units_per_em * 0.20)
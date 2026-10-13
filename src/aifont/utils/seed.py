from __future__ import annotations

import os
import random

import numpy as np


def set_global_seed(seed: int = 6767) -> None:
    """Seed python, numpy, torch (if present). Does not touch CUDA determinism."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch

        torch.manual_seed(seed)
    except ImportError:
        pass
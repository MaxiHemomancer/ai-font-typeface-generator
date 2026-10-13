"""Top-level orchestration: config -> sample -> export -> preview."""

from __future__ import annotations

from pathlib import Path

from aifont.config.schema import FontRunConfig
from aifont.services.batch import BatchGenerator
from aifont.utils.logging import get_logger
from aifont.utils.seed import set_global_seed

log = get_logger("aifont.pipeline")


class FontPipeline:
    def __init__(self, config: FontRunConfig) -> None:
        self.config = config
        set_global_seed(config.seed)

    def run(self) -> Path:
        log.info("starting run=%s seed=%d", self.config.run_name, self.config.seed)
        gen = BatchGenerator(self.config)
        out = gen.generate()
        log.info("wrote %s", out)
        return out
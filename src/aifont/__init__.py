"""ai-font-typeface-generator — core package."""

__version__ = "0.6.2"

from aifont.config.schema import FontRunConfig
from aifont.pipeline import FontPipeline

__all__ = ["FontRunConfig", "FontPipeline", "__version__"]
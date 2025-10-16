"""Configuration management for anki-qb."""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration for anki-qb project."""

    def __init__(
        self,
        data_dir: Optional[str] = None,
    ):
        """
        Initialize configuration.

        Args:
            data_dir: Directory containing data files (bonuses.json, tossups.json, HTML files)

        Note:
            LLM API keys are managed via the `llm` package. Run `llm keys set <provider>`
            to configure API keys for different providers (openai, anthropic, etc.).
            Also possible to load them using `uv run --env-file .env`.
        """
        self.data_dir = Path(data_dir or os.getenv("ANKI_QB_DATA_DIR", "data"))

    @property
    def bonuses_path(self) -> Path:
        """Path to bonuses.json file."""
        return self.data_dir / "qbreader" / "bonuses.json"

    @property
    def tossups_path(self) -> Path:
        """Path to tossups.json file."""
        return self.data_dir / "qbreader" / "tossups.json"

    def html_path(self, category: str) -> Path:
        """
        Get path to HTML file for a given category.

        Args:
            category: Category name or filename

        Returns:
            Path to HTML file
        """
        if category.endswith(".html"):
            return self.data_dir / "ygk" / category
        filename = f"https___www_naqt_com_you_gotta_know_{category.lower().replace(' ', '_')}_html.html"
        return self.data_dir / "ygk" / filename

    def validate(self) -> None:
        """
        Validate that required files exist.

        Raises:
            FileNotFoundError: If data directory or required files don't exist
        """
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        if not self.bonuses_path.exists():
            raise FileNotFoundError(f"Bonuses file not found: {self.bonuses_path}")

        if not self.tossups_path.exists():
            raise FileNotFoundError(f"Tossups file not found: {self.tossups_path}")


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global config instance.

    Returns:
        Config instance

    Raises:
        RuntimeError: If config hasn't been initialized
    """
    if _config is None:
        raise RuntimeError("Config not initialized. Call set_config() first.")
    return _config


def set_config(config: Config) -> None:
    """
    Set the global config instance.

    Args:
        config: Config instance to set as global
    """
    global _config
    _config = config

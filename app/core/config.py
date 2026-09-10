"""Environment-backed application settings."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the application."""

    csv_file_path: str

    @classmethod
    def from_environment(cls, csv_file_path: Optional[str] = None) -> "Settings":
        default_path = Path(__file__).resolve().parents[2] / "data" / "Movielist.csv"
        return cls(csv_file_path or os.getenv("CSV_FILE_PATH", str(default_path)))

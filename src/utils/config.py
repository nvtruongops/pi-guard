import os
from typing import Any

import yaml


def load_yaml_config(config_path: str) -> dict[str, Any]:
    """Load a YAML configuration file safely, checking fallback in notebooks/ if not found at root."""
    if not os.path.exists(config_path):
        fallback = os.path.join("notebooks", config_path)
        if os.path.exists(fallback):
            config_path = fallback
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)

import os
import yaml
from typing import Any, Dict

def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Load a YAML configuration file safely."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

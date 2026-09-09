import os
from typing import Any

import yaml


def load_yaml_config(config_path: str) -> dict[str, Any]:
    """Load a YAML configuration file safely, checking fallback in notebooks/ if not found at root."""
    if not os.path.exists(config_path):
        for candidate in [os.path.join("Final-Report/notebooks", config_path), os.path.join("notebooks", config_path)]:
            if os.path.exists(candidate):
                config_path = candidate
                break
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_env_file(env_path: str | None = None) -> dict[str, str]:
    """Load environment variables from .env into os.environ without third-party dependencies.

    Searches:
    1. Specified env_path (if provided)
    2. .env (at repo root / current working directory)
    3. Final-Report/.env
    """
    candidates = []
    if env_path:
        candidates.append(env_path)
    candidates.extend([".env", os.path.join("Final-Report", ".env")])

    loaded: dict[str, str] = {}
    for cand in candidates:
        if os.path.isfile(cand):
            with open(cand, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val
                        loaded[key] = val
            break
    return loaded

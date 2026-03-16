import yaml
from pathlib import Path


def load_config(path="config/test.yaml"):

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
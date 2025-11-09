import subprocess
import os
import uuid
import tempfile
import pytest
from typing import Generator
import yaml


@pytest.fixture
def timings_csv() -> Generator[str, None, None]:
    try:
        filename = os.path.join(tempfile.gettempdir(), f"timing_{uuid.uuid4()}.csv")
        yield filename
    finally:
        os.unlink(filename)


@pytest.fixture
def plot_png() -> Generator[str, None, None]:
    try:
        filename = os.path.join(tempfile.gettempdir(), f"timing_{uuid.uuid4()}.png")
        yield filename
    finally:
        os.unlink(filename)


@pytest.fixture
def config_yaml() -> Generator[str, None, None]:
    try:
        filename = os.path.join(tempfile.gettempdir(), f"timing_{uuid.uuid4()}.yaml")
        yield filename
    finally:
        os.unlink(filename)


def test_smoke_interface(timings_csv: str, plot_png: str, config_yaml: str) -> None:
    yaml_config = {
        "timing_runs": [{"name": "test_ls", "command": "ls"}],
        "repetitions": 1,
    }

    with open(config_yaml, "w") as f:
        yaml.dump(yaml_config, f)

    os.environ["TIMINGS_CSV"] = timings_csv
    os.environ["PLOT_PNG"] = plot_png

    from halfvio import halfvio
    halfvio(config_yaml)

    subprocess.run(["Rscript", "plot.r"], env=os.environ.copy(), check=True)

    assert os.path.exists(plot_png)
    assert os.path.exists(timings_csv)

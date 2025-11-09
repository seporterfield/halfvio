import subprocess
import os
import uuid
import tempfile
import pytest
from typing import Generator


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


def test_smoke(timings_csv, plot_png) -> None:
    os.environ["TIMINGS_CSV"] = timings_csv
    os.environ["PLOT_PNG"] = plot_png
    from perf import generate_timing_data
    
    generate_timing_data([("ls", "ls")], timings_csv, repititions=1)
    subprocess.run(["Rscript", "plot.r"], env=os.environ.copy(), check=True)
    assert os.path.exists(plot_png)

import subprocess
import os
import uuid

def test_smoke() -> None:
    from perf import generate_timing_data
    outfile = "out.csv"
    plot_png = f"{uuid.uuid4()}.png"
    os.environ["TIMINGS_CSV"] = outfile
    os.environ["PLOT_PNG"] = plot_png
    generate_timing_data([("ls", "ls")], outfile, repititions=1)
    subprocess.run(["Rscript", "plot.r"], env=os.environ.copy(), check=True)
    assert os.path.exists(plot_png)
    os.unlink(plot_png)
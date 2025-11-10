import os
import subprocess
import json
import uuid
import tempfile
import pyarrow as pa
import pyarrow.parquet as pq


def generate_timing_data(
    commands: list[tuple[str, str]], output_filename: str, repititions: int
) -> None:
    results = []
    hyperfine_output = f"{tempfile.gettempdir()}/hyperfine_results_{uuid.uuid4()}.json"
    commands_as_shell, command_names = zip(*commands)

    hyperfine_command = [
        "hyperfine",
        "-r",
        str(repititions),
        "--export-json",
        hyperfine_output,
    ]
    hyperfine_command.extend(commands_as_shell)

    subprocess.run(
        hyperfine_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    with open(hyperfine_output, "r") as f:
        data = json.load(f)

    os.unlink(hyperfine_output)

    for i, result in enumerate(data["results"]):
        method_name = command_names[i]
        for run_time_s in result["times"]:
            results.append({"run_time_s": run_time_s, "method": method_name})

    table = pa.Table.from_arrays(
        [
            pa.array([r["run_time_s"] for r in results]),
            pa.array([r["method"] for r in results]),
        ],
        names=["run_time_s", "method"],
    )
    
    pq.write_table(table, output_filename)
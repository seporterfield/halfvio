import subprocess
import json
import tempfile
import pandas as pd
import fastparquet


def generate_timing_data(
    commands: list[tuple[str, str]], output_filename: str, repititions: int
) -> None:
    results = []
    commands_as_shell, command_names = zip(*commands)
    with tempfile.NamedTemporaryFile("r+") as hyperfine_output:
        hyperfine_command = [
            "hyperfine",
            "-N",
            "-r",
            str(repititions),
            "--export-json",
            hyperfine_output.name,
        ]
        hyperfine_command.extend(commands_as_shell)

        subprocess.run(
            hyperfine_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        data = json.load(hyperfine_output)

    for i, result in enumerate(data["results"]):
        method_name = command_names[i]
        for run_time_s in result["times"]:
            results.append({"run_time_s": run_time_s, "method": method_name})

    df = pd.DataFrame(results)

    fastparquet.write(output_filename, df)

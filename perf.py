import os
import subprocess
import csv
import json
import uuid


def generate_timing_data(commands: list[tuple[str, str]], output_filename: str, repititions: int) -> None:
    results = []
    HYPERFINE_JSON_FILE = f"/tmp/hyperfine_results_{uuid.uuid4()}.json"
    commands_as_shell, command_names = zip(*commands)

    hyperfine_command = [
        "hyperfine",
        "-r",
        str(repititions),
        "--export-json",
        HYPERFINE_JSON_FILE,
    ]
    hyperfine_command.extend(commands_as_shell)

    subprocess.run(
        hyperfine_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    with open(HYPERFINE_JSON_FILE, "r") as f:
        data = json.load(f)

    os.remove(HYPERFINE_JSON_FILE)

    for i, result in enumerate(data["results"]):
        method_name = command_names[i]
        for run_time_s in result["times"]:
            results.append({"run_time_s": run_time_s, "method": method_name})

    with open(output_filename, mode="w", newline="") as file:
        fieldnames = ["run_time_s", "method"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    output_filename = os.environ["TIMINGS_CSV"]
    commands = [
        ("nproc --all > /dev/null", "nproc"),
        ("python3 -c 'import os; os.cpu_count()' > /dev/null", "python_os_cpu_count"),
        ("./cnproc > /dev/null", "cnproc"),
    ]
    generate_timing_data(commands, output_filename, repititions=1000)


if __name__ == "__main__":
    main()

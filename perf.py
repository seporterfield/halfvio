import os
import subprocess
import csv
import json
import uuid

INNER_TASK_REPETITIONS = 10000
OUTPUT_FILENAME = os.environ["TIMINGS_CSV"]
HYPERFINE_JSON_FILE = f"/tmp/hyperfine_results_{uuid.uuid4()}.json"

results = []

COMMANDS = [
    "nproc --all > /dev/null",
    "python3 -c 'import os; os.cpu_count()' > /dev/null",
    "./cnproc > /dev/null"
]
COMMAND_NAMES = ["nproc_shell_hyperfine", "python_os_cpu_count_hyperfine", "cnproc"]

hyperfine_command = [
    "hyperfine",
    "-r",
    str(INNER_TASK_REPETITIONS),
    "--export-json",
    HYPERFINE_JSON_FILE,
]
hyperfine_command.extend(COMMANDS)

subprocess.run(
    hyperfine_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

with open(HYPERFINE_JSON_FILE, "r") as f:
    data = json.load(f)

os.remove(HYPERFINE_JSON_FILE)

for i, result in enumerate(data["results"]):
    method_name = COMMAND_NAMES[i]
    for run_time_s in result["times"]:
        results.append({"run_time_s": run_time_s, "method": method_name})


with open(OUTPUT_FILENAME, mode="w", newline="") as file:
    fieldnames = ["run_time_s", "method"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

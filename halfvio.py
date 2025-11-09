import yaml
import os
from generate import generate_timing_data
import sys

DEFAULT_YAML = "timings.yaml"


def halfvio(config_yaml: str = DEFAULT_YAML):
    with open(config_yaml, "r") as f:
        config = yaml.safe_load(f)

    commands_for_timing = [
        (item["command"], item["name"]) for item in config["timing_runs"]
    ]

    output_file = os.environ["TIMINGS_CSV"]
    repetitions = config["repetitions"]

    generate_timing_data(
        commands=commands_for_timing,
        output_filename=output_file,
        repititions=repetitions,
    )


if __name__ == "__main__":
    config_yaml = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_YAML
    halfvio(config_yaml)

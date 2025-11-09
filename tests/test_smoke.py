def test_smoke() -> None:
    from perf import generate_timing_data
    generate_timing_data([("ls", "ls")], "out.csv", repititions=1)
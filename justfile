run:
    #!/usr/bin/env bash
    gcc -o cnproc cnproc.c
    export TIMINGS_CSV="timings.csv"
    export PLOT_PNG="timings.png"
    uv run perf.py
    Rscript plot.r

fmt:
    uv run ruff check --fix
    uv run ty check --exit-zero

lint:
    uv run ruff check
    uv run ty check

test:
    uv run pytest .
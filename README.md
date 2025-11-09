A useful hyperfine and R plotting workflow.

## Usage

```bash
gcc -o cnproc cnproc.c
export TIMINGS_CSV="cpu_count_hyperfine_distribution.csv"
uv run perf.py
Rscript plot.r
```

## Requirements
- gcc ~ 13.3.0
- R (incl. tidyverse) ~ 4.3.3
- uv ~ 0.9.8
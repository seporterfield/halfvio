library(nanoparquet)
library(ggplot2)
library(dplyr)
library(scales, include.only = c("trans_breaks", "trans_format", "math_format"))
library(gghalves)

TIMINGS_PARQUET <- Sys.getenv("TIMINGS_PARQUET")
PLOT_PNG <- Sys.getenv("PLOT_PNG")
timing_data <- nanoparquet::read_parquet(TIMINGS_PARQUET)

p_thresholds <- timing_data %>%
  group_by(method) %>%
  summarise(
    p99_value = quantile(run_time_s, 0.995, na.rm = TRUE),
    p01_value = quantile(run_time_s, 0.005, na.rm = TRUE)
  )

outlier_data <- timing_data %>%
  left_join(p_thresholds, by = "method") %>%
  filter(run_time_s > p99_value | run_time_s < p01_value)

timing_plot <- ggplot(timing_data, aes(x = method, y = run_time_s, fill = method)) +
  geom_half_violin(
    side = "r",
    trim = FALSE,
    alpha = 0.8
  ) +
  geom_point(
    data = outlier_data,
    aes(x = method, y = run_time_s),
    inherit.aes = FALSE,
    color = "gray30",
    alpha = 0.5,
    size = 0.25,
    position = position_nudge(x = 0)
  ) +
  scale_y_log10(
    breaks = trans_breaks("log10", function(x) 10^x),
    labels = trans_format("log10", math_format(10^.x))
  ) +
  labs(
    y = "Time per Single Run (seconds, log scale)",
    x = NULL,
    title = "Runtime Distribution"
  ) +
  coord_flip() +
  theme_minimal() +
  theme(legend.position = "none")

ggsave(PLOT_PNG, timing_plot, width = 9, height = 4.5)
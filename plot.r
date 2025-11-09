library(readr)
library(ggplot2)
library(scales, include.only = c("trans_breaks", "trans_format", "math_format"))
library(gghalves)

TIMINGS_CSV <- Sys.getenv("TIMINGS_CSV")
PLOT_PNG <- Sys.getenv("PLOT_PNG", unset = "timings.png")
timing_data <- read_csv(TIMINGS_CSV, show_col_types = FALSE)

timing_plot <- ggplot(timing_data, aes(x = method, y = run_time_s, fill = method)) +
  geom_half_violin(
    side = "r", 
    trim = FALSE, 
    alpha = 0.8
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
# Render RWAA Onboarding Guide
# Run: source("render.R")

# Clean stale output
if (dir.exists("_site")) unlink("_site", recursive = TRUE)
if (dir.exists(".quarto")) unlink(".quarto", recursive = TRUE)
if (dir.exists("_freeze")) unlink("_freeze", recursive = TRUE)

# Verify all files exist before rendering
qmd_files <- list.files(pattern = "\\.qmd$")
cat("Found", length(qmd_files), "QMD files:\n")
cat(paste(" ", qmd_files), sep = "\n")
cat("\n")

if (!requireNamespace("quarto", quietly = TRUE)) install.packages("quarto")
library(quarto)
quarto_render()

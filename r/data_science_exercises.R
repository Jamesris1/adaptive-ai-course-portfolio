# Base-R version of the graph and study-planning exercise.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else "r/data_science_exercises.R"
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "study_sessions.csv")
artifact_dir <- file.path(root, "artifacts")
dir.create(artifact_dir, showWarnings = FALSE, recursive = TRUE)

study <- read.csv(data_path)

recommend_study_plan <- function(data, target_score = 90) {
  recent <- tail(data, 3)
  score_gain <- tail(recent$quiz_score, 1) - head(recent$quiz_score, 1)
  current <- tail(data$quiz_score, 1)
  gap <- max(0, target_score - current)
  weaker_language <- if (sum(data$r_hours) < sum(data$python_hours)) "R" else "Python"
  extra_hours <- round(max(1, gap / max(score_gain, 1) * 1.5), 1)
  data.frame(
    current_score = current,
    target_score = target_score,
    recent_score_gain = score_gain,
    priority_language = weaker_language,
    recommended_extra_hours = extra_hours
  )
}

summary <- recommend_study_plan(study)
write.csv(summary, file.path(artifact_dir, "r_analysis_summary.csv"), row.names = FALSE)

png(file.path(artifact_dir, "r_study_progress.png"), width = 1600, height = 1100, res = 180)
par(mfrow = c(2, 1), mar = c(4, 4.5, 3, 1), bg = "#f8fafc", family = "sans")
plot(
  study$week, study$quiz_score,
  type = "o", pch = 19, lwd = 3, col = "#4338ca",
  ylim = c(55, 96), xlab = "Week", ylab = "Quiz score",
  main = "Learning Progress Across Ten Weeks"
)
abline(h = 90, col = "#0f766e", lty = 2, lwd = 2)
legend("bottomright", legend = "Target: 90", col = "#0f766e", lty = 2, bty = "n")

hours <- rbind(study$python_hours, study$r_hours)
barplot(
  hours,
  beside = TRUE,
  names.arg = study$week,
  col = c("#2563eb", "#f97316"),
  border = NA,
  xlab = "Week",
  ylab = "Practice hours",
  main = "Weekly Practice by Language"
)
legend(
  "topleft", legend = c("Python", "R"),
  fill = c("#2563eb", "#f97316"), bty = "n", horiz = TRUE
)
dev.off()

print(summary)


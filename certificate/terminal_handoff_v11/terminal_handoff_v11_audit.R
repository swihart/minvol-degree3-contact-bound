#!/usr/bin/env Rscript

# Independent base-R numerical audit of the exact Python terminal-handoff
# candidate.  This script is not proof authority; it checks the archived bridge
# constants and the ordering of the old theorem, candidate theorem, unchanged
# near-Jung branch, and split terminal rows.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) != 1L) stop("cannot locate script path")
script_path <- normalizePath(sub("^--file=", "", file_arg), mustWork = TRUE)
root <- dirname(script_path)
constants_path <- file.path(root, "certificates", "audit_constants.csv")

x <- read.csv(constants_path, stringsAsFactors = FALSE)
vals <- setNames(as.numeric(x$value), x$name)
required <- c(
  "old_v1_volume",
  "candidate_v11_volume_lower",
  "candidate_v11_volume_upper",
  "near_jung_volume_lower",
  "split_terminal_min_volume_lower",
  "gain_over_v1",
  "near_margin",
  "split_margin"
)
if (!all(required %in% names(vals))) stop("missing audit constants")
if (any(!is.finite(vals[required]))) stop("non-finite audit constant")

old <- vals[["old_v1_volume"]]
candidate_lo <- vals[["candidate_v11_volume_lower"]]
candidate_hi <- vals[["candidate_v11_volume_upper"]]
near <- vals[["near_jung_volume_lower"]]
split <- vals[["split_terminal_min_volume_lower"]]

stopifnot(candidate_lo > old)
stopifnot(candidate_hi < near)
stopifnot(near < split)
stopifnot(vals[["gain_over_v1"]] > 2.1074e-6)
stopifnot(vals[["near_margin"]] > 2.5e-12)
stopifnot(vals[["near_margin"]] < 2.6e-12)
stopifnot(vals[["split_margin"]] > 6.3e-7)

cat(sprintf("v1.0.0 lower:              %.16f\n", old))
cat(sprintf("v1.1 candidate lower:      %.16f\n", candidate_lo))
cat(sprintf("unchanged near-Jung lower: %.16f\n", near))
cat(sprintf("split terminal minimum:    %.16f\n", split))
cat(sprintf("gain over v1.0.0:          %.16e\n", candidate_lo - old))
cat(sprintf("near-Jung safety margin:   %.16e\n", near - candidate_hi))
cat("MINVOL TERMINAL-HANDOFF V1.1 BASE-R AUDIT: PASS\n")

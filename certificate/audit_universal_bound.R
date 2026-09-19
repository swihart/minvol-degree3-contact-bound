#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
D <- if (length(args) >= 1) normalizePath(args[[1]]) else normalizePath(".")

constants_path <- file.path(D, "certificates", "audit_constants.csv")
fan_path <- file.path(D, "certificates", "fan_orbit_margin_audit.tsv")
hulls_path <- file.path(D, "certificates", "all_axis_pair_section_hulls.tsv")
rows_path <- file.path(D, "certificates", "refined_lower_rows.tsv")

constants <- read.csv(
  constants_path,
  stringsAsFactors = FALSE,
  colClasses = c("character", "character", "character", "character")
)
fan <- read.delim(
  fan_path,
  stringsAsFactors = FALSE,
  colClasses = c("integer", "integer", "character", "character", "integer", "character", "numeric")
)
hulls <- read.delim(
  hulls_path,
  stringsAsFactors = FALSE,
  colClasses = c("integer", "integer", "integer", "character", "character", "character", "character")
)
rows <- read.delim(
  rows_path,
  stringsAsFactors = FALSE,
  colClasses = "character"
)

text_val <- function(name) {
  i <- match(name, constants$name)
  stopifnot(!is.na(i))
  constants$decimal[[i]]
}

val <- function(name) {
  out <- suppressWarnings(as.numeric(text_val(name)))
  stopifnot(length(out) == 1, is.finite(out))
  out
}

compare_digit_strings <- function(a, b) {
  if (nchar(a) < nchar(b)) return(-1L)
  if (nchar(a) > nchar(b)) return(1L)
  aa <- utf8ToInt(a)
  bb <- utf8ToInt(b)
  different <- which(aa != bb)
  if (length(different) == 0) return(0L)
  k <- different[[1]]
  if (aa[[k]] < bb[[k]]) -1L else 1L
}

canonical_nonnegative_decimal <- function(x) {
  stopifnot(grepl("^[0-9]+(\\.[0-9]+)?$", x))
  pieces <- strsplit(x, ".", fixed = TRUE)[[1]]
  integer_part <- sub("^0+", "", pieces[[1]])
  if (identical(integer_part, "")) integer_part <- "0"
  fractional_part <- if (length(pieces) == 2) pieces[[2]] else ""
  fractional_part <- sub("0+$", "", fractional_part)
  list(integer = integer_part, fractional = fractional_part)
}

nonnegative_decimal_less <- function(a, b) {
  pa <- canonical_nonnegative_decimal(a)
  pb <- canonical_nonnegative_decimal(b)
  integer_cmp <- compare_digit_strings(pa$integer, pb$integer)
  if (integer_cmp != 0L) return(integer_cmp < 0L)
  n <- max(nchar(pa$fractional), nchar(pb$fractional))
  fa <- paste0(pa$fractional, strrep("0", n - nchar(pa$fractional)))
  fb <- paste0(pb$fractional, strrep("0", n - nchar(pb$fractional)))
  compare_digit_strings(fa, fb) < 0L
}

profile <- function(area, depth, extension) {
  area * extension^3 / (24 * (depth + extension)^2)
}

profile_derivative <- function(area, depth, extension) {
  area * extension^2 * (3 * depth + extension) /
    (24 * (depth + extension)^3)
}

stopifnot(nrow(constants) == 60)
all_decimals <- suppressWarnings(as.numeric(constants$decimal))
stopifnot(all(is.finite(all_decimals)))

# Four exact replacement cells for the former O3A1 interval.
stopifnot(nrow(rows) == 4)
stopifnot(all(rows$angle_N == "76800"))
stopifnot(all(rows$radial_grid == "40000000000"))
stopifnot(rows$left[[1]] == "30549/50000")
stopifnot(rows$right[[1]] == rows$left[[2]])
stopifnot(rows$right[[2]] == rows$left[[3]])
stopifnot(rows$right[[3]] == rows$left[[4]])
stopifnot(rows$right[[4]] == "6113/10000")
stopifnot(all(as.numeric(rows$positive_steps) == c(12739, 12719, 12699, 12679)))
stopifnot(all(as.numeric(rows$negative_steps) == c(36890, 36931, 36973, 37015)))
stopifnot(val("minimum_refined_row_margin") > 1.8e-5)
for (i in 1:4) {
  stopifnot(val(paste0("refined_row", i, "_margin")) > 1.8e-5)
  stopifnot(val(paste0("refined_row", i, "_pi_coefficient")) > val("theorem_pi_coefficient"))
}

# Exact fan orbit summary, read independently as finite decimals.
stopifnot(nrow(fan) == 24833)
stopifnot(sum(fan$orbit_size) == 98306)
stopifnot(sum(fan$orbit_size[fan$active_bound == "convex"]) == 4)
stopifnot(sum(fan$orbit_size[fan$active_bound == "edge"]) == 0)
stopifnot(sum(fan$orbit_size[fan$active_bound == "dominant"]) == 81663)
stopifnot(sum(fan$orbit_size[fan$active_bound == "tie"]) == 16639)
stopifnot(min(fan$margin_decimal) > 2.8e-10)

stopifnot(nrow(hulls) == 550)
stopifnot(sum(hulls$axis == 0 & hulls$sign == 1) == 110)
stopifnot(sum(hulls$axis == 0 & hulls$sign == -1) == 84)
stopifnot(sum(hulls$axis == 1 & hulls$sign == 1) == 102)
stopifnot(sum(hulls$axis == 1 & hulls$sign == -1) == 76)
stopifnot(sum(hulls$axis == 2 & hulls$sign == 1) == 102)
stopifnot(sum(hulls$axis == 2 & hulls$sign == -1) == 76)

stopifnot(val("split_radius") > 0.6113911)
stopifnot(val("split_radius") < 0.6113913)
stopifnot(val("sharp_total_deficiency_upper") > 0.0193)
stopifnot(val("sharp_total_deficiency_upper") < 0.0195)
stopifnot(val("determinant_squared_lower") > 0.9901)
stopifnot(val("reference_fan_coefficient") > 0.5851)
stopifnot(val("core_volume_lower") > 0.41173)
stopifnot(val("minimum_fan_margin") > 2.8e-10)

# Independently reconstruct the new dominant-edge coordinate-width bounds.
# Edge order: e01,e02,e03,e12,e13,e23.  The exact Python verifier checks
# these integer identities; here base R checks their numerical consequences.
diag0 <- c(1, -1, -1, -1, -1, 1)
diag1 <- c(-1, 1, -1, -1, 1, -1)
diag2 <- c(-1, -1, 1, 1, -1, -1)
stopifnot(all(1 - diag0 == c(0, 2, 2, 2, 2, 0)))
stopifnot(all(1 - 3 * diag1 == c(4, -2, 4, 4, -2, 4)))
stopifnot(all(1 - 3 * diag2 == c(4, 4, -2, -2, 4, 4)))

E <- val("sharp_total_deficiency_upper")
w0sq <- 1 / (1 + E / 2)
w1sq <- 1 / (1 + E / 6)
stopifnot(abs(w0sq - val("axis0_coordinate_width_squared_lower")) < 5e-15)
stopifnot(abs(w1sq - val("axis1_coordinate_width_squared_lower")) < 5e-15)
stopifnot(abs(w1sq - val("axis2_coordinate_width_squared_lower")) < 5e-15)
stopifnot(abs(sqrt(w0sq) - val("axis0_coordinate_width_lower")) < 5e-15)
stopifnot(abs(sqrt(w1sq) - val("axis1_coordinate_width_lower")) < 5e-15)
stopifnot(abs(sqrt(w1sq) - val("axis2_coordinate_width_lower")) < 5e-15)
stopifnot(val("axis0_coordinate_width_lower") > 0.995)
stopifnot(val("axis1_coordinate_width_lower") > val("axis0_coordinate_width_lower"))
stopifnot(abs(val("axis1_coordinate_width_lower") - val("axis2_coordinate_width_lower")) < 1e-15)

# Independent base-R reconstruction of all three one-dimensional cap minima.
cap_sum <- 0
for (axis in 0:2) {
  p <- paste0("axis", axis, "_")
  area_plus <- val(paste0(p, "area_plus"))
  area_minus <- val(paste0(p, "area_minus"))
  depth_plus <- val(paste0(p, "depth_plus"))
  depth_minus <- val(paste0(p, "depth_minus"))
  total <- val(paste0(p, "total_excess"))
  left_text <- text_val(paste0(p, "allocation_left"))
  right_text <- text_val(paste0(p, "allocation_right"))
  left_binary64 <- val(paste0(p, "allocation_left"))
  right_binary64 <- val(paste0(p, "allocation_right"))
  archived <- val(paste0(p, "cap_lower"))

  stopifnot(area_plus > 0, area_minus > 0)
  stopifnot(depth_plus > 0, depth_minus > 0, total > 0)
  stopifnot(nonnegative_decimal_less(left_text, right_text))
  stopifnot(0 <= left_binary64, right_binary64 <= total)

  # The exact brackets have width 1e-20 and collapse to one binary64 number.
  # Build a wider diagnostic bracket for the independent R root finder.
  center <- (left_binary64 + right_binary64) / 2
  audit_half_width <- max(
    1e-12,
    4096 * .Machine$double.eps * max(1, abs(center), abs(total))
  )
  audit_left <- center - audit_half_width
  audit_right <- center + audit_half_width
  stopifnot(0 <= audit_left, audit_left < audit_right, audit_right <= total)

  balance_derivative <- function(extension_plus) {
    profile_derivative(area_plus, depth_plus, extension_plus) -
      profile_derivative(area_minus, depth_minus, total - extension_plus)
  }

  dleft <- balance_derivative(audit_left)
  dright <- balance_derivative(audit_right)
  stopifnot(dleft < 0, dright > 0)

  root <- uniroot(
    balance_derivative,
    interval = c(audit_left, audit_right),
    tol = 1e-15
  )$root
  stopifnot(audit_left < root, root < audit_right)

  determinant_scale <- sqrt(val("determinant_squared_lower"))
  numerical_minimum <- determinant_scale *
    (profile(area_plus, depth_plus, root) +
       profile(area_minus, depth_minus, total - root))
  stopifnot(abs(numerical_minimum - archived) < 5e-13)

  widened_lower <- determinant_scale *
    (profile(area_plus, depth_plus, audit_left) +
       profile(area_minus, depth_minus, total - audit_right))
  stopifnot(widened_lower <= archived + 1e-13)
  stopifnot(archived - widened_lower < 1e-11)
  cap_sum <- cap_sum + archived
}

stopifnot(val("axis0_cap_lower") > 5.0e-5)
stopifnot(val("axis1_cap_lower") > 4.6e-5)
stopifnot(val("axis2_cap_lower") > 4.6e-5)
stopifnot(abs(cap_sum - val("total_cap_lower")) < 5e-15)
stopifnot(val("total_cap_lower") > 1.43e-4)

# Reconstruct the inherited six-cap disjointness gap.
R <- val("split_radius")
q <- R^2
E_reconstructed <- (3 - 8 * q) / (4 * q - 1)
cmax <- 3 - 8 * q
hmin <- min(
  val("axis0_support_plus"), val("axis0_support_minus"),
  val("axis1_support_plus"), val("axis1_support_minus"),
  val("axis2_support_plus"), val("axis2_support_minus")
)
reconstructed_gap <- 2 * (hmin - cmax)^2 - 3 / (1 - E_reconstructed)
stopifnot(abs(E_reconstructed - E) < 5e-15)
stopifnot(abs(reconstructed_gap - val("cross_axis_gap")) < 5e-13)
stopifnot(reconstructed_gap > 0.63)

near_reconstructed <- val("core_volume_lower") + val("total_cap_lower")
stopifnot(abs(near_reconstructed - val("near_jung_volume_lower")) < 5e-15)
stopifnot(val("near_jung_volume_lower") > 0.4118796)
stopifnot(val("theorem_volume_lower") > 0.4118775)
stopifnot(val("theorem_volume_upper") >= val("theorem_volume_lower"))
stopifnot(val("near_jung_volume_lower") > val("theorem_volume_upper"))
stopifnot(val("near_jung_margin") > 2.0e-6)
stopifnot(val("strict_gain_over_previous") > 2.0e-5)

cat(sprintf("refined O3A1 rows:             %d\n", nrow(rows)))
cat(sprintf("angular grid / radial grid:    %s/%s\n", rows$angle_N[[1]], rows$radial_grid[[1]]))
cat(sprintf("minimum refined row margin:   %.15e\n", val("minimum_refined_row_margin")))
cat(sprintf("fan orbit rows / vertices:    %d/%d\n", nrow(fan), sum(fan$orbit_size)))
cat(sprintf("dominant / tie active rays:   %d/%d\n",
            sum(fan$orbit_size[fan$active_bound == "dominant"]),
            sum(fan$orbit_size[fan$active_bound == "tie"])))
cat(sprintf("minimum fan margin:           %.15e\n", min(fan$margin_decimal)))
cat(sprintf("sharp deficiency upper:       %.15f\n", E))
cat(sprintf("determinant squared lower:    %.15f\n", val("determinant_squared_lower")))
cat(sprintf("core volume lower:            %.15f\n", val("core_volume_lower")))
cat(sprintf("coordinate width lowers:      %.15f/%.15f/%.15f\n",
            val("axis0_coordinate_width_lower"),
            val("axis1_coordinate_width_lower"),
            val("axis2_coordinate_width_lower")))
cat(sprintf("axis cap lowers:              %.15f/%.15f/%.15f\n",
            val("axis0_cap_lower"), val("axis1_cap_lower"), val("axis2_cap_lower")))
cat(sprintf("three-pair cap lower:         %.15f\n", val("total_cap_lower")))
cat(sprintf("cross-axis gap:               %.15f\n", reconstructed_gap))
cat(sprintf("near-Jung volume lower:       %.15f\n", val("near_jung_volume_lower")))
cat(sprintf("universal coefficient lower: %.15f\n", val("theorem_volume_lower")))
cat(sprintf("gain over previous:           %.15e\n", val("strict_gain_over_previous")))
cat("MINVOL UNIVERSAL CONTACT-BOUND BASE-R AUDIT: PASS\n")

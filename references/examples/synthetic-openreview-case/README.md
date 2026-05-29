# Synthetic OpenReview Case

Use this case to test per-reviewer strategy.

## Inputs

- Venue rules: user-confirmed OpenReview per-reviewer thread, 5000 chars per reply, no external links.
- Paper: synthetic ML method with claimed +2.1 average improvement.
- Reviews:
  - R1: positive, asks for clarification on novelty.
  - R2: borderline, missing baseline and significance concern.
  - R3: negative, thinks dataset scope is too narrow.

## Expected outputs

- Reviewer stance map with R2 as pivotal.
- Atomic concerns for novelty, baseline, significance, dataset scope.
- Experiment triage marking baseline as must-do if feasible.
- Per-reviewer response blueprint.

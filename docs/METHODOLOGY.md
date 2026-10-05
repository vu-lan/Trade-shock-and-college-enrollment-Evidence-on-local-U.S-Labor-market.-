# Original-model audit form

Complete from the original manuscript AND executed code. Resolve any disagreement explicitly; do not silently rewrite the study.

- Manuscript version, table numbering, population/sample years, geographic units and balanced/unbalanced panel decisions.
- Exact enrollment indicator, age restrictions, person weights, denominators and missing-data treatment.
- Treatment/IV: source variables, complete formula, employment bases, country/industry sets, concordances, nominal/real units, normalization and period scaling.
- Main model: every endogenous regressor and excluded instrument, controls, fixed effects, regression weights, pooled versus period-specific specifications; identification assumptions and rank/weak-instrument checks.
- Inference: estimator options, covariance formula, clustering level, finite-sample correction and any shift-share-specific procedure. Reproduce baseline first; put new inferential methods in extensions.
- Outcomes beyond enrollment (if present): exact construction and their role as outcome, control, mechanism or endogenous regressor.
- Diagnostics: geographic allocation, merge losses, duplicate keys, sample attrition, missingness, support, first-stage coefficients/diagnostics and exact estimation N.
- Robustness: list only analyses appearing in the original study; distinguish newly proposed checks.
- Numerical acceptance: full-precision benchmarks, chosen tolerances and rationale, paper-rounding comparison, separate visual figure inspection.

The generic equations in README are orientation only. They do not fill any of these fields automatically.

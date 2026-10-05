# Variable dictionary to complete

Names below are proposed canonical names, not verified original variable names. Add source column, exact transformation, unit, valid range, missing codes and the generating script for **every** analysis variable.

| Proposed variable | Unit/key | Definition to recover |
|---|---|---|
| `cz_id` | Geography identifier | CZ vintage; consistent format and coverage |
| `year` | Calendar/sample year | Census/ACS reference year versus field year |
| `period_start`, `period_end` | Unique with `cz_id` | Exact periods; annualization or decade-equivalent scaling |
| `enrollment_rate` | Fraction [0,1] | Eligible age/cohort, numerator definition, denominator, person weights |
| `delta_enrollment_pp` | Percentage points | 100 × end-minus-start fraction; change scaling must be explicit |
| `delta_import_exposure` | To confirm | Import growth per worker, price basis, industry/worker base |
| `instrument_import_exposure` | To confirm | Other-country import growth, basket and lagged employment shares |
| `regression_weight` | To confirm | Population base year, normalization and zero/missing treatment |
| Controls/other endogenous variables | To confirm | Full names, levels/changes, timing, transformations, instrument mapping |

If enrollment is weighted, document `sum(weight × enrolled × eligible) / sum(weight × eligible)` and whether geography allocations multiply person weights. A zero denominator is missing/unsupported, never a zero enrollment rate. Do not treat institution attendance as college enrollment without the original coding rule.

Keep identifiers as stable strings or validated integers; state/PUMA vintage belongs in the join key. Report allocation-weight sums and weighted totals before/after geographic conversion. Avoid interpreting a planned many-to-many crosswalk as a simple one-to-one merge.

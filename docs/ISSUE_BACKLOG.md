# Proposed replication issues

These are ready-to-copy issue specifications. They have **not** been opened automatically. Owner for source recovery: Lan; assign integration and independent validation after handover.

| Priority | Suggested issue title | Depends on | Acceptance criteria |
|---|---|---|---|
| P0 | Freeze manuscript and original study specification | None | Exact version; no unresolved study-spec fields; table/figure inventory |
| P0 | Recover original scripts and software environment | Manuscript | Complete master/script dependency graph; all package versions and licenses |
| P0 | Document input access and provenance | Manuscript | Every consumed input has access recipe, source release, terms and SHA-256 |
| P0 | Restore geography and outcome construction | Inputs, scripts | Vintage-correct joins; allocation audit; denominator and weighted sample report |
| P0 | Restore trade exposure and SSIV | Inputs, scripts | Exact source/formula/bases/units; numerical comparison with original exposure |
| P0 | Integrate panel, estimates and export pipeline | Geography, exposure | Unique keys, sample attrition, original model/inference, table/figure mapping |
| P0 | Supply full-precision benchmarks and stage 07 | Original outputs | N/coefficient/SE/first-stage checks; explicit tolerances; failure exits nonzero |
| P1 | Run independent clean-room replication | All P0 | Clean clone and acquired data reproduce all mapped outputs; provenance attached |
| P1 | Prepare documented replication release | Independent run | License choice, citation, tested locks, runtime/hardware and known limitations |

A release should not be accepted because scaffold CI is green. Close each issue only with its acceptance evidence, and record which manuscript/version and commit were validated.

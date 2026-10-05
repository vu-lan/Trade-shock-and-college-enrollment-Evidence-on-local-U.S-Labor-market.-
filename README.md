# Trade shocks and college enrollment: evidence from U.S. local labor markets

**Status: replication scaffold — original data, analysis code, and numerical benchmarks are not included.**
The repository previously contained only a short description of a shift-share instrumental-variable (SSIV) approach based on Autor, Dorn, and Hanson (2013). This scaffold specifies how to assemble and audit a replication package; it does **not** reproduce the paper or implement a substitute estimator.

## Research and methodological scope

The project studies trade exposure and college enrollment in U.S. local labor markets. The intended design uses ADH-style trade exposure and an instrument constructed from import growth in other high-income countries. Exact samples, years, outcomes, controls, weights, and inference must be recovered from Lan's original manuscript and scripts. Names and contracts below are **proposed interfaces**, not verified descriptions of the original analysis.

For orientation only, an ADH-style exposure can be expressed as

$$
\Delta IPW_{ct}=\sum_j\frac{L_{cj,0}}{L_{j,0}}\frac{\Delta M^{US}_{jt}}{L_{c,0}},
\qquad
Z_{ct}=\sum_j\frac{L_{cj,b}}{L_{j,b}}\frac{\Delta M^{OTH}_{jt}}{L_{c,b}}.
$$

Here, imports `M` refer to the specified origin (China in the ADH design); `c` is a commuting zone, `j` is an industry, `t` is a change period, and `b` denotes the instrument's predetermined employment base. Import baskets, currencies, deflators, scaling, industry concordances, and base years must match the original design. `OTH` is not to be constructed by casually averaging country growth rates. The expression above is a conceptual guide; Lan must supply the exact implemented formula, including any differences from ADH.

A generic 2SLS specification is

$$
\Delta y_{ct}=\beta\Delta IPW_{ct}+X_{ct}'\gamma+\lambda_t+u_{ct},
\qquad
\Delta IPW_{ct}=\pi Z_{ct}+X_{ct}'\delta+\lambda_t+v_{ct}.
$$

These equations do not establish causality by themselves. Replication requires the original instrument, identifying assumptions, first stage, weighting and standard-error procedure. Any additional endogenous regressors require their own documented instruments and identification checks. Alternative specifications belong in separately labeled extensions, not silently in the baseline.

Reference: Autor, D. H., Dorn, D., and Hanson, G. H. (2013), *The China Syndrome: Local Labor Market Effects of Import Competition in the United States*, American Economic Review 103(6), 2121–2168. DOI: https://doi.org/10.1257/aer.103.6.2121.

## Repository layout

| Path | Purpose |
|---|---|
| `config/pipeline.json` | Ordered stage commands and input/output contracts |
| `config/study_spec.json` | Original-design decisions; unresolved fields are `null` |
| `config/data_manifest.csv` | Required source files, access conditions, versions and SHA-256 |
| `config/output_manifest.csv` | Manuscript-to-output mapping and numerical acceptance criteria |
| `data/raw/` | Immutable original inputs; ignored by Git |
| `data/interim/` | Harmonized microdata, geography mappings and exposure data; ignored |
| `data/processed/` | Analysis-ready CZ-period panel; ignored |
| `src/stages/` | Numbered stage adapters; currently explicit blocking placeholders |
| `scripts/replicate.py` | Cross-platform preflight and pipeline runner (Python standard library) |
| `docs/` | Access, variable, methodological, software and handover documentation |
| `outputs/tables/`, `outputs/figures/` | Generated manuscript tables and figures; ignored |
| `outputs/diagnostics/` | Sample/merge/first-stage reports and benchmark comparison |
| `logs/` | Timestamped stage logs and successful-run provenance |
| `tests/` | Runner safety tests; no claim about econometric correctness |
| `.github/` | Scaffold CI and replication-task issue template |
| `environment.yml`, `requirements.txt` | Minimal runner environment; original analysis dependencies pending |

Folder README files remain tracked. No microdata, credentials, synthetic estimates, or fabricated results are bundled.

## Quick start

Requirements for the scaffold: Git and Python 3.11 or 3.12. No external Python packages are needed. These versions are a scaffold compatibility choice, not a claim about the author's original software.

```bash
git clone https://github.com/vu-lan/Trade-shock-and-college-enrollment-Evidence-on-local-U.S-Labor-market.-.git
cd Trade-shock-and-college-enrollment-Evidence-on-local-U.S-Labor-market.-
python -m venv .venv
```

Activate on macOS/Linux with `source .venv/bin/activate`; on Windows PowerShell use `.venv\Scripts\Activate.ps1` (or call `.venv\Scripts\python.exe` directly if activation is unavailable).

```bash
python -m pip install -r requirements.txt
python scripts/replicate.py --validate-scaffold
python -m unittest discover -s tests -v
python scripts/replicate.py --dry-run
python scripts/replicate.py --check
```

`--validate-scaffold` checks scaffold structure, not research reproducibility. `--dry-run` prints the stage plan without running it. `--check` **currently exits 1 by design**, listing unresolved study choices, unavailable inputs/checksums, unimplemented stages, and absent output benchmarks. Exit 0 means a command's stated checks passed, not that the paper is correct.

Optional Conda route: `conda env create -f environment.yml`, then `conda activate trade-enrollment`. Use either Conda or venv. Once original dependencies are known, replace the preliminary environment with a tested, platform-specific lock and document it in `docs/SOFTWARE.md`.

## Assemble the real replication

1. Complete [Lan's handover checklist](docs/LAN_CHECKLIST_VI.md), including manuscript, source scripts, and reference outputs.
2. Obtain data using [data access instructions](docs/DATA_ACCESS.md). Keep original files unchanged. Supply the actual local filenames in `config/data_manifest.csv` and the exact release/extract metadata. Use licensed data only through its permitted access route.
3. Fill every field in `config/study_spec.json` from the original research; `null` blocks execution. Record exclusions and source-to-variable rules in `docs/VARIABLES.md` and `docs/METHODOLOGY.md`.
4. Replace stage placeholders with the original code or adapters. Python, Stata or R can be invoked using a JSON argv list in `config/pipeline.json`; use absolute executable paths when needed. Set `implemented: true` only after integration. Retain relative project paths and set every stage's real inputs/outputs. A process must exit nonzero on any scientific or data validation error; verify Stata batch error propagation if used.
5. Add checksums using `python scripts/replicate.py --hash data/raw/<file>`. Fill the manifest's access/version/license fields. Do not redistribute restricted data.
6. Fill `config/output_manifest.csv` with each actual table/figure/panel, original benchmark file, absolute/relative tolerances and its generating stage. Blank tolerances for nonnumeric figures must be explained in `validation_rule`. Implement numerical comparisons in stage 07.
7. Record all software and package versions, hardware, expected duration and memory in `docs/SOFTWARE.md`. Keep the original econometric software unless a separately validated port is intended.
8. Run from a clean generated-data/output state:

```bash
python scripts/replicate.py --check
python scripts/replicate.py --run
```

Existing declared outputs must first be archived or removed manually; the runner refuses to reuse or overwrite them. The runner executes stages in order from the repository root, stops on failure or missing declared output, captures combined stdout/stderr, and records raw/output hashes and runtime information on successful completion. It does not automatically download restricted data, install Stata/R packages, or resume a partial run. The analysis itself must apply the study seed, sorting rules and package versions. No partial run should be reported as a completed replication.

## Pipeline: inputs to outputs

| Stage | Input | Output and required audit |
|---|---|---|
| 01 Ingest | Original microdata, extraction metadata and trade files | Parsed source data; row counts, types, missing codes |
| 02 Harmonize geography | Parsed microdata and vintage-specific crosswalks | CZ allocation; join cardinality, unmatched mass and weight conservation |
| 03 Construct outcomes | CZ-assigned records | CZ-year enrollment and controls; numerator/denominator and support |
| 04 Construct exposure/IV | ADH files or trade/employment components | CZ-period treatment and IV; base-year and unit checks |
| 05 Build panel | Outcomes, controls and exposure | Unique CZ-period panel; sample attrition and period scaling |
| 06 Estimate/export | Frozen analysis panel and exact study specification | Main/robustness tables, figures, first stage and estimation sample |
| 07 Verify | Generated outputs and original numerical benchmarks | Machine-readable comparison; nonzero exit on any failed tolerance |

Concrete proposed filenames are in `config/pipeline.json`. If using published ADH treatment/instrument files, replace the construction route and manifest with the exact required source; do not require raw trade components unnecessarily. Any change to a contract must update the stage, config and documentation together.

## Naming and data rules

- Lowercase ASCII `snake_case`; no spaces, accented filenames or `final_final` suffixes.
- Source data: `{source}_{sample_or_vintage}_{year_or_period}_{release}.{ext}`; keep upstream filename alongside local filename in the manifest. Replace all template tokens with actual values.
- Intermediate: `ipums_harmonized.parquet`, `persons_cz.parquet`; final: `cz_period_analysis.parquet`. These formats are proposals; preserve `.dta`/`.rds` if required by the original workflow and update contracts.
- Code: `01_ingest`, `02_harmonize_geography`, …; use `.py`, `.do` or `.R` as appropriate. Put exploratory work outside the production pipeline.
- IDs such as state FIPS/PUMA/CZ must preserve padding and vintage. Never join PUMAs on their code alone. Crosswalk expansion can be many-to-many and must conserve weighted population according to the documented allocation rule.
- Use `cz_id`, `year`, `period_start`, `period_end` as proposed key names. Distinguish levels, changes and annualized changes; label enrollment fractions versus percentage points and imports dollars versus thousands of dollars.
- Outputs: `table_{paper_number}_{short_name}.csv/.tex`, `figure_{paper_number}_{short_name}.pdf`; the current `*_index.csv` files are proposed export inventories, not manuscript tables.
- Treat `data/raw` as read-only. Never hard-code user-specific Desktop paths. Do not commit `.env`, API keys, or individual-level data.

## Validation and release gate

Checks must establish geography and time comparability, uniqueness of CZ-period rows, documented weighted enrollment denominators, valid shares in [0,1], no silent merge loss, finite treatment/instrument values, and the same estimation sample across intended specifications. Record N, coefficients, standard errors, first-stage diagnostics and the exact inference method. Shared industry shocks may matter for inference; reproduce the original method first and label methodological changes separately.

An independent user must rebuild the panel, tables and figures using the stated commands and legally acquired data. Compare **unrounded** numerical results to a frozen benchmark with an explicit rule such as `abs(actual - expected) <= atol + rtol * abs(expected)`; preserve paper-rounded values as a separate check. A figure visual check alone cannot validate coefficients. CI currently runs only runner tests and scaffold checks, not confidential-data replication. Fill the issue backlog and release checklist before calling the package replication-ready.

See [proposed issues](docs/ISSUE_BACKLOG.md). No issues are automatically opened by this scaffold.

## Attribution, licensing and availability

Author: Lan (GitHub: `vu-lan`). Confirm the final manuscript title, author list and persistent citation before a release. No license is selected on the author's behalf: public repository visibility is not a license. Add a code license after the author chooses one, and document data-specific licenses separately. Do not assume IPUMS or third-party source data may be rehosted. Source links below are acquisition starting points; exact releases and access conditions must be verified for this study.

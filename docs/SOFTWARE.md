# Software and runtime record

## Scaffold
Python standard library only; CI targets Python 3.11 and 3.12 on Ubuntu and Windows. `requirements.txt` contains no third-party packages. `environment.yml` constrains the interpreter family but is **not** a reproducibility lock. GitHub CI verifies orchestration only.

## Original analysis — author must complete

| Item | Required record |
|---|---|
| Primary runtime | Stata edition/version + OS, R version, or Python version actually used |
| Extensions | Stata ado names/source/version (including IV/FE/export commands if used), R packages, Python packages |
| Installation | Exact commands and archived/locked versions; do not auto-upgrade during replication |
| License | Stata availability/license requirement if used; never place license keys in the repository |
| Portable invocation | Executable path/configuration; ensure batch failures return nonzero |
| Reproducibility | Seed, sorting, locale, encoding and thread-count sensitivity |
| Lock | Actual tested lockfile; retain package version/session reports |
| Resource requirements | CPU, RAM, free disk, total/per-stage runtime measured on a complete run |

Do not add pandas, linearmodels or a new estimator just to make a dependency file look complete. Preserve original code until a port is separately checked against full-precision results. Parquet in contracts does not imply a reader/writer package is already installed: update contracts or add the real dependencies when code is supplied.

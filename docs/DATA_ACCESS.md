# Source acquisition and provenance

All manifest filenames are proposed local aliases, not assertions that these source files exist. Change the manifest and stage contracts together when restoring actual files. No source data are bundled. This document is a completion form, not a finished download recipe.

| Source | Acquisition starting point | Lan must supply |
|---|---|---|
| IPUMS USA or original population microdata | https://usa.ipums.org/usa/ | Exact Census/ACS samples and years, extract ID/date, selected variables, universe, DDI/XML/codebook and reading syntax; whether household records are used |
| ADH treatment/IV or their original components | https://www.ddorn.net/data.htm and the ADH article replication materials | Archive/release, direct file URL, upstream filename, variable mapping, currencies/deflators, units and country list |
| Geographic crosswalks | Original study's geography source, potentially Dorn/IPUMS | Exact PUMA vintage, CZ definition, source URL, allocation weights and treatment of unmatched units |
| Other controls/deflators | Original manuscript/source scripts | Each source/version and retrieval recipe; add one manifest row per required file |
| Reference results | Author's frozen original results | Full-precision values, sample sizes, manuscript-to-output mapping and redistribution permission |

For each input: record upstream filename, local alias, release/extract ID, retrieval URL, retrieval date within access instructions, access steps, usage/redistribution terms and SHA-256. The runner checks file hashes but cannot establish license compliance or scientific suitability. For archives, document unpacking and checksums of the actual consumed files. One hash is required per consumed file; add rows for every microdata year and crosswalk vintage.

IPUMS extracts may require registration/project approval. Reusers should obtain their own authorized extract with exactly the documented selection. Do not commit or circulate microdata without checking its terms. For nonredistributable inputs provide metadata and a reproducible acquisition recipe, not the records. Public availability does not establish redistribution rights.

The default manifest assumes preconstructed ADH-style inputs. If the original work rebuilds exposure/IV, replace that row with the full trade, industry employment, concordance and deflator dependencies, and update stage 04. No raw-input downloader is supplied until sources and access conditions are known.

Source check (2026-10-05): Dorn’s data page lists industry-trade inputs under [D], geography crosswalks under [E], and paper-specific archives. Crosswalk [E4] covers 1990 PUMAs, [E5] covers 2000 Census/2005–2011 ACS PUMAs, and [E6] covers 2010 Census/2012–2021 ACS PUMAs. Choose by the actual extract vintage; this does not establish which file Lan originally used. Source: https://www.ddorn.net/data.htm.

# AnonLabels-200 (review copy)

A US grocery corpus of 200 packaged products where the barcode, the label
text, and the photograph of the physical package all belong to the same
product, released in two provenance tiers: 65 rows hand-transcribed from our
own photographs at a single US retailer (CC0), 135 rows derived from Open
Food Facts (ODbL). This is the anonymized review copy: the public repository
URL, product photographs, and retailer name are withheld for double-blind
review and are released in full with the camera-ready version.

Files: labels200.csv (full corpus), labels65_handtranscribed.csv
(hand-transcribed tier), datapackage.json (schema), k_redundancy.py
(redundancy budget k and per-allergen fragility), validate_corpus.py
(arithmetic validation gates), stats.py (Wilson CIs and exact binomial
tests), monte_carlo.py (RQ3 risk composition, seed 20260824),
allergen_omission.py (paired database-path omission analysis).

The deployed application is publicly listed on a mobile app store; the store
listing is likewise withheld for anonymity and available to the chairs on
request.

## Column completeness (by design, not missing data)

- Image url: reads withheld_for_review in this copy; every product's
  photographs exist and are released with the camera-ready version.
- source_url: populated for the 135 rows derived from Open Food Facts,
  where it carries the per-record attribution the ODbL license calls for;
  empty for the 65 own-photography rows, which have no external source.
- category: complete for all 200 rows; 11 values were completed
  editorially from product name, brand and ingredient list, in the same
  kebab-case convention as the source taxonomy.
- The upca_expansion column of the canonical release (populated only for
  the 8 UPC-E barcodes requiring expansion to UPC-A) is omitted here as it
  is unused by any analysis; gtin14 already carries the canonical key.

Apart from these documented substitutions the anonymized copy is
row-for-row identical to the canonical release.

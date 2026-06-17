# papers/ — drop your paper PDFs here

To show a **real journal front page** on the Research page (instead of the
styled placeholder), drop a PDF of the paper here, named to match the basename
used in `research.html`, then run:

```bash
scripts/generate-paper-thumbs.sh
```

That renders the first page of each PDF to `img/papers/<basename>.png`. The
Research page automatically uses the PNG when present and falls back to
`img/papers/placeholders/<basename>.svg` when it is missing.

## Expected filenames (one per featured paper)

| Drop this file                              | Paper |
|---------------------------------------------|-------|
| `averett-2026-lgbtq-stem.pdf`               | Not Thriving: LGBTQ+ Women in STEM Work |
| `averett-2026-cdctc-health.pdf`             | Long-Term Health Effects … Child & Dependent Care Tax Credit |
| `averett-2025-one-child-fertility.pdf`      | Exposure to the One-Child Policy and Fertility … |
| `averett-2025-instate-tuition.pdf`          | The Gendered Impact of In-State Tuition Policies … |
| `averett-2025-circadian.pdf`                | Living in Sync with the Sun |
| `averett-2021-light-pollution.pdf`          | Light Pollution, Sleep Deprivation during Pregnancy … |
| `averett-2020-aviation-noise.pdf`           | Residential Noise Exposure and Health … |
| `averett-2019-medicaid-opioid.pdf`          | Medicaid Expansion and Opioid Deaths |
| `averett-2012-depression-risky.pdf`         | Identification of the Effect of Depression on Risky Sexual Behavior |

## Notes

- Backend: the script uses `pdftoppm` (poppler) if installed, otherwise falls
  back to macOS `qlmanage` (Quick Look) — no install required.
- If a PDF's first page is a publisher cover sheet, add a page override in
  `scripts/generate-paper-thumbs.sh` (only works with the poppler backend).
- To add a new featured paper: add a card in `research.html`, add an entry to
  `PAPERS` in `scripts/generate-paper-placeholders.py`, run that script, then
  (optionally) drop the PDF here and run `generate-paper-thumbs.sh`.

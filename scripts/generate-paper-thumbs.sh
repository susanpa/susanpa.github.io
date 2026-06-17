#!/usr/bin/env bash
# Generate publication thumbnail PNGs from paper PDFs.
#
# Drop a PDF of each paper into papers/ using the naming convention
#   averett-<year>-<slug>.pdf   (e.g. averett-2025-circadian.pdf)
# matching the basenames referenced in research.html, then run this script.
# It renders the configured page of each PDF to img/papers/<basename>.png.
# Where no PDF (and thus no PNG) exists, research.html falls back to the SVG
# placeholder at img/papers/placeholders/<basename>.svg (see
# scripts/generate-paper-placeholders.py).
#
# Backend: prefers pdftoppm (poppler, `brew install poppler`) for crisp output;
# falls back to macOS `qlmanage` (Quick Look, no install) when poppler is absent.

set -euo pipefail

cd "$(dirname "$0")/.."

# Fixed render size (max dimension). Display in CSS is constrained further.
THUMB_WIDTH=800

# Per-paper page overrides. Add lines as needed: "<basename>:<page>".
# basename is the .pdf filename without extension. Page is 1-indexed.
# (Use this when page 1 of a PDF is a publisher cover sheet, not the article.)
PAGE_OVERRIDES=(
  # "averett-2025-circadian:2"
)

get_page() {
  local base="$1"
  # Guard the expansion so `set -u` doesn't error when PAGE_OVERRIDES is empty.
  for entry in "${PAGE_OVERRIDES[@]+"${PAGE_OVERRIDES[@]}"}"; do
    if [[ "${entry%%:*}" == "$base" ]]; then
      echo "${entry#*:}"
      return
    fi
  done
  echo 1
}

PDFTOPPM="$(command -v pdftoppm || true)"
if [[ -z "$PDFTOPPM" && -x /opt/homebrew/bin/pdftoppm ]]; then
  PDFTOPPM=/opt/homebrew/bin/pdftoppm
fi
QLMANAGE="$(command -v qlmanage || true)"

if [[ -z "$PDFTOPPM" && -z "$QLMANAGE" ]]; then
  echo "Neither pdftoppm nor qlmanage found. Install poppler with: brew install poppler" >&2
  exit 1
fi
if [[ -n "$PDFTOPPM" ]]; then
  echo "Using pdftoppm (poppler)."
else
  echo "pdftoppm not found; using qlmanage (Quick Look) fallback. For higher-quality"
  echo "thumbnails, install poppler: brew install poppler"
fi

mkdir -p img/papers

shopt -s nullglob
pdfs=(papers/*.pdf)

if [[ ${#pdfs[@]} -eq 0 ]]; then
  echo "No PDFs found in papers/. Drop your paper PDFs there using the naming"
  echo "convention averett-<year>-<slug>.pdf, then re-run this script."
  exit 0
fi

count=0
for pdf in "${pdfs[@]}"; do
  base="$(basename "$pdf" .pdf)"
  out_png="img/papers/${base}.png"
  page="$(get_page "$base")"

  if [[ -f "$out_png" && "$out_png" -nt "$pdf" ]]; then
    echo "skip (up-to-date): $out_png"
    continue
  fi

  echo "generating (page $page): $out_png"
  if [[ -n "$PDFTOPPM" ]]; then
    tmp="$(mktemp -t pdfthumb.XXXXXX)"
    "$PDFTOPPM" -png -f "$page" -l "$page" -singlefile -scale-to-x "$THUMB_WIDTH" -scale-to-y -1 "$pdf" "$tmp" >/dev/null 2>&1 || true
    if [[ -f "${tmp}.png" ]]; then
      mv "${tmp}.png" "$out_png"
      count=$((count + 1))
    else
      echo "  WARN: pdftoppm did not produce output for $pdf" >&2
    fi
    rm -f "$tmp"
  else
    # qlmanage renders only the first page; PAGE_OVERRIDES are ignored here.
    [[ "$page" != "1" ]] && echo "  NOTE: qlmanage renders page 1 only (override page $page ignored)."
    tmpdir="$(mktemp -d -t qlthumb.XXXXXX)"
    "$QLMANAGE" -t -s "$THUMB_WIDTH" -o "$tmpdir" "$pdf" >/dev/null 2>&1 || true
    produced="${tmpdir}/$(basename "$pdf").png"
    if [[ -f "$produced" ]]; then
      mv "$produced" "$out_png"
      count=$((count + 1))
    else
      echo "  WARN: qlmanage did not produce output for $pdf" >&2
    fi
    rm -rf "$tmpdir"
  fi
done

echo
echo "Generated $count thumbnail(s) in img/papers/."
echo "If you removed a PDF, also delete the matching .png to fall back to the SVG placeholder."
